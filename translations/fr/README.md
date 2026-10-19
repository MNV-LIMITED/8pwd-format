# Format de fichier .8pwd

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · [简体中文](../zh-Hans/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [Deutsch](../de/README.md) · **Français** · [Español](../es/README.md) · [Português (Brasil)](../pt-BR/README.md) · [Italiano](../it/README.md) · [العربية](../ar/README.md) · [Русский](../ru/README.md)

Le format de sauvegarde ouvert de **8PWD**, le gestionnaire de mots de passe et authentificateur hors ligne de MNV LIMITED pour iPhone, iPad et Mac : du XML en clair, une enveloppe AES-256-GCM facultative, deux fichiers d’exemple et un vérificateur en un seul fichier — de quoi lire n’importe quelle sauvegarde sans l’app.

**Version canonique :** https://www.8pwd.com/fr/open-format. Ce dépôt en est le miroir, généré à partir de la même source, pour que le format puisse être lu, cité et vérifié sans passer par notre site.

| Chemin | Description |
|---|---|
| [SPEC.md](SPEC.md) | La spécification complète : la sauvegarde XML en clair, l’enveloppe de chiffrement, les règles pour les lecteurs |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | Une sauvegarde en clair, version 8 du format (8PWD 5.0). Toutes les valeurs y sont fictives |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | Le même coffre, chiffré avec le mot de passe `example` |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | Un seul fichier Python 3 qui inspecte, compte et déchiffre une sauvegarde |

## Vérifier un fichier

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # uniquement pour déchiffrer
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

Le vérificateur n’écrit jamais dans le fichier, ne touche jamais au réseau et n’affiche jamais de mot de passe. Empreintes SHA-256 des fichiers de ce commit (`shasum -a 256 -c` lit cette liste) :

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## Licence

Tout ce qui se trouve ici — spécification, fichiers d’exemple et vérificateur — est placé dans le domaine public sous **CC0 1.0 Universel** ([texte juridique en anglais](../../LICENSE) · [traduction officielle de Creative Commons](LICENSE.md)). Vous pouvez créer des lecteurs, des outils d’écriture ou des convertisseurs sans nous demander la permission, sans nous citer et sans nous payer.

## L’app

L’app elle-même n’est pas open source ; le format, si. [8PWD sur l’App Store](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/fr/)

## Contact

Ce dépôt n’accepte ni issues ni pull requests. Questions ou corrections : support@8pwd.com, avec *Format* dans l’objet.
