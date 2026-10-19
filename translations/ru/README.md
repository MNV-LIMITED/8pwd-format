# Формат файлов .8pwd

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · [简体中文](../zh-Hans/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Português (Brasil)](../pt-BR/README.md) · [Italiano](../it/README.md) · [العربية](../ar/README.md) · **Русский**

Открытый формат резервных копий **8PWD**, офлайн-менеджера паролей и аутентификатора для iPhone, iPad и Mac от MNV LIMITED: обычный XML, необязательный конверт AES-256-GCM, два примера файлов и верификатор в одном файле — этого достаточно, чтобы прочитать любую резервную копию без приложения.

**Основная версия:** https://www.8pwd.com/ru/open-format. Этот репозиторий — её зеркало, сгенерированное из того же источника, чтобы формат можно было читать, цитировать и проверять без нашего сайта.

| Путь | Что это |
|---|---|
| [SPEC.md](SPEC.md) | Полная спецификация: незашифрованная резервная копия в XML, зашифрованный конверт, правила для читающих программ |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | Незашифрованная резервная копия, версия формата 8 (8PWD 5.0). Все значения в ней вымышлены |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | То же хранилище, зашифрованное паролем `example` |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | Один файл на Python 3, который разбирает, подсчитывает и расшифровывает резервную копию |

## Проверить файл

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # нужно только для расшифровки
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

Верификатор никогда не пишет в файл, не обращается к сети и не выводит пароли. Контрольные суммы SHA-256 файлов в этом коммите (список можно проверить командой `shasum -a 256 -c`):

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## Лицензия

Всё содержимое репозитория — спецификация, примеры файлов и верификатор — передано в общественное достояние по условиям **CC0 1.0 Универсальная** ([юридический текст на английском](../../LICENSE) · [краткое описание от Creative Commons](https://creativecommons.org/publicdomain/zero/1.0/deed.ru)). Кто угодно может писать программы для чтения, записи или конвертации, не спрашивая нас, не упоминая нас и ничего нам не платя.

## Приложение

Само приложение не имеет открытого исходного кода; открыт формат. [8PWD в App Store](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/ru/)

## Контакты

Этот репозиторий не принимает issues и pull requests. Вопросы и исправления присылайте на support@8pwd.com, указав в теме письма *Format*.
