# .8pwd 文件格式

[English](../../SPEC.md) · [繁體中文](../zh-HK/SPEC.md) · **简体中文** · [日本語](../ja/SPEC.md) · [한국어](../ko/SPEC.md) · [Deutsch](../de/SPEC.md) · [Français](../fr/SPEC.md) · [Español](../es/SPEC.md) · [Português (Brasil)](../pt-BR/SPEC.md) · [Italiano](../it/SPEC.md) · [العربية](../ar/SPEC.md) · [Русский](../ru/SPEC.md)

> 本文是 [SPEC.md](../../SPEC.md) 的译文，与 [www.8pwd.com/zh-hans/open-format](https://www.8pwd.com/zh-hans/open-format) 由同一来源生成。两者如有出入，以英文版为准。

没有服务器，意味着这个文件就是一切。所以文件格式是公开的：在这一页完整写明，进入公有领域，并附带示例文件和一个不用 8PWD 也能运行的校验脚本。就算我们明天消失了，你的密码仍然是一个读得懂的文件。

## 这里的“开放”指什么

- **有文档**：App 写出的每个元素和属性都列在本页，连同读取程序必须遵守的规则。
- **公有领域**：规范以 **CC0 1.0** 发布——任何人都可以编写读取、写入或转换程序，不必征求我们同意、不必署我们的名、也不必付钱给我们。
- **可验证**：[verify_8pwd.py](../../tools/verify_8pwd.py)（CC0）可以检查、清点并解密一份备份，除 Python 3 外不需要任何依赖。
- **稳定**：版本号只增不减；新的部分只会追加在后面；读取程序忽略它不认识的内容。格式变动都列在[新功能](https://www.8pwd.com/zh-hans/changelog)页面。
- **有镜像**：本页、两个示例文件和校验脚本在 [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format)（英文） 上都有镜像，格式的每一次改动在那里都留有公开、注明日期的历史记录。

App 本身不开源，格式是开放的。对你的数据而言，这才是真正重要的承诺。

## 明文备份：一个 UTF-8 XML 文件

不设密码导出，得到的就是一个明文 XML 的 `.8pwd` 文件。根元素是 `<vault>`，带属性 `app`（产品名）、`version`（目前为 **8**）、`exportedAt`（ISO 8601 UTC）、`nodes` 和 `formattedBlocks`（数量）。里面依次是：

- `<tree>`——文件夹和账户。`<folder uuid name>` 可以任意嵌套。`<account uuid name favorite icon category created updated>` 装着 `<fields>`，每个 `<field name kind hidden>value</field>` 是记录里的一行。`created` 和 `updated` *（5.0）* 是可选的：记录的创建时间和最后一次编辑时间，单位为 Unix 秒。
- 字段的**含义**由它的 `kind` 决定：`username`、`password`、`url`、`email`、`phone`、`note` 或 `text`（自定义字段）。`name` 只是用户看到的标签——它是本地化的（“Password”、“密碼”、“Passwort”），不应该用来判断字段是什么。`hidden="true"` 标记 App 默认会遮住的字段。
- `<formattedBlocks>`——可复用的文本块：`<formattedBlock uuid name recordSeparator>`，内含一个 `<template>` 和 `<accountRefs><ref uuid/></accountRefs>`。
- `<totps>`——双重认证密钥，以标准的 `<totp uuid note linkedAccount>otpauth://…</totp>` URI 形式保存；`linkedAccount` 是它所属的第一个账户的 uuid（为兼容旧版读取程序而保留——完整的多对多关系在 `<links>` 里，见下文）。任何验证器都能导入这个 URI。
- `<recoveryCodes>` *（4.0）*——开启双重认证时网站给出的一次性备用码，每个验证码条目对应一个 `<codes totp="uuid">free text, newlines kept</codes>`（内容是自由文本，换行原样保留）。它单独放在 `<totp>` 之外，好让 URI 保持为纯粹的 URI。
- `<links>` *（4.0）*——`<link account="uuid" kind="totp|card|identity" target="uuid"/>`：记录哪些双重认证验证码、银行卡和身份属于哪些账户，多对多。两端都是同一文件中别处出现的 uuid；只想要密码的读取程序可以跳过它。
- `<account>` 内部 *（4.0）*：`<fields>` 之前可选的若干 `<alias>other sign-in name</alias>` 子元素——即该账户的其他用户名或邮箱地址。App 里的搜索和自动填充会匹配它们；读取程序可以把它们视为同一密码的额外用户名。
- `<wifi>`——`<network uuid ssid security password hidden note/>`。
- `<cards>`——`<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>`，外加以 `b` 开头的账单地址属性（`bName`、`bStreet1`、`bCity`……）。
- `<identities>`——`<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>`，带子元素 `<email label>`、`<phone label>` 和 `<address label aStreet1 aCity aRegion aPostal aCountry/>`。
- `<passkeys>`——`<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>`；二进制值以 Base64 编码。通行密钥**只会**被写进加密备份。
- App 自用的内务部分：`<preferences>`（首页快捷方式，以及从 4.0 起的“我 › 我的常用”网格，保存为 `<quickAccess>` / `<quickAccessHidden>`）、`<usage>`、`<siteNotes>`、`<checkups>`。只想要密码的读取程序可以跳过它们。

读取程序的规则：不认识的元素和属性一律忽略；缺少的可选部分表示“没有”；`uuid` 在多次导出之间保持不变，所以同一个账户始终是同一个 id；`created` / `updated` / `at` 里的日期是 Unix 秒数。

合并两份副本 *（5.0）*：当文件中某个账户的 `uuid` 在 App 里已经存在时，**智能合并**会保留 `updated` 时间较晚的那份，并把被替换的密码归入该账户的密码历史；没有 `updated` 的账户（5.0 之前导出的）则保留设备上原来的样子。合并绝不会删除任何东西。欢迎其他读取程序遵循同样的规则。

## 加密备份：同一份 XML 外面的一层小封装

开启**加密此备份**（或包含通行密钥）后，同一份 XML 会按如下方式封存，全部为大端序：

1. 8 个字节的 ASCII 魔数 `8PWDENC1`。
2. 4 个字节：PBKDF2 迭代次数，无符号 32 位整数——App 导出时为 **600,000**。
3. 16 个字节：随机盐。
4. 12 个字节：AES-256-GCM 的 nonce，后面是密文和 16 字节的 GCM 标签（常见的 *nonce ‖ ciphertext ‖ tag* 布局）。

密钥是备份密码（UTF-8）配合上述盐和迭代次数算出的 **PBKDF2-HMAC-SHA256**，长 32 字节。没有附加认证数据。明文就是上面的明文备份，逐字节一致。分享（`.8pwdshare`）和 AirDrop 密码库传输使用同样的封装，以 6 位一次性验证码作为密码。

没有私有容器，没有密钥托管，也没有秘密：有了密码，两行标准库代码就能打开这个文件。

## 示例文件

两个示例装的是同一个虚构的、第 8 版格式的密码库——两个文件夹、三个账户（其中一个带别名，每个都带 `created` / `updated` 时间）、一个带恢复码的双重认证验证码、一个 Wi-Fi 网络、一张银行卡和一个身份，外加 `<links>` 部分，把这个验证码和这张银行卡关联到各自的账户。**里面的每个值都是编造的**，不属于任何真实的人或网站。

- [sample-plain.8pwd](../../samples/sample-plain.8pwd)——明文 XML，3 KB。用任何文本编辑器都能打开。
- [sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd)——同一个密码库，用密码 `example` 封存。

两个文件都可以像普通备份一样导入 8PWD（**我 › 导入 › 8PWD 备份**），你可以亲眼看到文件里的内容如何对应到 App 中。

## 不用 App 也能检查、清点或解密文件

`verify_8pwd.py` 是单个 Python 3 文件，属于公有领域（CC0），检查时不需要任何依赖；解密需要可选的 `cryptography` 包。

1. `python3 verify_8pwd.py sample-plain.8pwd`——告诉你文件是明文还是加密的、格式版本、导出日期、里面有多少账户、文件夹、验证码、网络、银行卡、身份和通行密钥（从 4.0 起还有别名、恢复码条目和关联记录），以及它的 SHA-256。
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example`——在内存中解密，并打印同样的数量。
3. `python3 verify_8pwd.py Backup.8pwd --json`——机器可读的输出，供你自己的脚本使用。

它绝不改写文件，也绝不联网。先读一读它的代码；它故意写得很短。

## 用其他形式把数据带走

- **CSV**：**我 › 导出 › 导出通用 CSV** 会写出通用的列（名称、网址、用户名、密码、备注），Apple Passwords、1Password、Bitwarden 和各家浏览器都能导入。所有方案都能导出，不管是不是 Pro。
- **双重认证验证码**：每个 `<totp>` 都是标准的 `otpauth://` URI；App 也能把它们逐个显示为二维码，方便搬到另一个验证器。
- **纸质**：打印密码本和紧急工具包是留给你身后家人的离线后备。

## 许可证与承诺

在法律允许的最大范围内，MNV LIMITED 已依据 **CC0 1.0 通用**放弃本格式规范的全部著作权及相关权利。校验脚本和示例文件同样以 **CC0 1.0** 发布；相关声明写在脚本开头。

我们不会加入私有容器、服务器端密钥，或只有这个 App 才能读的格式。如果将来某个版本改动了格式，版本号会增加，旧文件仍然可以导入，而改动会写在本页和更新说明里。

## 延伸阅读

- [你的数据永远属于你](https://www.8pwd.com/zh-hans/your-data)
- [密码库如何加密](https://www.8pwd.com/zh-hans/encryption)
- [为什么不同步——以及怎么搬移密码库](https://www.8pwd.com/zh-hans/why-no-sync)
- [迁移到 8PWD](https://www.8pwd.com/zh-hans/migrate)
