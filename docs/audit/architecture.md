# Arquitetura - leitura inicial

## Estrutura observada

A raiz do projeto separa principalmente:

- `admin/` - área administrativa, bibliotecas, módulos, cron e templates;
- `client/` - área pública, API e skins;
- `setup/` - instalação e upgrades;
- `plugins/` - infraestrutura/plugin data do produto;
- entry points como `index.php`, `api.php`, `endpoint.php`, `rss.php`.

A aplicação usa uma arquitetura própria anterior aos frameworks PHP modernos. Há camadas como `BaseModel`, `AppModel`, controllers, views e templates próprios.

## Persistência

O projeto usa ADOdb. O `admin/lib/composer.json` declara, entre outras dependências:

- PHPMailer;
- ADOdb;
- AWS SDK for PHP;
- Bacon QR Code;
- RobThree TwoFactorAuth.

O diretório `admin/lib/vendor/` está versionado no próprio repositório.

## Frontend

A área pública usa skins em `client/skin/view_*/*/`. A área administrativa possui CSS/templates próprios e vários componentes jQuery/jQuery UI e plugins legados.

## Ponto importante para nossa estratégia

Como o KBpublicar continua separado, não vamos modificar essa arquitetura ainda. O objetivo inicial é mapear pontos de manutenção e produzir patches pequenos somente quando houver ganho claro e teste de regressão.
