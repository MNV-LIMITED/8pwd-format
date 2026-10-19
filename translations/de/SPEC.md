# Das .8pwd-Dateiformat

[English](../../SPEC.md) · [繁體中文](../zh-HK/SPEC.md) · [简体中文](../zh-Hans/SPEC.md) · [日本語](../ja/SPEC.md) · [한국어](../ko/SPEC.md) · **Deutsch** · [Français](../fr/SPEC.md) · [Español](../es/SPEC.md) · [Português (Brasil)](../pt-BR/SPEC.md) · [Italiano](../it/SPEC.md) · [العربية](../ar/SPEC.md) · [Русский](../ru/SPEC.md)

> Übersetzung von [SPEC.md](../../SPEC.md), aus derselben Quelle erzeugt wie [www.8pwd.com/de/open-format](https://www.8pwd.com/de/open-format). Bei Abweichungen ist die englische Fassung maßgeblich.

Kein Server heißt: Die Datei ist alles. Deshalb ist das Dateiformat öffentlich – hier vollständig dokumentiert, als gemeinfrei freigegeben, mit Beispieldateien und einem Prüfskript, das Sie ohne 8PWD ausführen können. Wenn wir morgen verschwänden, wären Ihre Passwörter immer noch eine lesbare Datei.

## Was „offen“ hier bedeutet

- **Dokumentiert**: Jedes Element und jedes Attribut, das die App schreibt, ist auf dieser Seite aufgeführt, samt den Regeln, die ein Leseprogramm befolgen muss.
- **Gemeinfrei**: Die Spezifikation steht unter **CC0 1.0** – jeder darf Lese-, Schreib- oder Konvertierungsprogramme bauen, ohne uns zu fragen, uns zu nennen oder uns zu bezahlen.
- **Prüfbar**: [verify_8pwd.py](../../tools/verify_8pwd.py) (CC0) untersucht, zählt und entschlüsselt ein Backup ohne andere Abhängigkeiten als Python 3.
- **Stabil**: Die Versionsnummer steigt nur; neue Abschnitte werden immer nur angehängt; ein Leseprogramm ignoriert, was es nicht kennt. Formatänderungen stehen auf der Seite [Neue Funktionen](https://www.8pwd.com/de/changelog).
- **Gespiegelt**: Diese Seite, beide Beispieldateien und das Prüfskript sind unter [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format) (englischsprachig) gespiegelt; dort ist jede Änderung am Format öffentlich und mit Datum nachvollziehbar.

Die App selbst ist nicht quelloffen; das Format schon. Das ist das Versprechen, auf das es für Ihre Daten ankommt.

## Das unverschlüsselte Backup: eine UTF-8-XML-Datei

Exportieren Sie ohne Passwort, erhalten Sie eine `.8pwd`-Datei, die unverschlüsseltes XML ist. Das Wurzelelement ist `<vault>` mit den Attributen `app` (der Produktname), `version` (derzeit **8**), `exportedAt` (ISO 8601 UTC), `nodes` und `formattedBlocks` (Zähler). Darin, in dieser Reihenfolge:

- `<tree>` – Ordner und Konten. `<folder uuid name>` lässt sich beliebig verschachteln. `<account uuid name favorite icon category created updated>` enthält `<fields>`, und jedes `<field name kind hidden>value</field>` ist eine Zeile des Eintrags. `created` und `updated` *(5.0)* sind optional: wann der Eintrag angelegt und zuletzt bearbeitet wurde, in Unix-Sekunden.
- Die **Bedeutung** eines Feldes ist sein `kind`: `username`, `password`, `url`, `email`, `phone`, `note` oder `text` (freies eigenes Feld). `name` ist nur die Beschriftung, die der Nutzer sieht – sie ist lokalisiert („Password“, „密碼“, „Passwort“) und sollte nicht herangezogen werden, um zu entscheiden, was ein Feld ist. `hidden="true"` kennzeichnet ein Feld, das die App standardmäßig verdeckt.
- `<formattedBlocks>` – wiederverwendbare Textblöcke: `<formattedBlock uuid name recordSeparator>` mit einem `<template>` und `<accountRefs><ref uuid/></accountRefs>`.
- `<totps>` – Zwei-Faktor-Geheimschlüssel als Standard-URIs `<totp uuid note linkedAccount>otpauth://…</totp>`; `linkedAccount` ist die uuid des ersten Kontos, zu dem sie gehören (für ältere Leseprogramme beibehalten – die vollständige Viele-zu-viele-Zuordnung steht in `<links>`, siehe unten). Jeder Authenticator kann die URI importieren.
- `<recoveryCodes>` *(4.0)* – die einmaligen Backup-Codes, die eine Website beim Einrichten der Zwei-Faktor-Authentifizierung ausgibt; je Code-Eintrag ein `<codes totp="uuid">free text, newlines kept</codes>`. Bewusst außerhalb von `<totp>`, damit die URI eine reine URI bleibt.
- `<links>` *(4.0)* – `<link account="uuid" kind="totp|card|identity" target="uuid"/>`: welche Zwei-Faktor-Codes, Karten und Identitäten zu welchen Konten gehören (viele-zu-viele). Beide Enden sind uuids, die an anderer Stelle derselben Datei stehen; ein Leseprogramm, das nur Passwörter will, kann den Abschnitt überspringen.
- Innerhalb von `<account>` *(4.0)*: optionale Kindelemente `<alias>other sign-in name</alias>` vor `<fields>` – die weiteren Benutzernamen oder E-Mail-Adressen des Kontos. Suche und „Automatisch ausfüllen“ in der App berücksichtigen sie; ein Leseprogramm kann sie als zusätzliche Benutzernamen für dasselbe Passwort behandeln.
- `<wifi>` – `<network uuid ssid security password hidden note/>`.
- `<cards>` – `<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>` plus Rechnungsadress-Attribute mit dem Präfix `b` (`bName`, `bStreet1`, `bCity` …).
- `<identities>` – `<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>` mit den Kindelementen `<email label>`, `<phone label>` und `<address label aStreet1 aCity aRegion aPostal aCountry/>`.
- `<passkeys>` – `<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>`; die binären Werte sind Base64. Passkeys werden **nur** in verschlüsselte Backups geschrieben.
- Verwaltungsabschnitte, die die App für sich selbst nutzt: `<preferences>` (die Abkürzungen auf „Start“ und ab 4.0 das Raster Ich › Meine Favoriten als `<quickAccess>` / `<quickAccessHidden>`), `<usage>`, `<siteNotes>`, `<checkups>`. Ein Leseprogramm, das nur Passwörter will, kann sie überspringen.

Regeln für Leseprogramme: Unbekannte Elemente und Attribute werden ignoriert; fehlende optionale Abschnitte bedeuten „keine“; `uuid`-Werte bleiben über Exporte hinweg stabil, dasselbe Konto behält also dieselbe ID; Datumsangaben in `created` / `updated` / `at` sind Unix-Sekunden.

Zusammenführen zweier Kopien *(5.0)*: Enthält eine Datei ein Konto, dessen `uuid` die App bereits kennt, behält **Intelligent zusammenführen** die Kopie mit der späteren `updated`-Zeit und legt ein ersetztes Passwort im Verlauf dieses Kontos ab; ein Konto ohne `updated` (vor 5.0 exportiert) bleibt so, wie es auf dem Gerät ist. Ein Zusammenführen löscht nie etwas. Andere Leseprogramme dürfen gern derselben Regel folgen.

## Das verschlüsselte Backup: eine kleine Hülle um dasselbe XML

Schalten Sie **Dieses Backup verschlüsseln** ein (oder nehmen Sie Passkeys auf), wird dasselbe XML wie folgt versiegelt, alles Big-Endian:

1. 8 Bytes ASCII-Kennung `8PWDENC1`.
2. 4 Bytes: PBKDF2-Iterationszahl als vorzeichenlose 32-Bit-Ganzzahl – **600.000**, wenn die App exportiert.
3. 16 Bytes: zufälliges Salt.
4. 12 Bytes: AES-256-GCM-Nonce, gefolgt vom Chiffretext und dem 16-Byte-GCM-Tag (das übliche Layout *nonce ‖ ciphertext ‖ tag*).

Der Schlüssel ist **PBKDF2-HMAC-SHA256** des UTF-8-Backup-Passworts mit diesem Salt und dieser Iterationszahl, 32 Bytes lang. Keine zusätzlichen authentifizierten Daten. Der Klartext ist das unverschlüsselte Backup von oben, Byte für Byte. Freigaben (`.8pwdshare`) und AirDrop-Tresorübertragungen verwenden dieselbe Hülle mit einem einmaligen 6-stelligen Code als Passwort.

Es gibt keinen proprietären Container, keine Schlüsselhinterlegung und kein Geheimnis: Mit dem Passwort öffnen zwei Zeilen Standardbibliothekscode die Datei.

## Beispieldateien

Beide Beispiele enthalten denselben erfundenen Tresor im Format 8 – zwei Ordner, drei Konten (eines mit einem Alias, jedes mit Zeitangaben in `created` / `updated`), einen Zwei-Faktor-Code mit Wiederherstellungscodes, ein Wi-Fi-Netzwerk, eine Karte und eine Identität, dazu den Abschnitt `<links>`, der den Code und die Karte mit ihren Konten verknüpft. **Jeder Wert darin ist ausgedacht**; nichts gehört einer echten Person oder Website.

- [sample-plain.8pwd](../../samples/sample-plain.8pwd) – das unverschlüsselte XML, 3 KB. Öffnen Sie es in einem beliebigen Texteditor.
- [sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) – derselbe Tresor, versiegelt mit dem Passwort `example`.

Beide lassen sich wie jedes andere Backup in 8PWD importieren (**Ich › Import › 8PWD-Backup**), sodass Sie genau sehen, wie die Datei auf die App abgebildet wird.

## Eine Datei ohne die App prüfen, auszählen oder entschlüsseln

`verify_8pwd.py` ist eine einzelne Python-3-Datei, gemeinfrei (CC0), ohne Abhängigkeiten fürs Untersuchen; das Entschlüsseln braucht das optionale Paket `cryptography`.

1. `python3 verify_8pwd.py sample-plain.8pwd` – sagt, ob die Datei unverschlüsselt oder verschlüsselt ist, die Formatversion, das Exportdatum, wie viele Konten, Ordner, Codes, Netzwerke, Karten, Identitäten und Passkeys sie enthält (und ab 4.0 Aliasse, Einträge mit Wiederherstellungscodes und Verknüpfungen), und ihren SHA-256.
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example` – entschlüsselt im Arbeitsspeicher und gibt dieselben Zähler aus.
3. `python3 verify_8pwd.py Backup.8pwd --json` – maschinenlesbare Ausgabe für Ihre eigenen Skripte.

Es schreibt nie in die Datei und greift nie aufs Netzwerk zu. Lesen Sie es zuerst; es ist mit Absicht kurz.

## Daten in anderen Formen herausholen

- **CSV**: **Ich › Export › Universelle CSV exportieren** schreibt den üblichen Spaltensatz (Name, URL, Benutzername, Passwort, Notiz), den Apple Passwords, 1Password, Bitwarden und die Browser alle importieren. Der Export funktioniert in jedem Tarif, mit oder ohne Pro.
- **Zwei-Faktor-Codes**: Jedes `<totp>` ist eine Standard-`otpauth://`-URI; die App zeigt sie auch als QR-Codes, einen nach dem anderen, zum Umzug in einen anderen Authenticator.
- **Papier**: Das gedruckte Passwortbuch und das Notfall-Kit sind die Offline-Absicherung für die Menschen, die Sie zurücklassen.

## Lizenz und Versprechen

Soweit gesetzlich möglich, hat MNV LIMITED unter **CC0 1.0 Universal** auf alle Urheber- und verwandten Schutzrechte an dieser Formatspezifikation verzichtet. Das Prüfskript und die Beispieldateien stehen ebenfalls unter **CC0 1.0**; der Hinweis darauf steht am Anfang des Skripts.

Wir werden keinen proprietären Container, keinen serverseitigen Schlüssel und kein Format hinzufügen, das nur diese App lesen kann. Ändert eine künftige Version das Format, steigt die Versionsnummer, alte Dateien lassen sich weiterhin importieren, und die Änderung wird auf dieser Seite und in den Versionshinweisen festgehalten.

## Siehe auch

- [Ihre Daten gehören immer Ihnen](https://www.8pwd.com/de/your-data)
- [Wie der Tresor verschlüsselt ist](https://www.8pwd.com/de/encryption)
- [Warum keine Synchronisierung – und wie Sie einen Tresor umziehen](https://www.8pwd.com/de/why-no-sync)
- [Wechsel zu 8PWD](https://www.8pwd.com/de/migrate)
