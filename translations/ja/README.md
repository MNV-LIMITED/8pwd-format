# .8pwd ファイル形式

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · [简体中文](../zh-Hans/README.md) · **日本語** · [한국어](../ko/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Português (Brasil)](../pt-BR/README.md) · [Italiano](../it/README.md) · [العربية](../ar/README.md) · [Русский](../ru/README.md)

**8PWD** は、MNV LIMITED が iPhone、iPad、Mac 向けに開発したオフラインのパスワード管理・認証アプリです。このリポジトリにあるのは、そのオープンなバックアップ形式です。平文の XML、AES-256-GCM の封筒形式（任意）、2つのサンプルファイル、ファイル1つで完結する検証ツールがそろっていて、Appがなくてもどのバックアップでも読めます。

**正本**：<https://www.8pwd.com/ja/open-format>。このリポジトリはそのミラーで、同じソースから生成しています。私たちのウェブサイトがなくても、この形式を読み、引用し、確かめられるようにするためです。

| パス | 説明 |
|---|---|
| [SPEC.md](SPEC.md) | 仕様の全文：平文の XML バックアップ、暗号化の封筒形式、リーダーのためのルール |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | 平文バックアップ。形式はバージョン 8（8PWD 5.0）で、中の値はすべて作りもの |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | 同じ保管庫を、パスワード `example` で暗号化したもの |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | バックアップの内容を調べ、件数を数え、復号する Python 3 のファイル1つ |

## ファイルを確かめる

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # 復号するときだけ必要
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

検証ツールは、ファイルに書き込むことも、ネットワークを使うことも、パスワードを表示することも決してありません。このコミットに含まれるファイルの SHA-256（この一覧は `shasum -a 256 -c` でそのまま検証できます）：

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## ライセンス

仕様、サンプルファイル、検証ツールを含め、ここにあるものはすべて **CC0 1.0 全世界**（[英語のリーガルコード](../../LICENSE) · [クリエイティブ・コモンズによる公式翻訳](LICENSE.md)）のもとでパブリックドメインに提供しています。私たちに許可を求めることも、名前を記すことも、料金を払うこともなく、リーダー、ライター、変換ツールを自由に作ってください。

## Appについて

App自体はオープンソースではありませんが、形式はオープンです。[App Store の 8PWD](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/ja/)

## お問い合わせ

このリポジトリでは Issue やプルリクエストを受け付けていません。質問や訂正は、件名に *Format* と入れて support@8pwd.com にメールしてください。
