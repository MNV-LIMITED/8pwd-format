# .8pwd file format

**English** · [繁體中文](translations/zh-HK/README.md) · [简体中文](translations/zh-Hans/README.md) · [日本語](translations/ja/README.md) · [한국어](translations/ko/README.md) · [Deutsch](translations/de/README.md) · [Français](translations/fr/README.md) · [Español](translations/es/README.md) · [Português (Brasil)](translations/pt-BR/README.md) · [Italiano](translations/it/README.md) · [العربية](translations/ar/README.md) · [Русский](translations/ru/README.md)

The open backup format of **8PWD**, the offline password manager and authenticator for iPhone, iPad and Mac by MNV LIMITED: plain XML, an optional AES-256-GCM envelope, two sample files and a one-file verifier — enough to read any backup without the app.

**Canonical version:** https://www.8pwd.com/open-format. This repository mirrors it, generated from the same source, so the format can be read, cited and checked without our website.

| Path | What it is |
|---|---|
| [SPEC.md](SPEC.md) | The full specification: the plain XML backup, the encrypted envelope, rules for readers |
| [samples/sample-plain.8pwd](samples/sample-plain.8pwd) | A plain backup, format version 8 (8PWD 5.0). Every value in it is made up |
| [samples/sample-encrypted.8pwd](samples/sample-encrypted.8pwd) | The same vault, encrypted with the password `example` |
| [tools/verify_8pwd.py](tools/verify_8pwd.py) | One Python 3 file that inspects, counts and decrypts a backup |

## Check a file

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # only needed to decrypt
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

The verifier never writes to the file, never uses the network and never prints a password. SHA-256 of the files in this commit (`shasum -a 256 -c` reads this list):

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## Licence

Everything here — specification, sample files and verifier — is dedicated to the public domain under **CC0 1.0 Universal** ([LICENSE](LICENSE)). Build readers, writers or converters without asking us, naming us or paying us.

## The app

The app itself is not open source; the format is. [8PWD on the App Store](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/)

## Contact

This repository does not take issues or pull requests. Questions or corrections: support@8pwd.com, with *Format* in the subject.
