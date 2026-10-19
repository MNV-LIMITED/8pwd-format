# .8pwd-Dateiformat

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · [简体中文](../zh-Hans/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · **Deutsch** · [Français](../fr/README.md) · [Español](../es/README.md) · [Português (Brasil)](../pt-BR/README.md) · [Italiano](../it/README.md) · [العربية](../ar/README.md) · [Русский](../ru/README.md)

Das offene Backup-Format von **8PWD**, dem Offline-Passwortmanager und Authenticator von MNV LIMITED für iPhone, iPad und Mac: unverschlüsseltes XML, eine optionale AES-256-GCM-Hülle, zwei Beispieldateien und ein Prüfskript aus einer einzigen Datei – genug, um jedes Backup ohne die App zu lesen.

**Kanonische Fassung:** https://www.8pwd.com/de/open-format. Dieses Repository wird aus derselben Quelle erzeugt und spiegelt sie, damit sich das Format auch ohne unsere Website lesen, zitieren und prüfen lässt.

| Pfad | Beschreibung |
|---|---|
| [SPEC.md](SPEC.md) | Die vollständige Spezifikation: das unverschlüsselte XML-Backup, die Verschlüsselungshülle, Regeln für Leseprogramme |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | Ein unverschlüsseltes Backup, Formatversion 8 (8PWD 5.0). Jeder Wert darin ist ausgedacht |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | Derselbe Tresor, verschlüsselt mit dem Passwort `example` |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | Eine einzelne Datei für Python 3, die ein Backup untersucht, auszählt und entschlüsselt |

## Eine Datei prüfen

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # nur zum Entschlüsseln nötig
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

Das Prüfskript schreibt nie in die Datei, greift nie aufs Netzwerk zu und gibt nie ein Passwort aus. SHA-256-Prüfsummen der Dateien in diesem Commit (`shasum -a 256 -c` liest diese Liste):

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## Lizenz

Alles hier – Spezifikation, Beispieldateien und Prüfskript – ist gemeinfrei und steht unter **CC0 1.0 Universell** ([Rechtstext auf Englisch](../../LICENSE) · [offizielle Übersetzung von Creative Commons](LICENSE.md)). Sie dürfen Lese-, Schreib- oder Konvertierungsprogramme bauen, ohne uns zu fragen, uns zu nennen oder uns zu bezahlen.

## Die App

Die App selbst ist nicht quelloffen; das Format schon. [8PWD im App Store](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/de/)

## Kontakt

Dieses Repository nimmt keine Issues oder Pull-Requests entgegen. Fragen oder Korrekturen: support@8pwd.com, mit *Format* im Betreff.
