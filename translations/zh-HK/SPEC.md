# .8pwd 檔案格式

[English](../../SPEC.md) · **繁體中文** · [简体中文](../zh-Hans/SPEC.md) · [日本語](../ja/SPEC.md) · [한국어](../ko/SPEC.md) · [Deutsch](../de/SPEC.md) · [Français](../fr/SPEC.md) · [Español](../es/SPEC.md) · [Português (Brasil)](../pt-BR/SPEC.md) · [Italiano](../it/SPEC.md) · [العربية](../ar/SPEC.md) · [Русский](../ru/SPEC.md)

> 本文是 [SPEC.md](../../SPEC.md) 的譯本，與 [www.8pwd.com/zh/open-format](https://www.8pwd.com/zh/open-format) 由同一份來源生成。兩者如有出入，以英文版為準。

沒有伺服器，就表示檔案就是一切。所以這個檔案格式是公開的：本頁完整記錄、已釋出到公有領域，並附上範例檔案和一個不用 8PWD 也能跑的校驗腳本。就算我們明天消失，你的密碼仍然是一個讀得懂的檔案。

## 這裡說的「開放」是什麼意思

- **有文件**：App 寫出的每一個元素和屬性都列在本頁，連同讀取程式必須遵守的規則。
- **公有領域**：規格以 **CC0 1.0** 釋出 —— 任何人都可以寫讀取、寫入或轉換工具，不必問我們、不必提我們的名字，也不必付錢給我們。
- **可校驗**：[verify_8pwd.py](../../tools/verify_8pwd.py)（CC0）可以檢查、點算和解密一份備份，除了 Python 3 之外不需要任何依賴。
- **穩定**：版本號只升不降；新區段只會往後追加；讀取程式略過自己不認識的部分。格式的改動都列在[新功能](https://www.8pwd.com/zh/changelog)頁。
- **有鏡像**：本頁、兩個範例檔案和校驗腳本在 [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format)（英文） 都有鏡像，格式的每一次改動在那裡都有公開、註明日期的記錄。

App 本身不是開源的；格式是。對你的資料來說，這才是真正重要的承諾。

## 明文備份：一個 UTF-8 XML 檔案

不設密碼匯出，得到的 `.8pwd` 檔案就是明文 XML。根元素是 `<vault>`，帶有屬性 `app`（產品名稱）、`version`（目前為 **8**）、`exportedAt`（ISO 8601 UTC）、`nodes` 和 `formattedBlocks`（計數）。裡面依次是：

- `<tree>` —— 資料夾和帳戶。`<folder uuid name>` 可以任意嵌套。`<account uuid name favorite icon category created updated>` 放著 `<fields>`，每個 `<field name kind hidden>value</field>` 就是記錄裡的一行。`created` 和 `updated` *(5.0)* 是可選的：記錄建立和最後編輯的時間，以 Unix 秒數表示。
- 欄位的**含義**由它的 `kind` 決定：`username`、`password`、`url`、`email`、`phone`、`note` 或 `text`（自由自訂欄位）。`name` 只是用戶看到的標籤 —— 它是本地化的（「Password」、「密碼」、「Passwort」），不應該用來判斷欄位是什麼。`hidden="true"` 標示 App 預設會遮蔽的欄位。
- `<formattedBlocks>` —— 可重用的文字區塊：`<formattedBlock uuid name recordSeparator>`，內含一個 `<template>` 和 `<accountRefs><ref uuid/></accountRefs>`。
- `<totps>` —— 兩步驗證密鑰，以標準的 `<totp uuid note linkedAccount>otpauth://…</totp>` URI 形式儲存；`linkedAccount` 是它所屬的第一個帳戶的 uuid（為舊版讀取程式保留 —— 完整的多對多關係在 `<links>` 裡，見下文）。任何驗證器 App 都能匯入這個 URI。
- `<recoveryCodes>` *(4.0)* —— 開啟兩步驗證時網站發給你的一次性備用碼；每個驗證碼條目對應一個 `<codes totp="uuid">free text, newlines kept</codes>`（自由文字，保留換行）。它放在 `<totp>` 之外，好讓那個 URI 保持為純粹的 URI。
- `<links>` *(4.0)* —— `<link account="uuid" kind="totp|card|identity" target="uuid"/>`：哪些兩步驗證碼、銀行卡和身份屬於哪些帳戶，多對多。兩端都是同一個檔案裡別處出現的 uuid；只想要密碼的讀取程式可以跳過它。
- `<account>` 裡面 *(4.0)*：`<fields>` 之前可以帶上 `<alias>other sign-in name</alias>` 子元素（可選）—— 即帳戶的其他用戶名或電郵地址。App 的搜尋和自動填充會用它們來匹配；讀取程式可以把它們當成同一條密碼的額外用戶名。
- `<wifi>` —— `<network uuid ssid security password hidden note/>`。
- `<cards>` —— `<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>`，另加以 `b` 開頭的賬單地址屬性（`bName`、`bStreet1`、`bCity`…）。
- `<identities>` —— `<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>`，子元素為 `<email label>`、`<phone label>` 和 `<address label aStreet1 aCity aRegion aPostal aCountry/>`。
- `<passkeys>` —— `<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>`；二進位值以 Base64 編碼。通行密鑰**只會**寫進加密備份。
- App 自用的內務區段：`<preferences>`（首頁捷徑，以及從 4.0 起以 `<quickAccess>` / `<quickAccessHidden>` 記錄的「我 › 我的常用」格子）、`<usage>`、`<siteNotes>`、`<checkups>`。只想要密碼的讀取程式可以跳過它們。

給讀取程式的規則：不認識的元素和屬性一律略過；可選區段缺席就表示「沒有」；`uuid` 的值在每次匯出之間保持不變，所以同一個帳戶永遠是同一個 id；`created` / `updated` / `at` 裡的日期是 Unix 秒數。

合併兩份副本 *(5.0)*：檔案裡的帳戶如果 `uuid` 與 App 裡已有的相同，**智能合併**會保留 `updated` 時間較晚的那份，並把被換掉的密碼記入該帳戶的密碼歷史；沒有 `updated` 的帳戶（5.0 之前匯出的）則保留裝置上原有的那份。合併永遠不會刪除任何東西。歡迎其它讀取程式採用同一規則。

## 加密備份：同一份 XML 外面的一層小封裝

開啟**加密這份備份**（或者備份裡含通行密鑰），同一份 XML 就會按下面的方式封起來，全部採用大端序：

1. 8 個位元組的 ASCII 標識 `8PWDENC1`。
2. 4 個位元組：PBKDF2 迭代次數，無符號 32 位元整數 —— App 匯出時為 **600,000**。
3. 16 個位元組：隨機 salt。
4. 12 個位元組：AES-256-GCM 的 nonce，後面接著密文和 16 個位元組的 GCM 標籤（即常見的 *nonce ‖ ciphertext ‖ tag* 排列）。

鑰匙是以 UTF-8 備份密碼、該 salt 和該迭代次數算出的 **PBKDF2-HMAC-SHA256**，長 32 個位元組。沒有附加資料（associated data）。明文就是上面的明文備份，一個位元組都不差。分享（`.8pwdshare`）和 AirDrop 密碼庫傳送使用同一套封裝，以一次性的 6 位數字代碼作為密碼。

沒有專有容器、沒有密鑰託管、沒有任何秘密：有了密碼，兩行標準程式庫的程式碼就能打開這個檔案。

## 範例檔案

兩個範例裝的是同一個以第 8 版格式寫成的虛構密碼庫 —— 兩個資料夾、三個帳戶（其中一個帶別名，每個都有 `created` / `updated` 時間）、一個附恢復碼的兩步驗證碼、一個 Wi-Fi 網絡、一張銀行卡和一個身份，另加 `<links>` 區段，把這個驗證碼和這張卡關聯到各自的帳戶。**裡面每一個值都是編出來的**；沒有任何一項屬於真實的人或網站。

- [sample-plain.8pwd](../../samples/sample-plain.8pwd) —— 明文 XML，3 KB。用任何文字編輯器都打得開。
- [sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) —— 同一個密碼庫，以密碼 `example` 封裝。

兩個檔案都可以像普通備份一樣匯入 8PWD（**「我」› 匯入 › 8PWD 備份**），讓你清楚看到檔案裡的每一項對應到 App 的哪裡。

## 不用 App 也能檢查、點算或解密檔案

`verify_8pwd.py` 是一個單檔 Python 3 腳本，屬公有領域（CC0），檢查時不需要任何依賴；解密則需要可選的 `cryptography` 套件。

1. `python3 verify_8pwd.py sample-plain.8pwd` —— 告訴你檔案是明文還是加密、格式版本、匯出日期、裡面有多少帳戶、資料夾、驗證碼、網絡、銀行卡、身份和通行密鑰（從 4.0 起還有別名、恢復碼條目和關聯），以及它的 SHA-256。
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example` —— 在記憶體中解密，並印出同樣的計數。
3. `python3 verify_8pwd.py Backup.8pwd --json` —— 機器可讀的輸出，給你自己的腳本用。

它永遠不會寫入檔案，也永遠不會碰網絡。先讀一讀它；它刻意寫得很短。

## 用其它形式把資料拿出來

- **CSV**：**「我」› 匯出 › 匯出通用 CSV** 會寫出 Apple 密碼、1Password、Bitwarden 和各家瀏覽器都能匯入的常用欄位組合（名稱、網址、用戶名稱、密碼、備註）。每個方案都能匯出，無論是否 Pro。
- **兩步驗證碼**：每個 `<totp>` 都是標準的 `otpauth://` URI；App 也能把它們逐一顯示成二維碼，方便搬到另一個驗證器 App。
- **紙本**：列印出來的密碼本和緊急工具包，是留給你身後親人的離線後備。

## 授權與承諾

在法律允許的最大範圍內，MNV LIMITED 已依據 **CC0 1.0 Universal** 放棄本格式規格的所有版權及相關權利。校驗腳本和範例檔案同樣以 **CC0 1.0** 釋出；相關聲明在腳本開頭。

我們不會加入專有容器、放在伺服器端的鑰匙，或者只有這個 App 才讀得懂的格式。如果將來的版本改動了格式，版本號會升高、舊檔案照樣能匯入，而且改動會寫在本頁和版本更新說明裡。

## 延伸閱讀

- [你的資料永遠屬於你](https://www.8pwd.com/zh/your-data)
- [密碼庫如何加密](https://www.8pwd.com/zh/encryption)
- [為什麼不同步 —— 以及怎樣搬密碼庫](https://www.8pwd.com/zh/why-no-sync)
- [轉用 8PWD](https://www.8pwd.com/zh/migrate)
