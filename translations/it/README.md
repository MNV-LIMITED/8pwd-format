# Formato di file .8pwd

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · [简体中文](../zh-Hans/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Português (Brasil)](../pt-BR/README.md) · **Italiano** · [العربية](../ar/README.md) · [Русский](../ru/README.md)

Il formato di backup aperto di **8PWD**, il password manager e authenticator offline di MNV LIMITED per iPhone, iPad e Mac: XML in chiaro, una busta AES-256-GCM facoltativa, due file di esempio e uno script di verifica in un unico file — quanto basta per leggere qualsiasi backup senza l'app.

**Versione canonica:** https://www.8pwd.com/it/open-format. Questo repository, generato dalla stessa fonte, ne è la replica, così il formato si può leggere, citare e verificare anche senza il nostro sito.

| Percorso | Descrizione |
|---|---|
| [SPEC.md](SPEC.md) | La specifica completa: il backup XML in chiaro, la busta di cifratura, le regole per i lettori |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | Un backup in chiaro, versione 8 del formato (8PWD 5.0). Ogni valore al suo interno è inventato |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | La stessa cassaforte, cifrata con la password `example` |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | Un unico file Python 3 che ispeziona, conta e decifra un backup |

## Controlla un file

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # serve solo per decifrare
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

Lo script di verifica non scrive mai sul file, non tocca mai la rete e non stampa mai una password. Hash SHA-256 dei file di questo commit (`shasum -a 256 -c` legge questo elenco):

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## Licenza

Tutto ciò che trovi qui — specifica, file di esempio e script di verifica — è rilasciato nel pubblico dominio tramite **CC0 1.0 Universale** ([testo legale in inglese](../../LICENSE) · [traduzione ufficiale di Creative Commons](LICENSE.md)). Puoi realizzare lettori, scrittori o convertitori senza chiederci il permesso, citarci o pagarci.

## L'app

L'app in sé non è open source; il formato sì. [8PWD sull'App Store](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/it/)

## Contatti

Questo repository non accetta issue né pull request. Domande o correzioni: support@8pwd.com, con *Format* nell'oggetto.
