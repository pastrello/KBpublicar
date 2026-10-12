# Segurança - Audit 0.1

## Observações confirmadas

### CSRF

Há infraestrutura explícita de CSRF. `Auth::getCsrfToken()` existe e vários módulos chamam `Validator->csrf()` ou `csrfCookie()`.

Conclusão inicial: **não considerar CSRF ausente**. A próxima etapa deve verificar cobertura, endpoints excepcionais e ações AJAX/API.

### Sessões

`Auth::authToSession()` chama `session_regenerate_id(true)` quando habilitado, com comentário explícito de prevenção a session fixation.

A sessão também inclui valores próprios de autenticação e, opcionalmente, vínculo ao IP.

### Hash de senha

`HashPassword.php` implementa hashing via `crypt()`. A preferência é Blowfish quando disponível, com fallback para SHA-512, SHA-256 e MD5-crypt. Para Blowfish, o custo observado é `07`.

`Auth::getAuth()` ainda reconhece hashes antigos de 32 caracteres e, após login válido, migra a senha para o formato atual.

**Alvo de modernização:** estudar substituição progressiva por `password_hash()`, `password_verify()` e `password_needs_rehash()`, preservando a migração transparente de hashes legados.

### SQL

Há diversos pontos onde SQL é montado por interpolação/`sprintf()`. Em `Auth::getAuth()`, por exemplo, username é tratado com `addslashes(stripslashes(...))` antes da construção da query.

Isso **não prova SQL injection**, mas é um alvo prioritário de revisão. ADOdb suporta mecanismos melhores que concatenação manual; devemos mapear origem e saneamento de cada valor antes de alterar comportamento.

### Serialização PHP

Há vários usos de `unserialize()` em dados vindos do banco e sessão persistida. A API v3, por exemplo, recupera uma sessão serializada do banco e chama `unserialize()`.

Isso deve ser auditado por fronteira de confiança:

- quem consegue gravar cada campo;
- se objetos podem estar presentes;
- se `allowed_classes => false` pode ser usado;
- se JSON pode substituir serialização em estruturas simples.

A mera existência de `unserialize()` não implica exploração.

### API

Na API v3, um hash interno ainda é criado com MD5 a partir de private key, user id e string fixa antes da montagem da sessão de API. A assinatura da requisição é validada separadamente por `KBApiValidator::validateSignature()`.

**Alvo de revisão:** entender o papel exato desse MD5 antes de propor substituição. Não tratá-lo automaticamente como hash de senha.

### Headers

Uma busca inicial encontrou referência a Content-Security-Policy comentada em fluxo de arquivo inline, mas não confirmou uma política CSP global.

**Próxima etapa:** inventariar headers de segurança efetivamente emitidos em Admin, Client, API e downloads.

## Prioridade sugerida

1. autenticação/sessões;
2. SQL dinâmico;
3. uploads/downloads;
4. `unserialize()`;
5. endpoints API;
6. headers e cookies;
7. dependências vendorizadas.
