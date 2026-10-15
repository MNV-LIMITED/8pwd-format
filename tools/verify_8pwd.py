#!/usr/bin/env python3
"""verify_8pwd.py — inspect an 8PWD backup file (.8pwd) without the app.

    python3 verify_8pwd.py Backup.8pwd
    python3 verify_8pwd.py Backup.8pwd --password 'your backup password'
    python3 verify_8pwd.py Backup.8pwd --json
    python3 verify_8pwd.py Backup.8pwd --show-names      # also list account names (never passwords)

What it does
  * Tells you whether the file is a PLAIN or an ENCRYPTED 8PWD backup.
  * Prints the format version, export date and how many accounts, folders,
    two-factor codes, Wi-Fi networks, cards, identities and passkeys it holds
    (plus, for 4.0 files, aliases, recovery-code entries and account links).
  * Prints the file's SHA-256 so you can compare it with the one 8PWD shows
    under Me > Export > Verify a backup file.
  * Never modifies the file, never uses the network, never prints a password.

Encrypted backups
  Layout (big-endian):  b"8PWDENC1" | iterations (4 bytes) | salt (16 bytes) |
                        AES-256-GCM nonce (12) + ciphertext + tag (16)
  Key = PBKDF2-HMAC-SHA256(password as UTF-8, salt, iterations, 32 bytes).
  The header is parsed with the standard library alone. To actually decrypt
  and count, pass --password and install the `cryptography` package
  (pip install cryptography); nothing else is needed.

License: CC0 1.0 (public domain). https://www.8pwd.com/your-data
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import xml.etree.ElementTree as ET

MAGIC = b"8PWDENC1"
SHARE_MAGIC = b"8PWDSHARE\x01"
VAULT_MAGIC = b"8PWDVAULT\x01"
SALT_LEN = 16
NONCE_LEN = 12
TAG_LEN = 16


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_header(data: bytes) -> dict:
    """Return the envelope parameters of an encrypted backup (no key needed)."""
    if not data.startswith(MAGIC):
        raise ValueError("not an encrypted 8PWD backup")
    off = len(MAGIC)
    (iterations,) = struct.unpack(">I", data[off:off + 4])
    off += 4
    salt = data[off:off + SALT_LEN]
    off += SALT_LEN
    body = data[off:]
    if iterations == 0 or len(body) < NONCE_LEN + TAG_LEN + 1:
        raise ValueError("corrupted envelope")
    return {"iterations": iterations, "salt_hex": salt.hex(), "nonce_hex": body[:NONCE_LEN].hex(),
            "ciphertext_bytes": len(body) - NONCE_LEN - TAG_LEN, "salt": salt, "body": body}


def decrypt(data: bytes, password: str) -> bytes:
    h = parse_header(data)
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        sys.exit("Decrypting needs the `cryptography` package: pip install cryptography")
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), h["salt"], h["iterations"], 32)
    body = h["body"]
    nonce, ct = body[:NONCE_LEN], body[NONCE_LEN:]
    try:
        return AESGCM(key).decrypt(nonce, ct, None)
    except Exception:
        sys.exit("Wrong password, or the file is damaged (authentication tag did not match).")


def count_vault(xml_bytes: bytes, show_names: bool) -> dict:
    root = ET.fromstring(xml_bytes)
    if root.tag != "vault":
        raise ValueError(f"root element is <{root.tag}>, expected <vault>")
    accounts = root.findall(".//tree//account")
    out = {
        "app": root.get("app"),
        "format_version": root.get("version"),
        "exported_at": root.get("exportedAt"),
        "folders": len(root.findall(".//tree//folder")),
        "accounts": len(accounts),
        "fields": sum(len(a.findall("./fields/field")) for a in accounts),
        "formatted_blocks": len(root.findall("./formattedBlocks/formattedBlock")),
        "two_factor_codes": len(root.findall("./totps/totp")),
        "wifi_networks": len(root.findall("./wifi/network")),
        "cards": len(root.findall("./cards/card")),
        "identities": len(root.findall("./identities/identity")),
        "passkeys": len(root.findall("./passkeys/passkey")),
        # 4.0 additions (all optional; older files simply report 0)
        "aliases": sum(len(a.findall("./alias")) for a in accounts),
        "recovery_code_entries": len(root.findall("./recoveryCodes/codes")),
        "links": len(root.findall("./links/link")),
    }
    if show_names:
        out["account_names"] = sorted(a.get("name", "") for a in accounts)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Inspect an 8PWD backup file without the app.")
    ap.add_argument("file")
    ap.add_argument("--password", help="backup password (only for encrypted backups)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--show-names", action="store_true", help="also list account names (never passwords)")
    args = ap.parse_args()

    with open(args.file, "rb") as f:
        data = f.read()

    report: dict = {"file": args.file, "size_bytes": len(data), "sha256": sha256(data)}

    if data.startswith(SHARE_MAGIC) or data.startswith(VAULT_MAGIC):
        kind = "share (.8pwdshare)" if data.startswith(SHARE_MAGIC) else "AirDrop vault transfer"
        report["type"] = kind
        inner = data[len(SHARE_MAGIC):] if data.startswith(SHARE_MAGIC) else data[len(VAULT_MAGIC):]
        h = parse_header(inner)
        report["encrypted"] = True
        report["pbkdf2_iterations"] = h["iterations"]
        report["note"] = "Protected by the 6-digit one-time code shown on the sending device; the payload is JSON, not a vault XML."
    elif data.startswith(MAGIC):
        report["type"] = "8PWD backup"
        report["encrypted"] = True
        h = parse_header(data)
        report["pbkdf2_iterations"] = h["iterations"]
        report["salt_hex"] = h["salt_hex"]
        report["ciphertext_bytes"] = h["ciphertext_bytes"]
        if args.password:
            xml_bytes = decrypt(data, args.password)
            report["decrypted"] = True
            report.update(count_vault(xml_bytes, args.show_names))
        else:
            report["decrypted"] = False
            report["note"] = "Pass --password to decrypt and count (needs `pip install cryptography`)."
    else:
        report["type"] = "8PWD backup"
        report["encrypted"] = False
        try:
            report.update(count_vault(data, args.show_names))
        except ET.ParseError as e:
            report["error"] = f"not well-formed XML: {e}"
        except ValueError as e:
            report["error"] = str(e)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for k, v in report.items():
            if k == "account_names":
                print(f"{k}:")
                for n in v:
                    print(f"  - {n}")
            else:
                print(f"{k}: {v}")
    return 1 if "error" in report else 0


if __name__ == "__main__":
    sys.exit(main())
