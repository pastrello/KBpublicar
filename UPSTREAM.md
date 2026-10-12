# Upstream KBPublisher

O KBpublicar permanece um projeto independente, não um fork.

## Repositório oficial

- Projeto: `onesign12/kbpublisher-community`
- Branch principal upstream: `github`
- Baseline atual de auditoria: `88c232fa8c40b807392a3a6469d8dcb50b26e5d0`
- Data do commit baseline: 2026-04-21
- Licença upstream: Apache License 2.0

O SHA também é mantido em `UPSTREAM_BASE` para uso por scripts.

## Configuração local

Em um clone do KBpublicar:

```bash
./tools/configure-upstream.sh
```

Equivalente manual:

```bash
git remote add upstream https://github.com/onesign12/kbpublisher-community.git
git fetch upstream github
```

Se o remote já existir:

```bash
git remote set-url upstream https://github.com/onesign12/kbpublisher-community.git
git fetch upstream github
```

## Uso

Ver commits novos desde o baseline auditado:

```bash
git log --oneline $(cat UPSTREAM_BASE)..upstream/github
```

Ver diferenças de um arquivo:

```bash
git diff $(cat UPSTREAM_BASE)..upstream/github -- admin/lib/eleontev/Auth/Auth.php
```

Ver o estado completo do upstream sem misturá-lo ao projeto:

```bash
git show upstream/github:admin/lib/eleontev/Auth/Auth.php
```

## Regra de trabalho

Não fazer merge de `upstream/github` em `main` ou `develop` enquanto o projeto estiver no modelo separado.

As melhorias encontradas na auditoria devem ser documentadas e, quando aplicáveis ao overlay, implementadas no próprio KBpublicar. Se futuramente decidirmos criar um fork real, os commits e documentos produzidos aqui servirão de base para transportar as mudanças.
