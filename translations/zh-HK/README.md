# .8pwd 檔案格式

[English](../../README.md) · **繁體中文** · [简体中文](../zh-Hans/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Português (Brasil)](../pt-BR/README.md) · [Italiano](../it/README.md) · [العربية](../ar/README.md) · [Русский](../ru/README.md)

**8PWD** 是 MNV LIMITED 為 iPhone、iPad 與 Mac 開發的離線密碼管理器與驗證器，這裡是它的開放備份格式：明文 XML、一層可選的 AES-256-GCM 封裝、兩個範例檔案和一個單檔校驗腳本 —— 不用 App 也足以讀懂任何一份備份。

**正式版本**：<https://www.8pwd.com/zh/open-format>。本儲存庫是它的鏡像，由同一份來源生成，好讓這個格式不靠我們的網站也能閱讀、引用和核對。

| 路徑 | 說明 |
|---|---|
| [SPEC.md](SPEC.md) | 完整規格：明文 XML 備份、加密封裝、給讀取程式的規則 |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | 明文備份，第 8 版格式（8PWD 5.0）。裡面每一個值都是編出來的 |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | 同一個密碼庫，以密碼 `example` 加密 |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | 一個單檔 Python 3 腳本，可以檢查、點算和解密一份備份 |

## 檢查檔案

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # 只有解密時才需要
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

校驗腳本永遠不會寫入檔案、永遠不會碰網絡，也永遠不會印出密碼。本次提交中各檔案的 SHA-256（`shasum -a 256 -c` 可以直接讀取這份清單）：

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## 授權

這裡的一切 —— 規格、範例檔案和校驗腳本 —— 都依據 **CC0 1.0 通用**（[英文法律文本](../../LICENSE) · [Creative Commons 官方譯本](LICENSE.md)）貢獻到公有領域。你可以自由編寫讀取、寫入或轉換工具，不必問我們、不必提我們的名字，也不必付錢給我們。

## 關於 App

App 本身不是開源的；格式是。[App Store 上的 8PWD](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/zh/)

## 聯絡我們

本儲存庫不接受 Issue 或 Pull Request。如有問題或更正，請電郵 support@8pwd.com，主旨註明 *Format*。
