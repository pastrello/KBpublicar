# Audit 0.1 - KBPublisher Community

Baseline analisado:

```text
repository: onesign12/kbpublisher-community
branch:     github
commit:     88c232fa8c40b807392a3a6469d8dcb50b26e5d0
date:       2026-04-21
```

Esta auditoria é exploratória. Os itens abaixo são classificados como **observação**, **alvo de revisão** ou **proposta**. A presença de um padrão antigo não é, por si só, prova de vulnerabilidade.

## Trilhas

- `architecture.md` - mapa inicial da aplicação.
- `security.md` - autenticação, sessões, CSRF, serialização, SQL e headers.
- `database.md` - ADOdb, MyISAM, transações e evolução para InnoDB.
- `php-modernization.md` - compatibilidade PHP 8 e dívida técnica.
- `frontend.md` - CSS, templates, jQuery e caminho para temas nativos.
- `roadmap.md` - ordem sugerida para aprofundar e implementar melhorias.

## Princípios

1. não alterar o upstream durante a fase de descoberta;
2. separar achado confirmado de hipótese;
3. criar teste antes de mudar comportamento crítico;
4. priorizar segurança, integridade e compatibilidade;
5. evitar reescrita total;
6. manter cada melhoria pequena e transportável para um futuro fork.
