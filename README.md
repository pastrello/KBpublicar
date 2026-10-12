# KBpublicar

Overlay independente de **dark mode** para [KBPublisher Community Edition](https://github.com/onesign12/kbpublisher-community), com modos **Claro / Escuro / Automático**.

> Projeto não oficial e independente. Não é um fork do KBPublisher e não redistribui a árvore de código do produto original.

## Objetivo

Adicionar um tema escuro utilizável ao KBPublisher Community 8.x sem alterar banco de dados e sem substituir os arquivos CSS originais da aplicação.

O instalador adiciona assets próprios e injeta apenas um pequeno bloco de referência nos templates do Admin e/ou da área pública.

## Recursos

- Claro, Escuro e Automático (`prefers-color-scheme`).
- Preferência local por navegador usando `localStorage` (`kbp_theme_mode`).
- Seletor visível de tema no Admin e na área pública.
- Admin, tela de login e popups.
- Área pública com detecção automática de `client/skin/view_*/*/page.html`.
- Cobertura para formulários, tabelas, menus, dropdowns, jQuery UI, `popup2`, `ezmodal`, Magnific Popup e popup de pesquisa.
- Instalador idempotente.
- Desinstalador conservador.
- Backup automático dos arquivos modificados.
- `--dry-run` para instalação e remoção.
- `check.sh` valida templates, integridade dos assets e versão do estado instalado.
- Nenhuma alteração em MySQL/MariaDB.

## Compatibilidade

Desenvolvido para a estrutura atual do **KBPublisher Community 8.x**.

O projeto valida os pontos de integração antes de alterar qualquer arquivo. Se a estrutura esperada não estiver presente, o instalador aborta em vez de aplicar um patch incerto.

## Instalação

```bash
chmod +x install.sh uninstall.sh check.sh

./install.sh /var/www/kbpublisher
./check.sh /var/www/kbpublisher
```

Antes de alterar arquivos, é possível visualizar o que seria feito:

```bash
./install.sh /var/www/kbpublisher --dry-run
```

Somente Admin:

```bash
./install.sh /var/www/kbpublisher --admin-only
```

Somente área pública:

```bash
./install.sh /var/www/kbpublisher --client-only
```

## Atualização de versões anteriores

A v0.3.0 pode ser instalada diretamente sobre v0.1.x ou v0.2.x:

```bash
./install.sh /var/www/kbpublisher
./check.sh /var/www/kbpublisher
```

O instalador:

1. remove o ponto legado da v0.1 em `client/template.txt`, se existir;
2. atualiza os assets;
3. mantém um único bloco de integração por template;
4. preserva backup dos arquivos que realmente forem alterados.

Depois da atualização, faça `Ctrl+F5` no navegador para evitar CSS/JS antigo em cache.

## Arquivos instalados no KBPublisher

```text
admin/css/kbp-dark-mode.css
admin/jscript/kbp-theme.js
client/skin/kbp-dark-mode.css
client/jscript/kbp-theme.js
```

No repositório, o JavaScript do seletor possui **uma única fonte** (`assets/common/kbp-theme.js`) e é distribuído para Admin e Client durante a instalação.

## Templates tocados

Admin:

```text
admin/template/page.html
admin/template/page_popup.html
admin/template/login.html
```

Área pública:

```text
client/skin/view_*/*/page.html
```

O trecho adicionado é delimitado por:

```html
<!-- KBP-DARK-MODE:BEGIN -->
...
<!-- KBP-DARK-MODE:END -->
```

## Controle de tema

No desktop, o seletor apresenta:

```text
Tema:  ☀ Claro   ◐ Automático   ☾ Escuro
```

Em telas estreitas, o controle é compactado para os ícones.

O modo **Automático** acompanha `prefers-color-scheme` do sistema operacional/navegador.

## Verificação

```bash
./check.sh /var/www/kbpublisher
```

Além de conferir os blocos nos templates, a v0.3.0 compara os SHA-256 dos assets instalados com os arquivos do pacote. Um arquivo alterado localmente aparece como `MOD`.

## Desinstalação

Visualizar primeiro:

```bash
./uninstall.sh /var/www/kbpublisher --dry-run
```

Remover:

```bash
./uninstall.sh /var/www/kbpublisher
```

O desinstalador remove somente o bloco do overlay. Assets que tenham sido modificados manualmente depois da instalação são preservados e geram um aviso.

Também é possível remover apenas uma área:

```bash
./uninstall.sh /var/www/kbpublisher --admin-only
./uninstall.sh /var/www/kbpublisher --client-only
```

O estado da área não removida é preservado.

## Atualização futura do KBPublisher

Fluxo recomendado:

1. `./uninstall.sh /var/www/kbpublisher`
2. atualizar o KBPublisher;
3. validar o KBPublisher original;
4. executar `./install.sh /var/www/kbpublisher --dry-run`;
5. instalar o overlay;
6. executar `./check.sh /var/www/kbpublisher`.

## Desenvolvimento e testes

```bash
python3 -m unittest discover -s tests -v
bash -n install.sh uninstall.sh check.sh
python3 -m py_compile tools/patcher.py
node --check assets/common/kbp-theme.js
```

O repositório possui GitHub Actions para executar essa validação em `push` e `pull_request`.

## Licença

**KBpublicar:** Apache License 2.0.

**KBPublisher Community Edition:** também é distribuído sob Apache License 2.0 por seus respectivos autores.

Este projeto é um overlay independente e não concede direitos sobre nomes, marcas ou outros ativos do KBPublisher além do uso necessário para indicar compatibilidade.
