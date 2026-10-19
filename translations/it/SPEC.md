# Il formato di file .8pwd

[English](../../SPEC.md) · [繁體中文](../zh-HK/SPEC.md) · [简体中文](../zh-Hans/SPEC.md) · [日本語](../ja/SPEC.md) · [한국어](../ko/SPEC.md) · [Deutsch](../de/SPEC.md) · [Français](../fr/SPEC.md) · [Español](../es/SPEC.md) · [Português (Brasil)](../pt-BR/SPEC.md) · **Italiano** · [العربية](../ar/SPEC.md) · [Русский](../ru/SPEC.md)

> Traduzione di [SPEC.md](../../SPEC.md), generata dalla stessa fonte di [www.8pwd.com/it/open-format](https://www.8pwd.com/it/open-format). In caso di differenze, prevale la versione inglese.

Niente server significa che il file è tutto. Per questo il formato del file è pubblico, documentato qui per intero, rilasciato nel pubblico dominio, e viene con file di esempio e uno script di verifica che puoi eseguire senza 8PWD. Se sparissimo domani, le tue password sarebbero ancora un file leggibile.

## Cosa significa “aperto” qui

- **Documentato**: ogni elemento e attributo che l'app scrive è elencato in questa pagina, con le regole che un lettore deve seguire.
- **Pubblico dominio**: la specifica è rilasciata sotto **CC0 1.0** — chiunque può realizzare lettori, scrittori o convertitori senza chiederci il permesso, citarci o pagarci.
- **Verificabile**: [verify_8pwd.py](../../tools/verify_8pwd.py) (CC0) ispeziona, conta e decifra un backup senza altre dipendenze oltre a Python 3.
- **Stabile**: il numero di versione può solo salire; le nuove sezioni vengono solo aggiunte in coda; un lettore ignora ciò che non conosce. Le modifiche al formato sono elencate nella pagina [Novità](https://www.8pwd.com/it/changelog).
- **Replicato**: questa pagina, entrambi i file di esempio e lo script di verifica sono replicati su [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format) (in inglese), dove ogni modifica al formato ha una cronologia pubblica e datata.

L'app in sé non è open source; il formato sì. È questa la promessa che conta per i tuoi dati.

## Il backup in chiaro: un unico file XML UTF-8

Esporta senza password e ottieni un file `.8pwd` che è XML in chiaro. L'elemento radice è `<vault>` con gli attributi `app` (il nome del prodotto), `version` (attualmente **8**), `exportedAt` (ISO 8601 UTC), `nodes` e `formattedBlocks` (conteggi). All'interno, in quest'ordine:

- `<tree>` — cartelle e account. `<folder uuid name>` si annida liberamente. `<account uuid name favorite icon category created updated>` contiene `<fields>`, e ogni `<field name kind hidden>valore</field>` è una riga del record. `created` e `updated` *(5.0)* sono facoltativi: quando il record è stato creato e quando è stato modificato l'ultima volta, in secondi Unix.
- Il **significato** di un campo è il suo `kind`: `username`, `password`, `url`, `email`, `phone`, `note` o `text` (campo personalizzato libero). `name` è solo l'etichetta che l'utente vede — è localizzata (“Password”, “密碼”, “Passwort”) e non va usata per decidere che cosa sia un campo. `hidden="true"` contrassegna un campo che l'app maschera per impostazione predefinita.
- `<formattedBlocks>` — blocchi di testo riutilizzabili: `<formattedBlock uuid name recordSeparator>` con un `<template>` e `<accountRefs><ref uuid/></accountRefs>`.
- `<totps>` — i segreti a due fattori come URI standard `<totp uuid note linkedAccount>otpauth://…</totp>`; `linkedAccount` è l'uuid del primo account a cui appartengono (resta per i lettori più vecchi — l'insieme completo dei collegamenti molti a molti è in `<links>`, vedi sotto). Qualsiasi authenticator può importare l'URI.
- `<recoveryCodes>` *(4.0)* — i codici di backup monouso che un sito fornisce quando si attiva la verifica in due passaggi, un elemento `<codes totp="uuid">testo libero, a capo conservati</codes>` per ogni codice. Stanno fuori da `<totp>` perché l'URI resti un URI puro.
- `<links>` *(4.0)* — `<link account="uuid" kind="totp|card|identity" target="uuid"/>`: quali codici a due fattori, carte e identità appartengono a quali account, in una relazione molti a molti. Entrambe le estremità sono uuid presenti altrove nello stesso file; un lettore che vuole solo le password può saltarla.
- Dentro `<account>` *(4.0)*: elementi figli `<alias>altro nome di accesso</alias>` facoltativi, prima di `<fields>` — gli altri nomi utente o indirizzi e-mail dell'account. Nell'app la ricerca e il riempimento automatico li riconoscono; un lettore può trattarli come nomi utente aggiuntivi per la stessa password.
- `<wifi>` — le reti Wi-Fi: `<network uuid ssid security password hidden note/>`.
- `<cards>` — `<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>` più gli attributi dell'indirizzo di fatturazione con prefisso `b` (`bName`, `bStreet1`, `bCity`…).
- `<identities>` — `<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>` con gli elementi figli `<email label>`, `<phone label>` e `<address label aStreet1 aCity aRegion aPostal aCountry/>`.
- `<passkeys>` — `<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>`; i valori binari sono in Base64. Le passkey vengono scritte **solo** nei backup cifrati.
- Sezioni di servizio che l'app usa per sé: `<preferences>` (le scorciatoie della Home e, dalla 4.0, la griglia Io › I miei preferiti come `<quickAccess>` / `<quickAccessHidden>`), `<usage>`, `<siteNotes>`, `<checkups>`. Un lettore che vuole solo le password può saltarle.

Regole per i lettori: elementi e attributi sconosciuti vengono ignorati; le sezioni facoltative mancanti significano “nessuno”; i valori `uuid` sono stabili tra un'esportazione e l'altra, quindi lo stesso account mantiene lo stesso id; le date in `created` / `updated` / `at` sono secondi Unix.

Unire due copie *(5.0)*: quando un file contiene un account il cui `uuid` è già presente nell'app, l'**Unione intelligente** conserva la copia con il valore `updated` più recente e mette la password sostituita nella cronologia di quell'account; un account senza `updated` (esportato prima della 5.0) viene mantenuto così com'è sul dispositivo. Un'unione non elimina mai nulla. Anche gli altri lettori possono seguire la stessa regola.

## Il backup cifrato: una piccola busta attorno allo stesso XML

Attiva **Cifra questo backup** (o includi le passkey) e lo stesso XML viene sigillato così, tutto in big-endian:

1. 8 byte: il magic number ASCII `8PWDENC1`.
2. 4 byte: il conteggio delle iterazioni PBKDF2 come intero a 32 bit senza segno — **600.000** quando esporta l'app.
3. 16 byte: salt casuale.
4. 12 byte: nonce AES-256-GCM, seguito dal testo cifrato e dal tag GCM di 16 byte (la solita disposizione *nonce ‖ ciphertext ‖ tag*).

La chiave è **PBKDF2-HMAC-SHA256** della password di backup in UTF-8 con quel salt e quel conteggio di iterazioni, lunga 32 byte. Nessun dato associato. Il testo in chiaro è il backup in chiaro descritto sopra, byte per byte. Le condivisioni (`.8pwdshare`) e i trasferimenti della cassaforte via AirDrop usano la stessa busta con un codice monouso a 6 cifre come password.

Non c'è nessun contenitore proprietario, nessun deposito di chiavi presso terzi e nessun segreto: con la password, due righe di codice di libreria standard aprono il file.

## File di esempio

Entrambi gli esempi contengono la stessa cassaforte inventata nel formato 8 — due cartelle, tre account (uno con un alias, ciascuno con le date `created` / `updated`), un codice a due fattori con codici di recupero, una rete Wi-Fi, una carta e un'identità, più la sezione `<links>` che collega il codice e la carta ai rispettivi account. **Ogni valore al loro interno è inventato**; nulla appartiene a una persona o a un sito reali.

- [sample-plain.8pwd](../../samples/sample-plain.8pwd) — l'XML in chiaro, 3 KB. Aprilo in qualsiasi editor di testo.
- [sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) — la stessa cassaforte sigillata con la password `example`.

Entrambi si importano in 8PWD come qualsiasi altro backup (**Io › Importa › Backup 8PWD**), così puoi vedere esattamente come il file corrisponde all'app.

## Controlla, conta o decifra un file senza l'app

`verify_8pwd.py` è un unico file Python 3, di pubblico dominio (CC0), senza dipendenze per l'ispezione; per decifrare serve il pacchetto facoltativo `cryptography`.

1. `python3 verify_8pwd.py sample-plain.8pwd` — dice se il file è in chiaro o cifrato, la versione del formato, la data di esportazione, quanti account, cartelle, codici, reti, carte, identità e passkey contiene (e, dalla 4.0, alias, voci di codici di recupero e collegamenti), e il suo SHA-256.
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example` — decifra in memoria e stampa gli stessi conteggi.
3. `python3 verify_8pwd.py Backup.8pwd --json` — output leggibile dalle macchine per i tuoi script.

Non scrive mai sul file e non tocca mai la rete. Leggilo prima: è corto di proposito.

## Portare fuori i dati in altre forme

- **CSV**: **Io › Esporta › Esporta un CSV universale** scrive l'insieme di colonne comune (nome, URL, nome utente, password, nota) che Apple Passwords, 1Password, Bitwarden e i browser importano tutti. L'esportazione funziona con ogni piano, Pro o no.
- **Codici a due fattori**: ogni `<totp>` è un URI `otpauth://` standard; l'app li mostra anche come codici QR, uno alla volta, per passare a un altro authenticator.
- **Carta**: il libretto delle password stampato e il kit di emergenza sono la riserva offline per chi resta dopo di te.

## Licenza e promessa

Nella misura consentita dalla legge, MNV LIMITED ha rinunciato a tutti i diritti d'autore e ai diritti connessi su questa specifica del formato ai sensi della **CC0 1.0 Universal**. Anche lo script di verifica e i file di esempio sono rilasciati sotto **CC0 1.0**; l'avviso è in cima allo script.

Non aggiungeremo un contenitore proprietario, una chiave lato server o un formato che solo questa app può leggere. Se una versione futura cambia il formato, il numero di versione sale, i vecchi file continuano a importarsi e la modifica viene scritta in questa pagina e nelle note di rilascio.

## Vedi anche

- [I tuoi dati sono sempre tuoi](https://www.8pwd.com/it/your-data)
- [Come è cifrata la cassaforte](https://www.8pwd.com/it/encryption)
- [Perché non sincronizza — e come spostare una cassaforte](https://www.8pwd.com/it/why-no-sync)
- [Passare a 8PWD](https://www.8pwd.com/it/migrate)
