# Changelog

## 0.3.2 - 2026-10-12

- Corrigido cache-busting dos assets do overlay.
  - versões anteriores usavam somente o `{pvhash}` do KBPublisher;
  - CSS e JS agora incluem também `kbpdark=<versão do KBpublicar>` na URL.
- Links de CSS/JS passam a expor `data-kbp-dark-version` e IDs estáveis para diagnóstico no navegador.
- O JavaScript publica a versão carregada em `document.documentElement.dataset.kbpDarkVersion` e `KBPTheme.version`.
- O seletor de tema informa a versão no atributo `title`.
- `check` agora detecta blocos de template antigos (`STALE`) mesmo que o arquivo CSS/JS no disco esteja correto.
- Análise do upstream documentou o comportamento híbrido das views públicas: `view_left`/ `view_fixed` reutilizam diversos templates de `view_default`.

## 0.3.1 - 2026-10-12

- Refinamento visual da área pública baseado em telas reais de uso.
- Corrigido o menu superior em dark mode:
  - fundo e bordas do bloco;
  - estado normal, hover e selecionado;
  - contraste do item `...`.
- Corrigida a faixa de navegação/breadcrumb, antes permanecendo clara em algumas skins.
- Melhorado o menu lateral:
  - blocos de categoria;
  - item selecionado da árvore;
  - hover dos nós.
- Corrigida a tela **Ask a Question**:
  - fundo do formulário;
  - labels e textos auxiliares;
  - inputs, select e textarea;
  - foco dos campos;
  - input de upload e botão nativo de seleção de arquivo.
- Melhorada a leitura de artigos:
  - metadados;
  - blocos `pre`/`code`/`.hljs`;
  - blockquotes;
  - tabelas no corpo do artigo.
- Mudanças continuam 100% no overlay: nenhum template original de formulário/artigo/menu é copiado ou substituído.

## 0.3.0 - 2026-10-12

- Projeto preparado para versionamento independente em GitHub, sem fork do KBPublisher.
- Licença do overlay alterada de MIT para Apache License 2.0, alinhada ao KBPublisher Community.
- JavaScript do seletor consolidado em uma única fonte (`assets/common/kbp-theme.js`).
- `VERSION` passa a ser a única fonte da versão; o patcher lê o valor desse arquivo.
- `check` agora valida também SHA-256 dos assets instalados e detecta arquivos modificados (`MOD`).
- Validação defensiva de marcadores incompletos ou duplicados nos templates.
- Preservação de CRLF/LF ao editar templates.
- Estado de instalação passa a controlar Admin e Client separadamente.
- Desinstalação parcial preserva o estado da área restante.
- Desinstalação ficou tolerante a estruturas alteradas por upgrades do KBPublisher.
- Backups passam a usar timestamp com microssegundos.
- Adicionado `--dry-run` a `install` e `uninstall`.
- Adicionados `.gitignore`, `NOTICE` e CI via GitHub Actions.
- Testes ampliados para integridade de assets, dry-run, CRLF e marcadores inválidos.

## 0.2.1 - 2026-10-12

- Corrigido contraste do popup de pesquisa da área pública (`block_search_top.html`).
  - `#search_menu` agora recebe fundo escuro explícito.
  - `#search_field` agora força fundo/texto/cursor compatíveis com o dark mode.
  - títulos, labels, ícone de busca e link **Advanced search** recebem cores próprias.
- Adicionada cobertura específica para o `ModalManager` (`.popup2`).
- Adicionada cobertura para diálogos `Easy-Z-Modal` (`.ezmodal`) no Client e no Admin.
- Melhorados inputs, selects, textareas, labels e botões de fechar dentro de modais.
- Adicionado refinamento para conteúdo inline do Magnific Popup.
- Mantida compatibilidade de atualização direta sobre v0.2.0; não é necessário desinstalar antes.

## 0.2.0 - 2026-10-03

- Corrigido carregamento do dark mode na área pública.
  - A v0.1 alterava `client/template.txt`, que não é o template renderizado pela Community 8.x atual.
  - Agora o instalador detecta `client/skin/view_*/*/page.html` e injeta os assets nos templates efetivamente usados.
- Migração automática da v0.1, removendo o bloco legado de `client/template.txt`.
- Seletor de tema redesenhado e mais visível, com rótulos de texto no desktop.
- Rótulos do seletor em inglês ou português de acordo com o idioma do documento/navegador.
- Cobertura ampliada no Admin:
  - cabeçalho de conteúdo (`titleCell`);
  - sidebars principal e secundária;
  - abas/submenus;
  - dashboard e bloco Quick Start;
  - formulários, tabelas, botões, filtros, comentários, badges e caixas auxiliares;
  - dropdowns, jQuery UI, tooltips e editores.
- Cobertura ampliada na área pública:
  - header, busca, artigos, tabelas, formulários, login, menus, TOC, popups, comentários e componentes jQuery UI.
- `check.sh` passa a validar os templates públicos realmente detectados.
- Testes ampliados para atualização v0.1 → v0.2 e múltiplas skins.

## 0.1.0 - 2026-10-03

- Primeira versão do overlay.
- Claro / Automático / Escuro.
- Admin, login, popups e tentativa inicial de área pública.
- Instalador/desinstalador idempotentes.
