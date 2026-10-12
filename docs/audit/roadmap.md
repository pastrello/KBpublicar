# Roadmap de auditoria

## Fase 0 - concluída

- manter KBpublicar independente;
- criar branch `develop`;
- registrar baseline upstream;
- criar remote helper;
- iniciar documentação de auditoria.

## Fase 1 - leitura estática

Prioridade:

1. autenticação e sessão;
2. CSRF e autorização;
3. SQL e acesso a dados;
4. uploads/downloads;
5. serialização;
6. API;
7. dependências;
8. frontend.

Entrega esperada: lista de achados com severidade, evidência, impacto e proposta.

## Fase 2 - baseline de testes

Antes de alterar core:

- instalar upstream limpo em laboratório;
- criar smoke tests de login, CRUD, busca, uploads, API e permissões;
- documentar versão PHP/MySQL/MariaDB;
- registrar warnings e deprecations.

## Fase 3 - melhorias de baixo risco

Candidatos:

- headers/cookies;
- hashing de senha com migração compatível;
- uso seguro de `unserialize()`;
- queries críticas parametrizadas;
- limpeza de warnings PHP 8.3;
- reforço de testes.

## Fase 4 - banco

Laboratório separado para MyISAM -> InnoDB, com testes de FULLTEXT, upgrade e concorrência.

## Gate de decisão

Após Fases 1 e 2:

- se os ganhos forem majoritariamente externos/isolados, manter overlay;
- se houver alterações recorrentes no core, criar fork oficial e transportar os commits;
- não converter o repositório atual em fork antes desse gate.
