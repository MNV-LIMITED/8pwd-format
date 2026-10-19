# Le format de fichier .8pwd

[English](../../SPEC.md) · [繁體中文](../zh-HK/SPEC.md) · [简体中文](../zh-Hans/SPEC.md) · [日本語](../ja/SPEC.md) · [한국어](../ko/SPEC.md) · [Deutsch](../de/SPEC.md) · **Français** · [Español](../es/SPEC.md) · [Português (Brasil)](../pt-BR/SPEC.md) · [Italiano](../it/SPEC.md) · [العربية](../ar/SPEC.md) · [Русский](../ru/SPEC.md)

> Traduction de [SPEC.md](../../SPEC.md), générée à partir de la même source que [www.8pwd.com/fr/open-format](https://www.8pwd.com/fr/open-format). En cas de divergence, la version anglaise prévaut.

Sans serveur, le fichier est tout. Le format de fichier est donc public, documenté ici en intégralité, placé dans le domaine public, et livré avec des fichiers d’exemple et un vérificateur que vous pouvez lancer sans 8PWD. Si nous disparaissions demain, vos mots de passe resteraient un fichier lisible.

## Ce que « ouvert » veut dire ici

- **Documenté** : chaque élément et chaque attribut que l’app écrit est listé sur cette page, avec les règles qu’un lecteur doit suivre.
- **Domaine public** : la spécification est publiée sous **CC0 1.0** — n’importe qui peut créer des lecteurs, des outils d’écriture ou des convertisseurs sans nous demander la permission, sans nous citer et sans nous payer.
- **Vérifiable** : [verify_8pwd.py](../../tools/verify_8pwd.py) (CC0) inspecte, compte et déchiffre une sauvegarde sans autre dépendance que Python 3.
- **Stable** : le numéro de version ne fait qu’augmenter ; les nouvelles sections sont toujours ajoutées à la fin ; un lecteur ignore ce qu’il ne connaît pas. Les changements de format sont listés sur la page [Nouveautés](https://www.8pwd.com/fr/changelog).
- **Mis en miroir** : cette page, les deux fichiers d’exemple et le vérificateur sont mis en miroir sur [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format) (en anglais), où chaque changement apporté au format est consigné dans un historique public et daté.

L’app elle-même n’est pas open source ; le format, si. C’est la promesse qui compte pour vos données.

## La sauvegarde en clair : un seul fichier XML UTF-8

Exportez sans mot de passe et vous obtenez un fichier `.8pwd` qui est du XML en clair. L’élément racine est `<vault>`, avec les attributs `app` (le nom du produit), `version` (actuellement **8**), `exportedAt` (ISO 8601 UTC), `nodes` et `formattedBlocks` (des compteurs). À l’intérieur, dans cet ordre :

- `<tree>` — les dossiers et les comptes. `<folder uuid name>` s’imbrique librement. `<account uuid name favorite icon category created updated>` contient `<fields>`, et chaque `<field name kind hidden>value</field>` est une ligne de l’enregistrement. `created` et `updated` *(5.0)* sont facultatifs : la date de création de l’enregistrement et celle de sa dernière modification, en secondes Unix.
- Le **sens** d’un champ est donné par son `kind` : `username`, `password`, `url`, `email`, `phone`, `note` ou `text` (champ personnalisé libre). `name` n’est que le libellé que voit l’utilisateur — il est localisé (« Mot de passe », « Password », « 密碼 ») et ne doit pas servir à décider ce qu’est un champ. `hidden="true"` marque un champ que l’app masque par défaut.
- `<formattedBlocks>` — des blocs de texte réutilisables : `<formattedBlock uuid name recordSeparator>` avec un `<template>` et `<accountRefs><ref uuid/></accountRefs>`.
- `<totps>` — les secrets à deux facteurs, sous forme d’URI standard `<totp uuid note linkedAccount>otpauth://…</totp>` ; `linkedAccount` est l’uuid du premier compte auquel ils appartiennent (conservé pour les lecteurs plus anciens — l’ensemble complet des liens, en plusieurs-à-plusieurs, se trouve dans `<links>`, voir plus bas). N’importe quel authentificateur peut importer l’URI.
- `<recoveryCodes>` *(4.0)* — les codes de secours à usage unique qu’un site fournit quand vous activez l’authentification à deux facteurs : un élément `<codes totp="uuid">free text, newlines kept</codes>` par entrée de codes (texte libre, retours à la ligne conservés). Ils sont placés hors de `<totp>` pour que l’URI reste une URI pure.
- `<links>` *(4.0)* — `<link account="uuid" kind="totp|card|identity" target="uuid"/>` : quels codes à deux facteurs, cartes et identités appartiennent à quels comptes, en plusieurs-à-plusieurs. Les deux extrémités sont des uuid présents ailleurs dans le même fichier ; un lecteur qui ne veut que les mots de passe peut la sauter.
- Dans `<account>` *(4.0)* : des éléments enfants facultatifs `<alias>other sign-in name</alias>` (autre identifiant de connexion), placés avant `<fields>` — les autres noms d’utilisateur ou adresses e-mail du compte. La recherche et le remplissage automatique de l’app les reconnaissent ; un lecteur peut les traiter comme des noms d’utilisateur supplémentaires pour le même mot de passe.
- `<wifi>` — les réseaux Wi‑Fi : `<network uuid ssid security password hidden note/>`.
- `<cards>` — `<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>`, plus les attributs d’adresse de facturation préfixés par `b` (`bName`, `bStreet1`, `bCity`…).
- `<identities>` — `<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>` avec des éléments enfants `<email label>`, `<phone label>` et `<address label aStreet1 aCity aRegion aPostal aCountry/>`.
- `<passkeys>` — `<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>` ; les valeurs binaires sont en Base64. Les clés d’accès ne sont écrites **que** dans les sauvegardes chiffrées.
- Des sections de gestion interne que l’app utilise pour elle-même : `<preferences>` (les raccourcis de l’onglet Accueil et, depuis la 4.0, la grille Moi › Mes raccourcis sous forme de `<quickAccess>` / `<quickAccessHidden>`), `<usage>`, `<siteNotes>`, `<checkups>`. Un lecteur qui ne veut que les mots de passe peut les sauter.

Règles pour les lecteurs : les éléments et attributs inconnus sont ignorés ; une section facultative absente signifie « aucun » ; les valeurs `uuid` sont stables d’un export à l’autre, le même compte garde donc le même identifiant ; les dates dans `created` / `updated` / `at` sont des secondes Unix.

Fusion de deux copies *(5.0)* : quand un fichier contient un compte dont l’app possède déjà l’identifiant `uuid`, la **Fusion intelligente** conserve la copie dont la date `updated` est la plus récente et range un mot de passe remplacé dans l’historique de ce compte ; un compte sans `updated` (exporté avant la 5.0) est conservé tel qu’il est sur l’appareil. Une fusion ne supprime jamais rien. Les autres lecteurs sont invités à suivre la même règle.

## La sauvegarde chiffrée : une petite enveloppe autour du même XML

Activez **Chiffrer cette sauvegarde** (ou incluez des clés d’accès) et le même XML est scellé comme suit, tout en big-endian :

1. 8 octets : le nombre magique ASCII `8PWDENC1`.
2. 4 octets : le nombre d’itérations PBKDF2, en entier non signé sur 32 bits — **600 000** quand c’est l’app qui exporte.
3. 16 octets : un sel aléatoire.
4. 12 octets : le nonce AES-256-GCM, suivi du texte chiffré et du tag GCM de 16 octets (la disposition habituelle *nonce ‖ texte chiffré ‖ tag*).

La clé est le **PBKDF2-HMAC-SHA256** du mot de passe de sauvegarde en UTF-8, avec ce sel et ce nombre d’itérations, sur 32 octets. Pas de données associées. Le texte en clair est la sauvegarde en clair décrite ci-dessus, octet pour octet. Les partages (`.8pwdshare`) et les transferts de coffre par AirDrop utilisent la même enveloppe, avec un code à usage unique à 6 chiffres comme mot de passe.

Pas de conteneur propriétaire, pas de séquestre de clé, pas de secret : avec le mot de passe, deux lignes de bibliothèque standard ouvrent le fichier.

## Fichiers d’exemple

Les deux exemples contiennent le même coffre inventé, au format 8 — deux dossiers, trois comptes (dont un avec un alias, et tous avec leurs dates `created` / `updated`), un code à deux facteurs avec ses codes de récupération, un réseau Wi‑Fi, une carte et une identité, plus la section `<links>`, qui relie le code et la carte à leurs comptes. **Toutes les valeurs y sont fictives** ; rien n’appartient à une personne ou à un site réels.

- [sample-plain.8pwd](../../samples/sample-plain.8pwd) — le XML en clair, 3 Ko. Ouvrez-le dans n’importe quel éditeur de texte.
- [sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) — le même coffre scellé avec le mot de passe `example`.

Les deux s’importent dans 8PWD comme n’importe quelle autre sauvegarde (**Moi › Importer › Sauvegarde 8PWD**) ; vous pouvez ainsi voir exactement comment le fichier correspond à ce que montre l’app.

## Vérifier, compter ou déchiffrer un fichier sans l’app

`verify_8pwd.py` est un seul fichier Python 3, dans le domaine public (CC0), sans dépendances pour l’inspection ; le déchiffrement demande le paquet facultatif `cryptography`.

1. `python3 verify_8pwd.py sample-plain.8pwd` — indique si le fichier est en clair ou chiffré, la version du format, la date d’export, combien de comptes, dossiers, codes, réseaux, cartes, identités et clés d’accès il contient (et, depuis la 4.0, d’alias, d’entrées de codes de récupération et de liens), et son SHA-256.
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example` — déchiffre en mémoire et affiche les mêmes compteurs.
3. `python3 verify_8pwd.py Backup.8pwd --json` — une sortie lisible par machine pour vos propres scripts.

Il n’écrit jamais dans le fichier et ne touche jamais au réseau. Lisez-le d’abord ; il est court à dessein.

## Sortir les données sous d’autres formes

- **CSV** : **Moi › Exporter › Exporter un CSV universel** écrit le jeu de colonnes commun (nom, URL, identifiant, mot de passe, note) qu’Apple Passwords, 1Password, Bitwarden et les navigateurs importent tous. L’export fonctionne dans toutes les formules, Pro ou non.
- **Codes à deux facteurs** : chaque `<totp>` est une URI `otpauth://` standard ; l’app les affiche aussi sous forme de codes QR, un à la fois, pour passer à un autre authentificateur.
- **Papier** : le carnet de mots de passe imprimé et le Kit d’urgence sont la solution de repli hors ligne pour vos proches, après vous.

## Licence et promesse

Dans toute la mesure permise par la loi, MNV LIMITED a renoncé à l’ensemble de ses droits d’auteur et droits voisins sur cette spécification de format, selon les termes de la **CC0 1.0 Universal**. Le script de vérification et les fichiers d’exemple sont eux aussi publiés sous **CC0 1.0** ; la mention CC0 figure en tête du script.

Nous n’ajouterons ni conteneur propriétaire, ni clé côté serveur, ni format que seule cette app saurait lire. Si une version future change le format, le numéro de version augmente, les anciens fichiers continuent de s’importer, et le changement est consigné sur cette page et dans les notes de version.

## Voir aussi

- [Vos données sont toujours à vous](https://www.8pwd.com/fr/your-data)
- [Comment le coffre est chiffré](https://www.8pwd.com/fr/encryption)
- [Pourquoi pas de synchronisation — et comment déplacer un coffre](https://www.8pwd.com/fr/why-no-sync)
- [Passer à 8PWD](https://www.8pwd.com/fr/migrate)
