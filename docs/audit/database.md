# Banco de dados - Audit 0.1

## Observações confirmadas

O schema de instalação atual contém tabelas com `ENGINE=MyISAM`.

`setup/inc/ParseSqlFile.php` também possui lógica explícita para reconhecer/converter sintaxe `ENGINE=MyISAM` / `TYPE=MyISAM`, mostrando que MyISAM faz parte do fluxo histórico de instalação/upgrade.

A camada de acesso é baseada em ADOdb.

## Consequências técnicas a avaliar

MyISAM não oferece transações nem foreign keys como InnoDB. Isso é relevante para:

- operações compostas de edição/exclusão;
- upgrades;
- recuperação de falhas parciais;
- concorrência;
- consistência entre tabelas relacionadas.

Não devemos converter tudo cegamente porque há uso de FULLTEXT e comportamento histórico que precisa ser testado.

## Plano para estudo InnoDB

1. inventariar todas as tabelas e engines;
2. identificar FULLTEXT e índices especiais;
3. mapear código que depende de table locks ou semântica MyISAM;
4. criar banco de teste convertido;
5. rodar instalação, upgrade, CRUD, busca e importação;
6. medir diferenças de desempenho;
7. somente então propor migração suportada.

## SQL

O código possui muita construção de SQL por strings. A modernização deve ser incremental:

- priorizar entradas externas;
- usar parâmetros/bind quando a camada permitir;
- manter SQL gerado por helpers onde já houver escaping centralizado;
- criar testes para consultas críticas antes da troca.
