# PHP - modernização gradual

## Observações

O README upstream declara PHP 8.0-8.3.

`admin/lib/composer.json` fixa a plataforma Composer em PHP 8.0 e mantém dependências modernas misturadas com infraestrutura própria/legada.

`AppModel.php` usa `#[AllowDynamicProperties]`, sinal de compatibilidade explícita com mudanças do PHP 8.2.

O código ainda contém padrões históricos como:

- propriedades declaradas com `var`;
- SQL montado por string;
- vários `require_once`;
- helpers e classes globais;
- comentários de compatibilidade com PHP 5;
- tratamento manual de hashing e comparação.

## Estratégia proposta

Não migrar para framework nem aplicar refatoração maciça.

### Fase 1

- PHP syntax/lint em toda a árvore própria;
- PHPStan/Psalm em nível inicial e baseline;
- separar código próprio de `vendor/`;
- inventariar warnings/deprecations no PHP 8.3.

### Fase 2

- remover `AllowDynamicProperties` apenas onde propriedades puderem ser declaradas com segurança;
- adicionar tipos de retorno/parâmetros em classes isoladas;
- substituir utilitários criptográficos obsoletos;
- reduzir supressão de erro `@` em caminhos críticos.

### Fase 3

- melhorar autoload e composição de dependências;
- introduzir testes unitários no código próprio;
- modernizar componentes de acesso a dados de forma incremental.
