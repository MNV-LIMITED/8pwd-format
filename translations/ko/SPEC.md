# .8pwd 파일 형식

[English](../../SPEC.md) · [繁體中文](../zh-HK/SPEC.md) · [简体中文](../zh-Hans/SPEC.md) · [日本語](../ja/SPEC.md) · **한국어** · [Deutsch](../de/SPEC.md) · [Français](../fr/SPEC.md) · [Español](../es/SPEC.md) · [Português (Brasil)](../pt-BR/SPEC.md) · [Italiano](../it/SPEC.md) · [العربية](../ar/SPEC.md) · [Русский](../ru/SPEC.md)

> [SPEC.md](../../SPEC.md)의 번역으로, [www.8pwd.com/ko/open-format](https://www.8pwd.com/ko/open-format) 페이지와 같은 소스에서 생성했습니다. 두 문서의 내용이 다를 경우 영어 버전이 우선합니다.

서버가 없다는 것은 파일이 전부라는 뜻입니다. 그래서 파일 형식을 공개합니다. 이 페이지에 빠짐없이 문서화했고, 퍼블릭 도메인으로 내놓았으며, 샘플 파일과 8PWD 없이 실행할 수 있는 검증 도구를 함께 제공합니다. 저희가 내일 사라져도 비밀번호는 여전히 읽을 수 있는 파일로 남습니다.

## 여기서 말하는 “공개”의 의미

- **문서화**: 앱이 기록하는 모든 요소와 속성을 이 페이지에 나열했고, 읽는 쪽이 따라야 할 규칙도 함께 적었습니다.
- **퍼블릭 도메인**: 이 사양은 **CC0 1.0**으로 공개됩니다. 누구나 저희에게 묻지 않고, 저희 이름을 밝히지 않고, 비용을 내지 않고도 리더, 라이터, 변환기를 만들 수 있습니다.
- **검증 가능**: [verify_8pwd.py](../../tools/verify_8pwd.py)(CC0)는 Python 3 외의 의존성 없이 백업을 검사하고, 개수를 세고, 복호화합니다.
- **안정적**: 버전 번호는 올라가기만 하고, 새 섹션은 뒤에 덧붙기만 하며, 리더는 모르는 것을 무시합니다. 형식 변경 사항은 [새로운 기능](https://www.8pwd.com/ko/changelog) 페이지에 적습니다.
- **미러링**: 이 페이지와 두 샘플 파일, 검증 도구는 [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format)(영문)에 미러링되어 있으며, 그곳에는 형식에 대한 모든 변경이 날짜와 함께 공개 이력으로 남습니다.

앱 자체는 오픈 소스가 아니지만, 형식은 공개되어 있습니다. 내 데이터에 정말 중요한 약속은 바로 이것입니다.

## 일반 백업: UTF-8 XML 파일 하나

비밀번호 없이 내보내면 일반 XML인 `.8pwd` 파일이 만들어집니다. 루트 요소는 `<vault>`이며 속성으로 `app`(제품 이름), `version`(현재 **8**), `exportedAt`(ISO 8601 UTC), `nodes`와 `formattedBlocks`(개수)를 갖습니다. 그 안에는 다음 순서로 들어 있습니다:

- `<tree>` — 폴더와 계정. `<folder uuid name>`은 자유롭게 중첩됩니다. `<account uuid name favorite icon category created updated>`는 `<fields>`를 담고, 각 `<field name kind hidden>value</field>`가 기록의 한 줄입니다. `created`와 `updated` *(5.0)*는 선택 사항으로, 기록이 만들어진 시각과 마지막으로 수정된 시각을 Unix 초 단위로 나타냅니다.
- 필드의 **의미**는 `kind`가 정합니다: `username`, `password`, `url`, `email`, `phone`, `note` 또는 `text`(자유 사용자 정의 필드). `name`은 사용자에게 보이는 라벨일 뿐이며, 언어에 따라 달라지므로(“Password”, “密碼”, “Passwort”) 필드가 무엇인지 판단하는 데 쓰면 안 됩니다. `hidden="true"`는 앱이 기본으로 가리는 필드를 표시합니다.
- `<formattedBlocks>` — 재사용 가능한 텍스트 블록: `<template>`과 `<accountRefs><ref uuid/></accountRefs>`를 가진 `<formattedBlock uuid name recordSeparator>`.
- `<totps>` — 2단계 인증 시크릿을 표준 `<totp uuid note linkedAccount>otpauth://…</totp>` URI로 담습니다. `linkedAccount`는 코드가 속한 첫 번째 계정의 uuid입니다(예전 리더를 위해 유지되며, 다대다 연결 전체는 아래에 설명하는 `<links>`에 있습니다). 어떤 인증 앱이든 이 URI를 가져올 수 있습니다.
- `<recoveryCodes>` *(4.0)* — 2단계 인증을 설정할 때 사이트가 주는 일회용 백업 코드로, 코드 항목마다 `<codes totp="uuid">free text, newlines kept</codes>` 하나씩입니다. URI가 순수한 URI로 남도록 `<totp>` 바깥에 둡니다.
- `<links>` *(4.0)* — `<link account="uuid" kind="totp|card|identity" target="uuid"/>`: 어떤 2단계 인증 코드, 카드, 신원 정보가 어떤 계정에 속하는지를 다대다로 나타냅니다. 양쪽 끝은 모두 같은 파일의 다른 곳에 있는 uuid입니다. 비밀번호만 필요한 리더는 건너뛰어도 됩니다.
- `<account>` 내부 *(4.0)*: `<fields>` 앞에 올 수 있는 선택적 자식 요소 `<alias>other sign-in name</alias>` — 계정의 다른 사용자 이름이나 이메일 주소입니다. 앱의 검색과 자동 완성은 별칭에도 일치합니다. 리더는 이를 같은 비밀번호에 딸린 추가 사용자 이름으로 다뤄도 됩니다.
- `<wifi>` — Wi-Fi 네트워크: `<network uuid ssid security password hidden note/>`.
- `<cards>` — `<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>`에 접두사 `b`가 붙은 청구지 주소 속성(`bName`, `bStreet1`, `bCity`…)이 더해집니다.
- `<identities>` — `<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>`에 자식 요소 `<email label>`, `<phone label>`, `<address label aStreet1 aCity aRegion aPostal aCountry/>`가 들어 있습니다.
- `<passkeys>` — `<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>`. 이진 값은 Base64입니다. 패스키는 **오직** 암호화된 백업에만 기록됩니다.
- 앱이 내부용으로 쓰는 관리 섹션: `<preferences>`(홈 바로 가기, 그리고 4.0부터는 `<quickAccess>` / `<quickAccessHidden>`으로 저장되는 나 › 내 바로가기 그리드), `<usage>`, `<siteNotes>`, `<checkups>`. 비밀번호만 필요한 리더는 건너뛰어도 됩니다.

리더가 따를 규칙: 모르는 요소와 속성은 무시합니다. 선택 섹션이 없으면 “없음”을 뜻합니다. `uuid` 값은 내보내기를 거듭해도 그대로 유지되므로 같은 계정은 같은 id를 갖습니다. `created` / `updated` / `at`의 날짜는 Unix 초 단위입니다.

두 사본 병합 *(5.0)*: 앱에 이미 있는 `uuid`의 계정이 파일에 들어 있으면, **스마트 병합**은 `updated` 시각이 더 늦은 사본을 유지하고 교체된 비밀번호는 그 계정의 비밀번호 기록에 넣습니다. `updated`가 없는 계정(5.0 이전에 내보낸 것)은 기기에 있는 그대로 유지됩니다. 병합은 아무것도 삭제하지 않습니다. 다른 리더도 같은 규칙을 따라도 좋습니다.

## 암호화된 백업: 같은 XML을 감싸는 작은 봉투 형식

**이 백업 암호화**를 켜면(또는 패스키를 포함하면) 같은 XML이 다음과 같이 봉인됩니다. 모두 빅 엔디언입니다:

1. 8바이트 ASCII 매직 `8PWDENC1`.
2. 4바이트: 부호 없는 32비트 정수로 된 PBKDF2 반복 횟수 — 앱이 내보낼 때는 **600,000**.
3. 16바이트: 무작위 솔트.
4. 12바이트: AES-256-GCM 논스. 그 뒤에 암호문과 16바이트 GCM 태그가 이어집니다(통상적인 *nonce ‖ ciphertext ‖ tag* 배치).

키는 UTF-8 백업 비밀번호에 그 솔트와 반복 횟수를 적용한 **PBKDF2-HMAC-SHA256**이며, 길이는 32바이트입니다. 연관 데이터는 없습니다. 평문은 위의 일반 백업과 바이트 단위로 동일합니다. 공유(`.8pwdshare`)와 AirDrop 보관함 전송은 같은 봉투 형식을 쓰되, 6자리 일회용 코드를 비밀번호로 삼습니다.

독점 컨테이너도, 키 에스크로도, 비밀도 없습니다. 비밀번호만 있으면 표준 라이브러리 코드 두 줄로 파일이 열립니다.

## 샘플 파일

두 샘플에는 형식 8로 된 같은 가상의 보관함이 들어 있습니다 — 폴더 2개, 계정 3개(그중 하나는 별칭 포함, 모두 `created` / `updated` 시각 포함), 복구 코드가 딸린 2단계 인증 코드 1개, Wi-Fi 네트워크 1개, 카드 1개, 신원 정보 1개, 그리고 코드와 카드를 해당 계정에 연결하는 `<links>` 섹션. **안의 모든 값은 지어낸 것**이며, 실제 사람이나 사이트의 것은 하나도 없습니다.

- [sample-plain.8pwd](../../samples/sample-plain.8pwd) — 일반 XML, 3 KB. 어떤 텍스트 편집기로도 열 수 있습니다.
- [sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) — 같은 보관함을 비밀번호 `example`로 봉인한 파일.

둘 다 다른 백업과 똑같이 8PWD로 가져올 수 있어(**나 › 가져오기 › 8PWD 백업**), 파일이 앱에 어떻게 대응되는지 정확히 볼 수 있습니다.

## 앱 없이 파일 확인, 개수 세기, 복호화

`verify_8pwd.py`는 퍼블릭 도메인(CC0)으로 공개된 Python 3 파일 하나로, 검사에는 의존성이 필요 없습니다. 복호화에는 선택 패키지 `cryptography`가 필요합니다.

1. `python3 verify_8pwd.py sample-plain.8pwd` — 파일이 일반인지 암호화되었는지, 형식 버전, 내보낸 날짜, 들어 있는 계정 · 폴더 · 코드 · 네트워크 · 카드 · 신원 정보 · 패스키의 개수(4.0부터는 별칭 · 복구 코드 항목 · 연결 포함), 그리고 SHA-256을 알려 줍니다.
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example` — 메모리에서 복호화해 같은 개수를 출력합니다.
3. `python3 verify_8pwd.py Backup.8pwd --json` — 직접 만든 스크립트에서 쓸 수 있는 기계 판독용 출력.

파일에 쓰는 일도, 네트워크를 건드리는 일도 결코 없습니다. 먼저 읽어 보세요. 일부러 짧게 만들었습니다.

## 다른 형태로 데이터 꺼내기

- **CSV**: **나 › 내보내기 › 범용 CSV로 내보내기**는 Apple Passwords, 1Password, Bitwarden, 브라우저가 모두 가져오는 공통 열 집합(이름, URL, 사용자 이름, 비밀번호, 메모)을 씁니다. 내보내기는 Pro 여부와 관계없이 모든 플랜에서 됩니다.
- **2단계 인증 코드**: 각 `<totp>`는 표준 `otpauth://` URI입니다. 다른 인증 앱으로 옮길 수 있도록 앱이 하나씩 QR 코드로도 보여 줍니다.
- **종이**: 프린트한 비밀번호 장부와 비상 키트는 내가 남기고 떠날 사람들을 위한 오프라인 대비책입니다.

## 라이선스와 약속

법이 허용하는 한도 내에서 MNV LIMITED는 **CC0 1.0 Universal**에 따라 이 형식 사양에 대한 모든 저작권과 관련 권리를 포기했습니다. 검증 스크립트와 샘플 파일도 **CC0 1.0**으로 공개되며, 고지문은 스크립트 맨 위에 있습니다.

독점 컨테이너, 서버 쪽 키, 이 앱만 읽을 수 있는 형식은 추가하지 않겠습니다. 앞으로의 버전에서 형식이 바뀌면 버전 번호가 올라가고, 이전 파일은 계속 가져올 수 있으며, 변경 내용은 이 페이지와 릴리즈 노트에 적습니다.

## 같이 보기

- [내 데이터는 언제나 내 것](https://www.8pwd.com/ko/your-data)
- [보관함은 어떻게 암호화되나](https://www.8pwd.com/ko/encryption)
- [동기화하지 않는 이유 — 그리고 보관함 옮기는 법](https://www.8pwd.com/ko/why-no-sync)
- [8PWD로 옮기기](https://www.8pwd.com/ko/migrate)
