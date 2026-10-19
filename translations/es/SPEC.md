# El formato de archivo .8pwd

[English](../../SPEC.md) · [繁體中文](../zh-HK/SPEC.md) · [简体中文](../zh-Hans/SPEC.md) · [日本語](../ja/SPEC.md) · [한국어](../ko/SPEC.md) · [Deutsch](../de/SPEC.md) · [Français](../fr/SPEC.md) · **Español** · [Português (Brasil)](../pt-BR/SPEC.md) · [Italiano](../it/SPEC.md) · [العربية](../ar/SPEC.md) · [Русский](../ru/SPEC.md)

> Traducción de [SPEC.md](../../SPEC.md), generada a partir de la misma fuente que [www.8pwd.com/es/open-format](https://www.8pwd.com/es/open-format). En caso de discrepancia, prevalece la versión en inglés.

Sin servidor, el archivo lo es todo. Por eso el formato de archivo es público, está documentado aquí por completo, se ha liberado al dominio público y viene con archivos de ejemplo y un verificador que puedes ejecutar sin 8PWD. Si desapareciéramos mañana, tus contraseñas seguirían siendo un archivo legible.

## Qué significa aquí “abierto”

- **Documentado**: cada elemento y atributo que escribe la app está listado en esta página, con las reglas que debe seguir un lector.
- **Dominio público**: la especificación se publica bajo **CC0 1.0**; cualquiera puede crear lectores, escritores o conversores sin pedirnos permiso, sin nombrarnos y sin pagarnos.
- **Verificable**: [verify_8pwd.py](../../tools/verify_8pwd.py) (CC0) inspecciona, cuenta y descifra una copia de seguridad sin más dependencias que Python 3.
- **Estable**: el número de versión solo sube; las secciones nuevas siempre se añaden al final; un lector ignora lo que no conoce. Los cambios de formato se enumeran en la página [Novedades](https://www.8pwd.com/es/changelog).
- **Replicado**: esta página, los dos archivos de ejemplo y el verificador están replicados en [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format) (en inglés), donde cada cambio del formato tiene un historial público y fechado.

La app en sí no es de código abierto; el formato sí. Esa es la promesa que importa para tus datos.

## La copia sin cifrar: un solo archivo XML en UTF-8

Exporta sin contraseña y obtendrás un archivo `.8pwd` que es XML sin cifrar. El elemento raíz es `<vault>` con los atributos `app` (el nombre del producto), `version` (actualmente **8**), `exportedAt` (ISO 8601 UTC), `nodes` y `formattedBlocks` (recuentos). Dentro, en este orden:

- `<tree>`: carpetas y cuentas. `<folder uuid name>` se anida libremente. `<account uuid name favorite icon category created updated>` contiene `<fields>`, y cada `<field name kind hidden>value</field>` es una línea del registro. `created` y `updated` *(5.0)* son opcionales: cuándo se creó el registro y cuándo se editó por última vez, en segundos Unix.
- El **significado** de un campo lo da su `kind`: `username`, `password`, `url`, `email`, `phone`, `note` o `text` (campo personalizado libre). `name` es solo la etiqueta que ve el usuario: está localizada (“Password”, “密碼”, “Passwort”) y no debe usarse para decidir qué es un campo. `hidden="true"` marca un campo que la app oculta por defecto.
- `<formattedBlocks>`: bloques de texto reutilizables, `<formattedBlock uuid name recordSeparator>` con un `<template>` y `<accountRefs><ref uuid/></accountRefs>`.
- `<totps>`: secretos de dos factores como URI estándar `<totp uuid note linkedAccount>otpauth://…</totp>`; `linkedAccount` es el uuid de la primera cuenta a la que pertenecen (se conserva por compatibilidad con lectores antiguos; el conjunto completo, de muchos a muchos, está en `<links>`, más abajo). Cualquier autenticador puede importar la URI.
- `<recoveryCodes>` *(4.0)*: los códigos de respaldo de un solo uso que da un sitio al configurar la autenticación de dos factores, un `<codes totp="uuid">free text, newlines kept</codes>` por cada entrada de códigos (texto libre; se conservan los saltos de línea). Se guardan fuera de `<totp>` para que la URI siga siendo una URI pura.
- `<links>` *(4.0)*: `<link account="uuid" kind="totp|card|identity" target="uuid"/>`, que indica qué códigos de dos factores, tarjetas e identidades pertenecen a qué cuentas, en una relación de muchos a muchos. Los dos extremos son uuid que aparecen en otra parte del mismo archivo; un lector que solo quiera contraseñas puede saltarse esta sección.
- Dentro de `<account>` *(4.0)*: elementos hijos opcionales `<alias>other sign-in name</alias>` antes de `<fields>`, con los otros nombres de usuario o direcciones de correo de la cuenta. La búsqueda y el Autorrelleno de la app los reconocen; un lector puede tratarlos como nombres de usuario adicionales para la misma contraseña.
- `<wifi>`: `<network uuid ssid security password hidden note/>`.
- `<cards>`: `<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>` más los atributos de la dirección de facturación con el prefijo `b` (`bName`, `bStreet1`, `bCity`…).
- `<identities>`: `<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>` con los elementos hijos `<email label>`, `<phone label>` y `<address label aStreet1 aCity aRegion aPostal aCountry/>`.
- `<passkeys>`: `<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>`; los valores binarios van en Base64. Las llaves de acceso se escriben **solo** en copias cifradas.
- Secciones internas que la app usa para sí misma: `<preferences>` (los accesos directos de Inicio y, desde la 4.0, la cuadrícula Yo › Mis accesos como `<quickAccess>` / `<quickAccessHidden>`), `<usage>`, `<siteNotes>`, `<checkups>`. Un lector que solo quiera contraseñas puede saltárselas.

Reglas para los lectores: los elementos y atributos desconocidos se ignoran; una sección opcional ausente significa “ninguna”; los valores `uuid` se mantienen estables entre exportaciones, así que la misma cuenta conserva el mismo id; las fechas en `created` / `updated` / `at` son segundos Unix.

Combinar dos copias *(5.0)*: cuando un archivo contiene una cuenta cuyo `uuid` ya tiene la app, la **Combinación inteligente** conserva la copia con la hora `updated` más reciente y pasa la contraseña reemplazada al historial de esa cuenta; una cuenta sin `updated` (exportada antes de la 5.0) se conserva tal como está en el dispositivo. Una combinación nunca elimina nada. Cualquier otro lector puede seguir la misma regla.

## La copia cifrada: un pequeño sobre alrededor del mismo XML

Activa **Cifrar esta copia de seguridad** (o incluye llaves de acceso) y el mismo XML se sella así, todo en big-endian:

1. 8 bytes: cabecera mágica ASCII `8PWDENC1`.
2. 4 bytes: el recuento de iteraciones de PBKDF2 como entero de 32 bits sin signo; **600.000** cuando exporta la app.
3. 16 bytes: sal aleatoria.
4. 12 bytes: nonce de AES-256-GCM, seguido del texto cifrado y de la etiqueta GCM de 16 bytes (la disposición habitual *nonce ‖ texto cifrado ‖ etiqueta*).

La clave es **PBKDF2-HMAC-SHA256** de la contraseña de la copia en UTF-8 con esa sal y ese recuento de iteraciones, de 32 bytes de longitud. Sin datos asociados. El texto en claro es la copia sin cifrar descrita arriba, byte a byte. Los compartidos (`.8pwdshare`) y las transferencias de bóveda por AirDrop usan el mismo sobre con un código de un solo uso de 6 dígitos como contraseña.

No hay contenedor propietario, ni custodia de claves, ni secreto alguno: con la contraseña, dos líneas de la biblioteca estándar abren el archivo.

## Archivos de ejemplo

Los dos ejemplos contienen la misma bóveda inventada en el formato 8: dos carpetas, tres cuentas (una con un alias, cada una con sus marcas de tiempo `created` / `updated`), un código de dos factores con códigos de recuperación, una red Wi-Fi, una tarjeta y una identidad, además de la sección `<links>`, que vincula el código y la tarjeta con sus cuentas. **Todos sus valores son inventados**; nada pertenece a una persona o a un sitio reales.

- [sample-plain.8pwd](../../samples/sample-plain.8pwd): el XML sin cifrar, 3 KB. Ábrelo en cualquier editor de texto.
- [sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd): la misma bóveda sellada con la contraseña `example`.

Los dos se importan en 8PWD como cualquier otra copia de seguridad (**Yo › Importar › Copia de 8PWD**), así que puedes ver exactamente cómo se corresponde el archivo con la app.

## Comprueba, cuenta o descifra un archivo sin la app

`verify_8pwd.py` es un único archivo de Python 3, de dominio público (CC0) y sin dependencias para inspeccionar; descifrar requiere el paquete opcional `cryptography`.

1. `python3 verify_8pwd.py sample-plain.8pwd`: dice si el archivo está sin cifrar o cifrado, la versión del formato, la fecha de exportación, cuántas cuentas, carpetas, códigos, redes, tarjetas, identidades y llaves de acceso contiene (y, desde la 4.0, alias, entradas de códigos de recuperación y vínculos), y su SHA-256.
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example`: descifra en memoria e imprime los mismos recuentos.
3. `python3 verify_8pwd.py Backup.8pwd --json`: salida legible por máquina para tus propios scripts.

Nunca escribe en el archivo y nunca toca la red. Léelo primero; es corto a propósito.

## Sacar los datos en otras formas

- **CSV**: **Yo › Exportar › Exportar un CSV universal** escribe el conjunto de columnas habitual (nombre, URL, usuario, contraseña, nota) que importan Contraseñas de Apple, 1Password, Bitwarden y los navegadores. La exportación funciona en todos los planes, con Pro o sin él.
- **Códigos de dos factores**: cada `<totp>` es una URI `otpauth://` estándar; la app también los muestra como códigos QR, de uno en uno, para pasarlos a otro autenticador.
- **Papel**: la libreta de contraseñas impresa y el kit de emergencia son el respaldo sin conexión para las personas que dejas atrás.

## Licencia y promesa

En la medida en que lo permite la ley, MNV LIMITED ha renunciado a todos los derechos de autor y derechos conexos sobre esta especificación de formato bajo **CC0 1.0 Universal**. El script verificador y los archivos de ejemplo también se publican bajo **CC0 1.0**; el aviso está al principio del script.

No añadiremos un contenedor propietario, una clave en el servidor ni un formato que solo pueda leer esta app. Si una versión futura cambia el formato, el número de versión sube, los archivos antiguos se siguen importando y el cambio queda escrito en esta página y en las notas de la versión.

## Véase también

- [Tus datos siempre son tuyos](https://www.8pwd.com/es/your-data)
- [Cómo se cifra la bóveda](https://www.8pwd.com/es/encryption)
- [Por qué no sincroniza y cómo mover una bóveda](https://www.8pwd.com/es/why-no-sync)
- [Cambiar a 8PWD](https://www.8pwd.com/es/migrate)
