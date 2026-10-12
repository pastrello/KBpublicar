# Frontend - Audit 0.1

## O que o Dark Mode já revelou

O KBPublisher usa muitos estilos com:

- cores literais;
- estilos inline;
- seletores específicos por ID;
- `!important`;
- folhas de estilo carregadas por componente;
- jQuery/jQuery UI e plugins antigos.

Foi por isso que o overlay precisou tratar componentes como `popup2`, `ezmodal`, Magnific Popup e o CSS específico do popup de busca.

## Enquanto o projeto permanecer separado

O dark mode continua como overlay. Não vamos alterar os CSS originais do KBPublisher.

## Se houver futuro fork

A melhoria estrutural mais promissora é substituir cores literais por tokens/variáveis CSS:

```css
:root {
    --kbp-background: #fff;
    --kbp-surface: #f4f4f4;
    --kbp-text: #121212;
    --kbp-border: #dadada;
    --kbp-accent: #4584c1;
}

[data-theme="dark"] {
    --kbp-background: #11161d;
    --kbp-surface: #181f27;
    --kbp-text: #e7ebf0;
    --kbp-border: #3b4a5c;
}
```

Isso permitiria tornar o dark mode nativo e reduzir drasticamente overrides.

## Próximos levantamentos

- inventário de CSS inline;
- dependências JS e versões;
- templates que carregam CSS local depois do CSS global;
- acessibilidade e contraste;
- possibilidade de eliminar plugins sem manutenção.
