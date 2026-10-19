# Formato de archivo .8pwd

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · [简体中文](../zh-Hans/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · **Español** · [Português (Brasil)](../pt-BR/README.md) · [Italiano](../it/README.md) · [العربية](../ar/README.md) · [Русский](../ru/README.md)

El formato abierto de copias de seguridad de **8PWD**, el gestor de contraseñas y autenticador sin conexión de MNV LIMITED para iPhone, iPad y Mac: XML sin cifrar, un sobre AES-256-GCM opcional, dos archivos de ejemplo y un verificador que cabe en un solo archivo. Con esto basta para leer cualquier copia de seguridad sin la app.

**Versión de referencia:** https://www.8pwd.com/es/open-format. Este repositorio la replica y se genera a partir de la misma fuente, para que el formato pueda leerse, citarse y comprobarse sin nuestro sitio web.

| Ruta | Qué es |
|---|---|
| [SPEC.md](SPEC.md) | La especificación completa: la copia XML sin cifrar, el sobre cifrado y las reglas para los lectores |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | Una copia sin cifrar, versión 8 del formato (8PWD 5.0). Todos sus valores son inventados |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | La misma bóveda, cifrada con la contraseña `example` |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | Un único archivo de Python 3 que inspecciona, cuenta y descifra una copia de seguridad |

## Comprueba un archivo

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # solo hace falta para descifrar
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

El verificador nunca escribe en el archivo, nunca toca la red y nunca imprime una contraseña. SHA-256 de los archivos de este commit (`shasum -a 256 -c` lee esta lista):

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## Licencia

Todo lo que hay aquí —la especificación, los archivos de ejemplo y el verificador— está dedicado al dominio público bajo **CC0 1.0 Universal** ([código legal en inglés](../../LICENSE) · [traducción oficial de Creative Commons](LICENSE.md)). Puedes crear lectores, escritores o conversores sin pedirnos permiso, sin nombrarnos y sin pagarnos.

## La app

La app en sí no es de código abierto; el formato sí. [8PWD en el App Store](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/es/)

## Contacto

Este repositorio no acepta issues ni pull requests. Para preguntas o correcciones, escribe a support@8pwd.com con *Format* en el asunto.
