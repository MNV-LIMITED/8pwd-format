# The .8pwd file format

> Mirror of [www.8pwd.com/open-format](https://www.8pwd.com/open-format), generated from the same source. The website is the canonical version and is also available in 12 other languages (links in the [README](README.md)).

No server means the file is everything. So the file format is public, documented here in full, released into the public domain, and comes with sample files and a verifier you can run without 8PWD. If we disappeared tomorrow, your passwords would still be a readable file.

## What “open” means here

- **Documented**: every element and attribute the app writes is listed on this page, with the rules a reader must follow.
- **Public domain**: the specification is released under **CC0 1.0** — anyone may build readers, writers or converters without asking us, naming us or paying us.
- **Verifiable**: [verify_8pwd.py](tools/verify_8pwd.py) (CC0) inspects, counts and decrypts a backup with no dependencies beyond Python 3.
- **Stable**: the version number only goes up; new sections are only ever appended; a reader ignores what it does not know. Format changes are listed on the [What's new](https://www.8pwd.com/changelog) page.
- **Mirrored**: this page, both sample files and the verifier are mirrored at [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format), where every change to the format has a public, dated history.

The app itself is not open source; the format is. That is the promise that matters for your data.

## The plain backup: one UTF-8 XML file

Export without a password and you get a `.8pwd` file that is plain XML. The root element is `<vault>` with the attributes `app` (the product name), `version` (currently **8**), `exportedAt` (ISO 8601 UTC), `nodes` and `formattedBlocks` (counts). Inside, in this order:

- `<tree>` — folders and accounts. `<folder uuid name>` nests freely. `<account uuid name favorite icon category created updated>` holds `<fields>`, and each `<field name kind hidden>value</field>` is one line of the record. `created` and `updated` *(5.0)* are optional: when the record was made and last edited, in Unix seconds.
- The **meaning** of a field is its `kind`: `username`, `password`, `url`, `email`, `phone`, `note` or `text` (free custom field). `name` is only the label the user sees — it is localized (“Password”, “密碼”, “Passwort”) and should not be used to decide what a field is. `hidden="true"` marks a field the app masks by default.
- `<formattedBlocks>` — reusable text blocks: `<formattedBlock uuid name recordSeparator>` with a `<template>` and `<accountRefs><ref uuid/></accountRefs>`.
- `<totps>` — two-factor secrets as standard `<totp uuid note linkedAccount>otpauth://…</totp>` URIs; `linkedAccount` is the uuid of the first account they belong to (kept for older readers — the full many-to-many set is in `<links>`, see below). Any authenticator can import the URI.
- `<recoveryCodes>` *(4.0)* — the one-time backup codes a site hands out when two-factor is set up, one `<codes totp="uuid">free text, newlines kept</codes>` per code entry. Kept outside `<totp>` so the URI stays a pure URI.
- `<links>` *(4.0)* — `<link account="uuid" kind="totp|card|identity" target="uuid"/>`: which two-factor codes, cards and identities belong to which accounts, many-to-many. Both ends are uuids found elsewhere in the same file; a reader that only wants passwords can skip it.
- Inside `<account>` *(4.0)*: optional `<alias>other sign-in name</alias>` children before `<fields>` — the account's other usernames or e-mail addresses. Search and AutoFill in the app match them; a reader may treat them as extra usernames for the same password.
- `<wifi>` — `<network uuid ssid security password hidden note/>`.
- `<cards>` — `<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>` plus billing-address attributes prefixed `b` (`bName`, `bStreet1`, `bCity`…).
- `<identities>` — `<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>` with child `<email label>`, `<phone label>` and `<address label aStreet1 aCity aRegion aPostal aCountry/>` elements.
- `<passkeys>` — `<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>`; the binary values are Base64. Passkeys are written **only** into encrypted backups.
- Housekeeping sections the app uses for itself: `<preferences>` (home shortcuts and, from 4.0, the Me › My Shortcuts grid as `<quickAccess>` / `<quickAccessHidden>`), `<usage>`, `<siteNotes>`, `<checkups>`. A reader that only wants passwords can skip them.

Rules for readers: unknown elements and attributes are ignored; missing optional sections mean “none”; `uuid` values are stable across exports, so the same account keeps the same id; dates in `created` / `updated` / `at` are Unix seconds.

Merging two copies *(5.0)*: when a file holds an account whose `uuid` the app already has, **Smart merge** keeps the copy with the later `updated` time and files a replaced password into that account's history; an account without `updated` (exported before 5.0) is kept as it is on the device. A merge never deletes anything. Other readers are welcome to follow the same rule.

## The encrypted backup: a small envelope around the same XML

Switch **Encrypt this backup** on (or include passkeys) and the same XML is sealed as follows, all big-endian:

1. 8 bytes ASCII magic `8PWDENC1`.
2. 4 bytes: PBKDF2 iteration count as an unsigned 32-bit integer — **600,000** when the app exports.
3. 16 bytes: random salt.
4. 12 bytes: AES-256-GCM nonce, followed by the ciphertext and the 16-byte GCM tag (the usual *nonce ‖ ciphertext ‖ tag* layout).

The key is **PBKDF2-HMAC-SHA256** of the UTF-8 backup password with that salt and iteration count, 32 bytes long. No associated data. The plaintext is the plain backup above, byte for byte. Shares (`.8pwdshare`) and AirDrop vault transfers use the same envelope with a one-time 6-digit code as the password.

There is no proprietary container, no key escrow and no secret: with the password, two lines of standard library code open the file.

## Sample files

Both samples hold the same invented vault in format 8 — two folders, three accounts (one with an alias, each with `created` / `updated` times), one two-factor code with recovery codes, one Wi-Fi network, one card and one identity, plus the `<links>` section tying the code and the card to their accounts. **Every value in them is made up**; nothing belongs to a real person or site.

- [sample-plain.8pwd](samples/sample-plain.8pwd) — the plain XML, 3 KB. Open it in any text editor.
- [sample-encrypted.8pwd](samples/sample-encrypted.8pwd) — the same vault sealed with the password `example`.

Both import into 8PWD like any other backup (**Me › Import › 8PWD backup**), so you can see exactly how the file maps onto the app.

## Check, count or decrypt a file without the app

`verify_8pwd.py` is one Python 3 file, public domain (CC0), no dependencies for inspection; decrypting needs the optional `cryptography` package.

1. `python3 verify_8pwd.py sample-plain.8pwd` — says whether the file is plain or encrypted, the format version, export date, how many accounts, folders, codes, networks, cards, identities and passkeys it holds (and, from 4.0, aliases, recovery-code entries and links), and its SHA-256.
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example` — decrypts in memory and prints the same counts.
3. `python3 verify_8pwd.py Backup.8pwd --json` — machine-readable output for your own scripts.

It never writes to the file and never touches the network. Read it first; it is short on purpose.

## Getting data out in other shapes

- **CSV**: **Me › Export › Export a universal CSV** writes the common column set (name, URL, username, password, note) that Apple Passwords, 1Password, Bitwarden and the browsers all import. Export works on every plan, Pro or not.
- **Two-factor codes**: each `<totp>` is a standard `otpauth://` URI; the app also shows them as QR codes, one at a time, for moving to another authenticator.
- **Paper**: the printed password book and the emergency kit are the offline fallback for the people you leave behind.

## Licence and promise

To the extent possible under law, MNV LIMITED has waived all copyright and related rights to this format specification under **CC0 1.0 Universal**. The verifier script and the sample files are released under **CC0 1.0** too; the notice is at the top of the script.

We will not add a proprietary container, a server-side key or a format that only this app can read. If a future version changes the format, the version number goes up, old files keep importing, and the change is written on this page and in the release notes.

## See also

- [Your data is always yours](https://www.8pwd.com/your-data)
- [How the vault is encrypted](https://www.8pwd.com/encryption)
- [Why no sync — and how to move a vault](https://www.8pwd.com/why-no-sync)
- [Switching to 8PWD](https://www.8pwd.com/migrate)
