# .8pwd ファイル形式

[English](../../SPEC.md) · [繁體中文](../zh-HK/SPEC.md) · [简体中文](../zh-Hans/SPEC.md) · **日本語** · [한국어](../ko/SPEC.md) · [Deutsch](../de/SPEC.md) · [Français](../fr/SPEC.md) · [Español](../es/SPEC.md) · [Português (Brasil)](../pt-BR/SPEC.md) · [Italiano](../it/SPEC.md) · [العربية](../ar/SPEC.md) · [Русский](../ru/SPEC.md)

> この文書は [SPEC.md](../../SPEC.md) の翻訳で、[www.8pwd.com/ja/open-format](https://www.8pwd.com/ja/open-format) と同じソースから生成しています。両者に違いがある場合は、英語版が優先します。

サーバがないということは、ファイルがすべてだということです。だからファイル形式は公開されています。このページに全文を記載し、パブリックドメインとして公開し、サンプルファイルと、8PWD なしで実行できる検証ツールを添えています。私たちが明日いなくなっても、あなたのパスワードは読めるファイルのまま残ります。

## ここでいう「オープン」の意味

- **文書化**：Appが書き出すすべての要素と属性を、読み手が従うべきルールとともにこのページに掲載しています。
- **パブリックドメイン**：仕様は **CC0 1.0** で公開しています。誰でも、私たちに許可を求めることも、名前を記すことも、料金を払うこともなく、リーダー、ライター、変換ツールを作れます。
- **検証可能**：[verify_8pwd.py](../../tools/verify_8pwd.py)（CC0）は、Python 3 以外に依存するものなしで、バックアップの内容を調べ、件数を数え、復号します。
- **安定**：バージョン番号は上がるだけ、新しいセクションは末尾に追加されるだけで、リーダーは知らないものを無視します。形式の変更は[新機能](https://www.8pwd.com/ja/changelog)ページに記載します。
- **ミラー公開**：このページ、2つのサンプルファイル、検証ツールを [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format)（英語） にミラーしています。そこでは、形式に加えたすべての変更が、日付付きの履歴として公開されています。

App自体はオープンソースではありませんが、形式はオープンです。あなたのデータにとって大事なのは、この約束です。

## 平文バックアップ：1つの UTF-8 XML ファイル

パスワードなしで書き出すと、平文の XML である `.8pwd` ファイルが得られます。ルート要素は `<vault>` で、属性として `app`（製品名）、`version`（現在は **8**）、`exportedAt`（ISO 8601、UTC）、`nodes` と `formattedBlocks`（件数）を持ちます。その中には、次の順で入っています：

- `<tree>` — フォルダとアカウント。`<folder uuid name>` は自由に入れ子にできます。`<account uuid name favorite icon category created updated>` は `<fields>` を持ち、その中の `<field name kind hidden>value</field>` の1つひとつがレコードの1行です。`created` と `updated` *(5.0)* は任意で、そのレコードが作成された日時と最後に編集された日時を Unix 秒で表します。
- フィールドの**意味**を決めるのは `kind` です：`username`、`password`、`url`、`email`、`phone`、`note`、または `text`（自由なカスタムフィールド）。`name` はユーザに見えるラベルにすぎず、ローカライズされている（“Password”、“密碼”、“Passwort”）ので、フィールドが何かを判断するのに使ってはいけません。`hidden="true"` は、Appがデフォルトで隠して表示するフィールドを示します。
- `<formattedBlocks>` — 再利用できるテキストブロック：`<formattedBlock uuid name recordSeparator>` が `<template>` と `<accountRefs><ref uuid/></accountRefs>` を持ちます。
- `<totps>` — 2要素認証のシークレット。標準の `<totp uuid note linkedAccount>otpauth://…</totp>` URI として保存され、`linkedAccount` は所属する最初のアカウントの uuid です（古いリーダーのために残しているもので、多対多の完全な対応は後述の `<links>` にあります）。この URI はどの認証アプリでも読み込めます。
- `<recoveryCodes>` *(4.0)* — 2要素認証を設定したときにサイトが発行する使い捨てのバックアップコード。2要素認証コード1件につき `<codes totp="uuid">free text, newlines kept</codes>` を1つ置き、中身は改行を保ったままの自由テキストです。URI を純粋な URI のまま保つため、`<totp>` の外に置いています。
- `<links>` *(4.0)* — `<link account="uuid" kind="totp|card|identity" target="uuid"/>`：どの2要素認証コード、カード、個人情報がどのアカウントに属するかを多対多で表します。両端はどちらも同じファイル内のほかの場所にある uuid です。パスワードだけが必要なリーダーは読み飛ばしてかまいません。
- `<account>` の中 *(4.0)*：`<fields>` の前に、任意の子要素 `<alias>other sign-in name</alias>` を置けます。そのアカウントの別のユーザ名やメールアドレス（エイリアス）です。Appの検索と自動入力はこれにも一致します。リーダーは、同じパスワードに対する追加のユーザ名として扱ってかまいません。
- `<wifi>` — `<network uuid ssid security password hidden note/>`。
- `<cards>` — `<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>` に加えて、`b` で始まる請求先住所の属性（`bName`、`bStreet1`、`bCity`…）。
- `<identities>` — `<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>` と、その子要素 `<email label>`、`<phone label>`、`<address label aStreet1 aCity aRegion aPostal aCountry/>`。
- `<passkeys>` — `<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>`。バイナリ値は Base64 です。パスキーは暗号化バックアップに**のみ**書き込まれます。
- App自身が使う管理用のセクション：`<preferences>`（ホームのショートカットと、4.0 からは「マイページ」›「マイショートカット」のグリッドを `<quickAccess>` / `<quickAccessHidden>` として保存）、`<usage>`、`<siteNotes>`、`<checkups>`。パスワードだけが必要なリーダーは読み飛ばしてかまいません。

リーダーのためのルール：知らない要素と属性は無視する。任意のセクションがなければ「なし」とみなす。`uuid` の値は書き出しをまたいでも変わらないので、同じアカウントは同じ id を保つ。`created` / `updated` / `at` の日時は Unix 秒。

2つのコピーの統合 *(5.0)*：Appがすでに持っている `uuid` のアカウントがファイルに含まれている場合、**スマート統合**は `updated` の時刻が新しい方を残し、置き換えられたパスワードはそのアカウントの履歴に入れます。`updated` のないアカウント（5.0 より前に書き出されたもの）は、デバイス上のものがそのまま残ります。統合で何かが削除されることはありません。ほかのリーダーも同じルールに従ってかまいません。

## 暗号化バックアップ：同じ XML を包む小さな封筒

<strong>「このバックアップを暗号化」</strong>をオンにする（またはパスキーを含める）と、同じ XML が次のように封印されます。すべてビッグエンディアンです。

1. 8 バイトの ASCII マジック `8PWDENC1`。
2. 4 バイト：PBKDF2 の反復回数（符号なし 32 ビット整数）。Appが書き出すときは **600,000**。
3. 16 バイト：ランダムなソルト。
4. 12 バイト：AES-256-GCM のノンス。続いて暗号文と 16 バイトの GCM タグ（よくある *nonce ‖ ciphertext ‖ tag* の並び）。

鍵は、UTF-8 のバックアップパスワードからそのソルトと反復回数で導出した **PBKDF2-HMAC-SHA256** で、長さは 32 バイトです。関連データ（associated data）はありません。平文は上の平文バックアップそのもので、1バイトも違いません。共有（`.8pwdshare`）と AirDrop による保管庫の転送も同じ封筒形式を使い、パスワードには6桁のワンタイムコードを使います。

独自のコンテナも、鍵の預託も、秘密もありません。パスワードさえあれば、標準ライブラリの2行のコードでファイルが開きます。

## サンプルファイル

2つのサンプルには、バージョン 8 の形式で同じ架空の保管庫が入っています。フォルダ2つ、アカウント3つ（うち1つはエイリアス付きで、どれにも `created` / `updated` の日時があります）、復旧コード付きの2要素認証コード1つ、Wi-Fi ネットワーク1つ、カード1枚、個人情報1件、そしてそのコードとカードをそれぞれのアカウントに結び付ける `<links>` セクションです。**中の値はすべて作りもの**で、実在の人物やサイトのものは1つもありません。

- [sample-plain.8pwd](../../samples/sample-plain.8pwd) — 平文の XML、3 KB。どのテキストエディタでも開けます。
- [sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) — 同じ保管庫をパスワード `example` で封印したもの。

どちらもほかのバックアップと同じように 8PWD に読み込めます（**「マイページ」›「読み込み」›「8PWD バックアップ」**）。ファイルの中身がAppのどこに対応するのかを、そのまま確かめられます。

## Appなしでファイルを確かめる・数える・復号する

`verify_8pwd.py` は Python 3 のファイル1つで、パブリックドメイン（CC0）です。内容を調べるだけなら依存パッケージは不要で、復号にはオプションの `cryptography` パッケージが必要です。

1. `python3 verify_8pwd.py sample-plain.8pwd` — ファイルが平文か暗号化か、形式のバージョン、書き出し日、含まれるアカウント、フォルダ、コード、ネットワーク、カード、個人情報、パスキーの件数（4.0 からはエイリアス、復旧コードのエントリ、リンクの件数も）、そして SHA-256 を表示します。
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example` — メモリ上で復号し、同じ件数を表示します。
3. `python3 verify_8pwd.py Backup.8pwd --json` — 自分のスクリプトで使える、機械可読の出力。

ファイルに書き込むことも、ネットワークに触れることも決してありません。まず中身を読んでください。わざと短くしてあります。

## ほかの形でデータを取り出す

- **CSV**：<strong>「マイページ」›「書き出し」›「汎用 CSV を書き出す」</strong>は、Apple Passwords、1Password、Bitwarden、各ブラウザのどれもが読み込める共通の列（名前、URL、ユーザ名、パスワード、メモ）を書き出します。書き出しは Pro かどうかにかかわらず、すべてのプランで使えます。
- **2要素認証コード**：各 `<totp>` は標準の `otpauth://` URI です。ほかの認証アプリへ移せるように、Appは1つずつ QR コードとしても表示します。
- **紙**：紙のパスワード帳と緊急キットは、あなたが残していく人たちのための、オフラインの備えです。

## ライセンスと約束

MNV LIMITED は、法律で認められる範囲で、この形式仕様に関するすべての著作権および関連する権利を **CC0 1.0 Universal** のもとで放棄しています。検証スクリプトとサンプルファイルも **CC0 1.0** で公開しており、その旨の表示はスクリプトの先頭にあります。

独自のコンテナも、サーバ側の鍵も、このAppだけが読める形式も、今後追加することはありません。将来のバージョンで形式が変わる場合は、バージョン番号を上げ、古いファイルは引き続き読み込めるようにし、変更内容をこのページとリリースノートに記載します。

## 関連ページ

- [データはいつでもあなたのもの](https://www.8pwd.com/ja/your-data)
- [保管庫はどう暗号化されているか](https://www.8pwd.com/ja/encryption)
- [同期しない理由 — 保管庫の移し方](https://www.8pwd.com/ja/why-no-sync)
- [8PWD への乗り換え](https://www.8pwd.com/ja/migrate)
