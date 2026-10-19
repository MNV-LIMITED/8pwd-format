# .8pwd 文件格式

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · **简体中文** · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Português (Brasil)](../pt-BR/README.md) · [Italiano](../it/README.md) · [العربية](../ar/README.md) · [Русский](../ru/README.md)

**8PWD** 是 MNV LIMITED 为 iPhone、iPad 和 Mac 开发的离线密码管理器与验证器，这里是它的开放备份格式：明文 XML、可选的 AES-256-GCM 封装、两个示例文件和一个单文件校验脚本——不用 App 也足以读取任何一份备份。

**正式版本**：<https://www.8pwd.com/zh-hans/open-format>。本仓库是它的镜像，由同一来源生成，这样即使不经过我们的网站，也能阅读、引用和核对这个格式。

| 路径 | 说明 |
|---|---|
| [SPEC.md](SPEC.md) | 完整规范：明文 XML 备份、加密封装、读取程序的规则 |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | 明文备份，第 8 版格式（8PWD 5.0）。里面的每个值都是编造的 |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | 同一个密码库，用密码 `example` 加密 |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | 单个 Python 3 文件，可以检查、清点并解密一份备份 |

## 检查文件

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # 仅解密时需要
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

校验脚本绝不改写文件、绝不联网，也绝不打印密码。本次提交中各文件的 SHA-256（`shasum -a 256 -c` 可以直接读取这份清单）：

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## 许可证

这里的一切——规范、示例文件和校验脚本——都依据 **CC0 1.0 通用**（[英文法律文本](../../LICENSE) · [知识共享官方译本](LICENSE.md)）贡献到公有领域。你可以自由编写读取、写入或转换程序，不必征求我们同意、不必署我们的名，也不必付钱给我们。

## 关于 App

App 本身不开源，格式是开放的。[App Store 上的 8PWD](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/zh-hans/)

## 联系我们

本仓库不接受 Issue 或 Pull Request。如有问题或更正，请发邮件至 support@8pwd.com，主题中注明 *Format*。
