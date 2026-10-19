# Formato de arquivo .8pwd

[English](../../README.md) · [繁體中文](../zh-HK/README.md) · [简体中文](../zh-Hans/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · **Português (Brasil)** · [Italiano](../it/README.md) · [العربية](../ar/README.md) · [Русский](../ru/README.md)

O formato aberto de backup do **8PWD**, o gerenciador de senhas e autenticador offline da MNV LIMITED para iPhone, iPad e Mac: XML simples, um envelope AES-256-GCM opcional, dois arquivos de exemplo e um verificador que cabe num único arquivo — o suficiente para ler qualquer backup sem o app.

**Versão de referência:** https://www.8pwd.com/pt-br/open-format. Este repositório a espelha e é gerado a partir da mesma fonte, para que o formato possa ser lido, citado e verificado sem o nosso site.

| Caminho | O que é |
|---|---|
| [SPEC.md](SPEC.md) | A especificação completa: o backup XML simples, o envelope criptografado e as regras para leitores |
| [samples/sample-plain.8pwd](../../samples/sample-plain.8pwd) | Um backup simples, versão 8 do formato (8PWD 5.0). Todos os valores nele são fictícios |
| [samples/sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) | O mesmo cofre, criptografado com a senha `example` |
| [tools/verify_8pwd.py](../../tools/verify_8pwd.py) | Um único arquivo Python 3 que inspeciona, conta e descriptografa um backup |

## Verifique um arquivo

```sh
python3 tools/verify_8pwd.py samples/sample-plain.8pwd
pip install cryptography        # só é necessário para descriptografar
python3 tools/verify_8pwd.py samples/sample-encrypted.8pwd --password example
```

O verificador nunca grava no arquivo, nunca toca na rede e nunca imprime uma senha. SHA-256 dos arquivos deste commit (`shasum -a 256 -c` lê esta lista):

```
86c0b58b96cb42e1dbcc7f48b67ba58455c0712361f410621d4c9f7fe17993a8  samples/sample-plain.8pwd
f458855cd90f00dbfe93a8f6a6bb2778d9104781804a1b7edd2680a48d8f23b9  samples/sample-encrypted.8pwd
aa12f5853eb24dc748244a2b5c217c9baa32617710ea3882cd90e8d1d692135e  tools/verify_8pwd.py
```

## Licença

Tudo o que está aqui — especificação, arquivos de exemplo e verificador — é dedicado ao domínio público sob a **CC0 1.0 Universal** ([texto legal em inglês](../../LICENSE) · [resumo da Creative Commons](https://creativecommons.org/publicdomain/zero/1.0/deed.pt-br)). Você pode criar leitores, gravadores ou conversores sem nos pedir, sem nos citar e sem nos pagar.

## O app

O app em si não é de código aberto; o formato é. [8PWD na App Store](https://apps.apple.com/app/id6785896938?ct=dir-github) · [www.8pwd.com](https://www.8pwd.com/pt-br/)

## Contato

Este repositório não aceita issues nem pull requests. Para dúvidas ou correções, envie um e-mail para support@8pwd.com com *Format* no assunto.
