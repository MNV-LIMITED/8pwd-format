# O formato de arquivo .8pwd

[English](../../SPEC.md) · [繁體中文](../zh-HK/SPEC.md) · [简体中文](../zh-Hans/SPEC.md) · [日本語](../ja/SPEC.md) · [한국어](../ko/SPEC.md) · [Deutsch](../de/SPEC.md) · [Français](../fr/SPEC.md) · [Español](../es/SPEC.md) · **Português (Brasil)** · [Italiano](../it/SPEC.md) · [العربية](../ar/SPEC.md) · [Русский](../ru/SPEC.md)

> Tradução de [SPEC.md](../../SPEC.md), gerada a partir da mesma fonte que [www.8pwd.com/pt-br/open-format](https://www.8pwd.com/pt-br/open-format). Em caso de divergência, a versão em inglês prevalece.

Sem servidor, o arquivo é tudo. Por isso o formato do arquivo é público, está documentado aqui por completo, foi liberado em domínio público e vem com arquivos de exemplo e um verificador que você roda sem o 8PWD. Se sumíssemos amanhã, suas senhas continuariam sendo um arquivo legível.

## O que “aberto” quer dizer aqui

- **Documentado**: todos os elementos e atributos que o app grava estão listados nesta página, com as regras que um leitor precisa seguir.
- **Domínio público**: a especificação é liberada sob a **CC0 1.0** — qualquer pessoa pode criar leitores, gravadores ou conversores sem nos pedir, sem nos citar e sem nos pagar.
- **Verificável**: [verify_8pwd.py](../../tools/verify_8pwd.py) (CC0) inspeciona, conta e descriptografa um backup sem nenhuma dependência além do Python 3.
- **Estável**: o número da versão só aumenta; seções novas são sempre acrescentadas no fim; um leitor ignora o que não conhece. As mudanças no formato ficam listadas na página [Novidades](https://www.8pwd.com/pt-br/changelog).
- **Espelhado**: esta página, os dois arquivos de exemplo e o verificador estão espelhados em [github.com/MNV-LIMITED/8pwd-format](https://github.com/MNV-LIMITED/8pwd-format) (em inglês), onde cada mudança no formato fica registrada num histórico público e datado.

O app em si não é de código aberto; o formato é. Essa é a promessa que importa para os seus dados.

## O backup simples: um único arquivo XML em UTF-8

Exporte sem senha e você obtém um arquivo `.8pwd` que é XML simples. O elemento raiz é `<vault>` com os atributos `app` (o nome do produto), `version` (atualmente **8**), `exportedAt` (ISO 8601 UTC), `nodes` e `formattedBlocks` (contagens). Dentro dele, nesta ordem:

- `<tree>` — pastas e contas. `<folder uuid name>` pode ser aninhado livremente. `<account uuid name favorite icon category created updated>` contém `<fields>`, e cada `<field name kind hidden>value</field>` é uma linha do registro. `created` e `updated` *(5.0)* são opcionais: quando o registro foi criado e editado pela última vez, em segundos Unix.
- O **significado** de um campo é o seu `kind`: `username`, `password`, `url`, `email`, `phone`, `note` ou `text` (campo personalizado livre). `name` é só o rótulo que o usuário vê — ele é localizado (“Senha”, “Password”, “密碼”) e não deve ser usado para decidir o que um campo é. `hidden="true"` marca um campo que o app oculta por padrão.
- `<formattedBlocks>` — blocos de texto reutilizáveis: `<formattedBlock uuid name recordSeparator>` com um `<template>` e `<accountRefs><ref uuid/></accountRefs>`.
- `<totps>` — segredos de dois fatores como URIs `<totp uuid note linkedAccount>otpauth://…</totp>` padrão; `linkedAccount` é o uuid da primeira conta a que pertencem (mantido para leitores mais antigos — o conjunto completo, muitos-para-muitos, está em `<links>`, veja abaixo). Qualquer autenticador consegue importar a URI.
- `<recoveryCodes>` *(4.0)* — os códigos de backup de uso único que um site fornece quando você configura a autenticação de dois fatores, um `<codes totp="uuid">free text, newlines kept</codes>` por entrada de códigos. Ficam fora de `<totp>` para que a URI continue sendo uma URI pura.
- `<links>` *(4.0)* — `<link account="uuid" kind="totp|card|identity" target="uuid"/>`: quais códigos de dois fatores, cartões e identidades pertencem a quais contas, numa relação muitos-para-muitos. As duas pontas são uuids que aparecem em outras partes do mesmo arquivo; um leitor que só quer as senhas pode pular esta seção.
- Dentro de `<account>` *(4.0)*: elementos filhos opcionais `<alias>other sign-in name</alias>` antes de `<fields>` — os outros nomes de usuário ou endereços de e-mail da conta. A busca e o Preenchimento automático do app também os reconhecem; um leitor pode tratá-los como nomes de usuário extras para a mesma senha.
- `<wifi>` — redes Wi-Fi: `<network uuid ssid security password hidden note/>`.
- `<cards>` — `<card uuid number name cardholder expMonth expYear cvv pin issuer note owner …/>` mais os atributos do endereço de cobrança com o prefixo `b` (`bName`, `bStreet1`, `bCity`…).
- `<identities>` — `<identity uuid title firstName lastName username company jobTitle birthday idNumber passportNumber licenseNumber note owner created updated>` com os elementos filhos `<email label>`, `<phone label>` e `<address label aStreet1 aCity aRegion aPostal aCountry/>`.
- `<passkeys>` — `<passkey uuid rpId rpName userName userDisplayName userHandle credentialId privateKey signCount note owner created lastUsed/>`; os valores binários estão em Base64. Chaves de acesso são gravadas **somente** em backups criptografados.
- Seções de manutenção interna que o app usa para si mesmo: `<preferences>` (os atalhos do Início e, a partir da 4.0, a grade Eu › Meus atalhos como `<quickAccess>` / `<quickAccessHidden>`), `<usage>`, `<siteNotes>`, `<checkups>`. Um leitor que só quer as senhas pode pulá-las.

Regras para leitores: elementos e atributos desconhecidos são ignorados; seções opcionais ausentes significam “nenhum”; os valores de `uuid` são estáveis entre exportações, então a mesma conta mantém o mesmo id; as datas em `created` / `updated` / `at` são segundos Unix.

Mesclagem de duas cópias *(5.0)*: quando um arquivo contém uma conta cujo `uuid` o app já tem, a **Mesclagem inteligente** mantém a cópia com a data `updated` mais recente e guarda a senha substituída no histórico de senhas dessa conta; quando a conta no arquivo não tem `updated` (foi exportada antes da 5.0), a versão do dispositivo é mantida como está. Uma mesclagem nunca apaga nada. Outros leitores podem seguir a mesma regra, se quiserem.

## O backup criptografado: um pequeno envelope em volta do mesmo XML

Ative **Criptografar este backup** (ou inclua chaves de acesso) e o mesmo XML é selado da seguinte forma, tudo em big-endian:

1. 8 bytes: o magic ASCII `8PWDENC1`.
2. 4 bytes: a contagem de iterações do PBKDF2 como inteiro de 32 bits sem sinal — **600.000** quando o app exporta.
3. 16 bytes: salt aleatório.
4. 12 bytes: o nonce do AES-256-GCM, seguido do texto cifrado e da tag GCM de 16 bytes (o layout habitual *nonce ‖ texto cifrado ‖ tag*).

A chave é o **PBKDF2-HMAC-SHA256** da senha de backup em UTF-8 com esse salt e essa contagem de iterações, com 32 bytes. Sem dados associados. O texto em claro é o backup simples descrito acima, byte a byte. Compartilhamentos (`.8pwdshare`) e transferências de cofre por AirDrop usam o mesmo envelope, com um código de uso único de 6 dígitos como senha.

Não há contêiner proprietário, custódia de chave nem segredo: com a senha, duas linhas de código da biblioteca padrão abrem o arquivo.

## Arquivos de exemplo

Os dois exemplos contêm o mesmo cofre inventado no formato 8 — duas pastas, três contas (uma delas com um apelido, todas com as datas `created` / `updated`), um código de dois fatores com códigos de recuperação, uma rede Wi-Fi, um cartão e uma identidade, além da seção `<links>`, que liga o código e o cartão às suas contas. **Todos os valores neles são fictícios**; nada pertence a uma pessoa ou a um site reais.

- [sample-plain.8pwd](../../samples/sample-plain.8pwd) — o XML simples, 3 KB. Abra-o em qualquer editor de texto.
- [sample-encrypted.8pwd](../../samples/sample-encrypted.8pwd) — o mesmo cofre selado com a senha `example`.

Os dois são importados no 8PWD como qualquer outro backup (**Eu › Importar › Backup do 8PWD**), para você ver exatamente como o arquivo corresponde ao app.

## Verifique, conte ou descriptografe um arquivo sem o app

`verify_8pwd.py` é um único arquivo Python 3, em domínio público (CC0) e sem dependências para inspecionar; descriptografar exige o pacote opcional `cryptography`.

1. `python3 verify_8pwd.py sample-plain.8pwd` — diz se o arquivo é simples ou criptografado, a versão do formato, a data de exportação, quantas contas, pastas, códigos, redes, cartões, identidades e chaves de acesso ele contém (e, a partir da 4.0, apelidos, entradas de códigos de recuperação e vínculos), e o seu SHA-256.
2. `python3 verify_8pwd.py sample-encrypted.8pwd --password example` — descriptografa em memória e imprime as mesmas contagens.
3. `python3 verify_8pwd.py Backup.8pwd --json` — saída legível por máquina para os seus próprios scripts.

Ele nunca grava no arquivo e nunca toca na rede. Leia-o primeiro; é curto de propósito.

## Tirar os dados em outros formatos

- **CSV**: **Eu › Exportar › Exportar um CSV universal** grava o conjunto comum de colunas (nome, URL, nome de usuário, senha, nota) que Apple Passwords, 1Password, Bitwarden e os navegadores importam. A exportação funciona em todos os planos, Pro ou não.
- **Códigos de dois fatores**: cada `<totp>` é uma URI `otpauth://` padrão; o app também os mostra como códigos QR, um de cada vez, para levar a outro autenticador.
- **Papel**: o caderno de senhas impresso e o kit de emergência são a alternativa offline para as pessoas que ficarem depois de você.

## Licença e promessa

Na medida permitida pela lei, a MNV LIMITED renunciou a todos os direitos autorais e direitos conexos sobre esta especificação de formato sob a **CC0 1.0 Universal**. O script verificador e os arquivos de exemplo também são liberados sob a **CC0 1.0**; o aviso está no início do script.

Não vamos adicionar um contêiner proprietário, uma chave do lado do servidor nem um formato que só este app consiga ler. Se uma versão futura mudar o formato, o número da versão aumenta, os arquivos antigos continuam sendo importados, e a mudança fica registrada nesta página e nas notas de lançamento.

## Veja também

- [Seus dados são sempre seus](https://www.8pwd.com/pt-br/your-data)
- [Como o cofre é criptografado](https://www.8pwd.com/pt-br/encryption)
- [Por que não há sincronização — e como mover um cofre](https://www.8pwd.com/pt-br/why-no-sync)
- [Migrando para o 8PWD](https://www.8pwd.com/pt-br/migrate)
