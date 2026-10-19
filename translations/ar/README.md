# صيغة ملفات .8pwd

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · [简体中文](../zh-Hans/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Português (Brasil)](../pt-BR/README.md) · [Italiano](../it/README.md) · **العربية** · [Русский](../ru/README.md)

صيغة النسخ الاحتياطية المفتوحة في **8PWD**، مدير كلمات المرور وتطبيق المصادقة دون اتصال لـ iPhone وiPad وMac من إنتاج MNV LIMITED: ملف XML عادي، وغلاف AES-256-GCM اختياري، وملفان نموذجيان، وأداة تحقق في ملف واحد — وهذا يكفي لقراءة أي نسخة احتياطية دون التطبيق.

**النسخة المرجعية:** https://www.8pwd.com/ar/open-format. وهذا المستودع نسخة مطابقة لها، مولَّدة من المصدر نفسه، كي يمكن قراءة الصيغة والاستشهاد بها والتحقق منها دون الحاجة إلى موقعنا.

| المسار | الوصف |
|---|---|
| [SPEC.md](SPEC.md) | المواصفة الكاملة: النسخة الاحتياطية العادية بصيغة XML، والغلاف المشفّر، وقواعد القارئات |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | نسخة احتياطية عادية وفق الإصدار 8 من الصيغة (8PWD 5.0). كل قيمة فيها مختلقة |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | الخزنة نفسها مشفّرة بكلمة السر `example` |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | ملف Python 3 واحد يفحص النسخة الاحتياطية ويعدّ محتوياتها ويفكّ تشفيرها |

## افحص ملفًا

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # مطلوب لفك التشفير فقط
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

لا تكتب أداة التحقق في الملف أبدًا، ولا تستخدم الشبكة أبدًا، ولا تطبع كلمة سر أبدًا. وهذه بصمات SHA-256 لملفات هذا الإيداع، بالصيغة التي يقرؤها `shasum -a 256 -c`:

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## الترخيص

كل ما في هذا المستودع — المواصفة والملفان النموذجيان وأداة التحقق — مطروح في الملك العام بموجب **CC0 1.0 عام** ([النص القانوني بالإنجليزية](../../LICENSE) · [الملخص الصادر عن المشاع الإبداعي](https://creativecommons.org/publicdomain/zero/1.0/deed.ar)). ويحق لأي شخص بناء قارئات أو كاتبات أو محوّلات دون استئذاننا أو ذكرنا أو الدفع لنا.

## التطبيق

التطبيق نفسه ليس مفتوح المصدر؛ أما الصيغة فمفتوحة. [8PWD على App Store](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/ar/)

## التواصل

لا يستقبل هذا المستودع مشكلات (issues) ولا طلبات سحب (pull requests). للأسئلة أو التصحيحات، راسلنا على support@8pwd.com مع كتابة *Format* في سطر الموضوع.
