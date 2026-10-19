# .8pwd 파일 형식

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · [简体中文](../zh-Hans/README.md) · [日本語](../ja/README.md) · **한국어** · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Português (Brasil)](../pt-BR/README.md) · [Italiano](../it/README.md) · [العربية](../ar/README.md) · [Русский](../ru/README.md)

MNV LIMITED가 만든 iPhone, iPad, Mac용 오프라인 비밀번호 관리자 겸 인증 앱 **8PWD**의 공개 백업 형식입니다. 일반 XML, 선택적인 AES-256-GCM 봉투 형식, 샘플 파일 두 개, 파일 하나로 된 검증 도구 — 이것만 있으면 앱 없이도 어떤 백업이든 읽을 수 있습니다.

**원본:** https://www.8pwd.com/ko/open-format. 이 저장소는 같은 소스에서 생성한 미러로, 저희 웹사이트 없이도 형식을 읽고, 인용하고, 확인할 수 있게 합니다.

| 경로 | 설명 |
|---|---|
| [SPEC.md](SPEC.md) | 전체 사양: 일반 XML 백업, 암호화 봉투 형식, 리더가 따를 규칙 |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | 일반 백업, 형식 버전 8(8PWD 5.0). 안의 모든 값은 지어낸 것입니다 |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | 같은 보관함을 비밀번호 `example`로 암호화한 파일 |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | 백업을 검사하고, 개수를 세고, 복호화하는 Python 3 파일 하나 |

## 파일 확인

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # 복호화할 때만 필요
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

검증 도구는 파일에 쓰는 일도, 네트워크를 사용하는 일도, 비밀번호를 출력하는 일도 결코 없습니다. 이 커밋에 포함된 파일의 SHA-256(`shasum -a 256 -c`가 이 목록을 그대로 읽습니다):

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## 라이선스

사양, 샘플 파일, 검증 도구를 비롯해 이 저장소의 모든 것을 **CC0 1.0 공통**([영문 이용허락규약](../../LICENSE) · [크리에이티브 커먼즈 공식 번역본](LICENSE.md))에 따라 퍼블릭 도메인으로 내놓았습니다. 누구나 저희에게 묻지 않고, 저희 이름을 밝히지 않고, 비용을 내지 않고도 리더, 라이터, 변환기를 만들 수 있습니다.

## 앱

앱 자체는 오픈 소스가 아니지만, 형식은 공개되어 있습니다. [App Store의 8PWD](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/ko/)

## 문의

이 저장소는 이슈나 풀 리퀘스트를 받지 않습니다. 질문이나 정정 요청은 제목에 *Format*을 넣어 support@8pwd.com으로 보내 주세요.
