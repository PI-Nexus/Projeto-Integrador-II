# Identidade Visual DM — Referência para o Front-end

> Subtarefa **SCRUM-27** · Card pai **SCRUM-5** · Branch: `feat/frontend`

Tokens levantados diretamente do CSS de produção de [vocedm.com.br/portal](https://www.vocedm.com.br/portal/)
e do perfil [@vocedm](https://www.instagram.com/vocedm/). Não são aproximações visuais — são os
valores computados que o site da DM realmente usa. Onde o projeto se afasta deles de propósito
(para passar nos critérios de contraste, por exemplo), o desvio está indicado no texto.

A implementação fica em `app/frontend/static/css/`:

| Arquivo | O que contém |
|---|---|
| `tokens.css` | Variáveis: cores, tipografia, espaçamento, formas, sombras e movimento |
| `base.css` | Reset, tipografia, ritmo das seções, cabeçalho e rodapé |
| `components.css` | Botões, cards, acordeão, formulário, telas de resultado, painéis e tabelas |

---

## 1. Cores

| Token | Hex | Onde é usado |
|---|---|---|
| `--dm-azul` | `#202AD0` | Cor primária. Cabeçalho, hero, fundos de seção, texto sobre os CTAs claros |
| `--dm-tinta` | `#000033` | Texto sobre fundos claros, texto do CTA secundário e fundo do rodapé |
| `--dm-aqua` | `#7DF4ED` | **CTA primário** (fundo) e marca-texto de palavra-chave em headline |
| `--dm-coral` | `#FF9A98` | **CTA secundário** (fundo) e fundo da seção de destaque ("Como funciona") |
| `--dm-amarelo` | `#FDE383` | Faixa multicolor e borda da tela "Em análise" |
| `--dm-verde` | `#6DDE9A` | Faixa multicolor e borda da tela "Aprovado" |
| `--dm-lilas` | `#F1EFFF` | Fundo da seção de dúvidas e de blocos de apoio (nota da etapa 4, resumo do resultado, faixa de produtos) |
| `--dm-cinza` | `#E3E1EC` | Bordas e estados desabilitados |
| `--dm-cinza-texto` | `#5F5E6B` | Texto secundário e placeholder. **Escurecido** a partir do `#91909A` que a DM usa (ver contraste) |
| `--dm-branco` | `#FFFFFF` | Fundo alternado e texto sobre azul |

### Variações de hover (criadas no projeto)

Não vêm do site da DM; existem para dar retorno visual ao passar o mouse.

| Token | Hex | Onde é usado |
|---|---|---|
| `--dm-azul-escuro` | `#1A21A6` | Hover de superfície azul |
| `--dm-aqua-escuro` | `#5FE4DC` | Hover do CTA primário |
| `--dm-coral-escuro` | `#F98784` | Hover do CTA secundário |

### Cores fora dos tokens

| Cor | Onde é usada |
|---|---|
| `#C62828` | Estado de erro: borda de campo inválido e mensagens de validação (`components.css` e `main.js`) |
| `#C94A4A` | Selo de status "Negado" nas tabelas dos painéis |

### Contraste (WCAG)

Razões calculadas com a fórmula de contraste do WCAG 2.x a partir dos valores hexadecimais acima.
Mínimos: **4,5:1** para texto normal (AA), **7:1** para AAA em texto normal e **3:1** para texto
grande (a partir de 18px, ou 14px em negrito).

| Combinação | Razão | Nível | Onde aparece |
|---|---|---|---|
| Branco sobre Azul | 9,12:1 | AAA | Textos do hero, benefícios e "Sobre a DM" |
| Aqua sobre Azul (e Azul sobre Aqua) | 6,96:1 | AA | Títulos dos benefícios, CTA primário, marca-texto |
| Tinta sobre Coral | 9,86:1 | AAA | CTA secundário e seção "Como funciona" |
| Tinta sobre Branco | 20,04:1 | AAA | Texto base |
| Tinta sobre Lilás | 17,69:1 | AAA | Texto nos blocos lilás |
| Azul sobre Branco | 9,12:1 | AAA | Títulos de cards, rótulos de campo |
| Cinza-texto `#5F5E6B` sobre Branco | 6,36:1 | AA | Texto de apoio |
| Cinza-texto `#5F5E6B` sobre Lilás | 5,62:1 | AA | Texto de apoio nos blocos lilás |
| Azul sobre Coral | 4,48:1 | **Abaixo do AA** em texto normal | Não usado: por isso o CTA secundário usa Tinta |
| Cinza-texto original da DM `#91909A` sobre Branco | 3,15:1 | **Abaixo do AA** | Não usado: foi o motivo do escurecimento |

⚠️ O `#91909A` da DM só passa em texto de 18px+ (ou 14px em negrito). Por isso o projeto usa o
`--dm-cinza-texto` escurecido (`#5F5E6B`), que serve também para texto pequeno. Ao reconferir os
valores no site da DM, **não** substitua o token pelo valor original.

---

## 2. Tipografia

**Catamaran** — disponível gratuitamente no Google Fonts. Pesos carregados: 400, 600, 700 e 800.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Catamaran:wght@400;600;700;800&display=swap" rel="stylesheet">
```

Se a fonte não carregar, o token `--fonte` cai para
`"Segoe UI", system-ui, -apple-system, sans-serif`.

| Uso | Peso | Observação |
|---|---|---|
| Títulos h1 e h2 | 800 | `line-height: 1.08`, `letter-spacing: -0.02em` |
| Títulos h3 e h4 | 700 | — |
| Texto de CTA | 700 | Nunca menos que 700 |
| Rótulos de campo | 700 | Em `--dm-azul` |
| Pergunta do acordeão (FAQ) | 600 | Em `--dm-tinta` |
| Corpo de texto | 400 | — |

Cor dos títulos: `--dm-azul` nos títulos de cards, de etapas do formulário e das telas de
resultado; o título principal (h1) das páginas internas herda `--dm-tinta`; sobre fundo azul, o
texto é branco.

### Escala tipográfica

A escala é fluida (`clamp()`): cresce com a largura da tela, sem media query.

| Token | Tamanho | Uso |
|---|---|---|
| `--texto-display` | 2,25rem → 4rem | h1 |
| `--texto-xg` | 1,75rem → 2,75rem | h2 |
| `--texto-g` | 1,25rem → 1,625rem | h3 e texto de apoio das seções |
| `--texto-m` | 1,0625rem → 1,1875rem | Corpo de texto |
| `--texto-p` | 0,9375rem | Texto dos botões e descrições de cards |
| `--texto-pp` | 0,8125rem | `small` e disclaimers |

---

## 3. Botões CTA — padrão obrigatório

Medidas idênticas às do site da DM. **As variantes compartilham a mesma geometria** (classe
`.btn`); o que muda é só a cor.

```
border-radius : 100px         ← pill, nunca cantos retos   (--raio-pill)
min-height    : 48px                                        (--altura-btn)
padding       : 0 24px                                      (0 var(--e-5))
font-size     : 15px                                        (--texto-p)
font-weight   : 700
font-family   : Catamaran
border        : 1px solid (mesma cor do fundo)
```

| Variante | Classe | Fundo | Texto | Quando usar |
|---|---|---|---|---|
| **Primário** | `.btn--primario` | `--dm-aqua` `#7DF4ED` | `--dm-azul` `#202AD0` | Ação principal da tela — "Peça seu cartão", "Enviar solicitação" |
| **Secundário** | `.btn--secundario` | `--dm-coral` `#FF9A98` | `--dm-tinta` `#000033` | Ação alternativa — "Conhecer o DM Cred", "Simular empréstimo" |
| **Terciário / ghost** | `.btn--ghost` | transparente | herda a cor do contexto (branco sobre azul, azul sobre claro) | Ação de baixa ênfase — "Voltar", "Sair", "Já sou cliente" |

⚠️ **Desvio em relação à DM:** o CTA secundário usa texto em `--dm-tinta`, e não em azul. Azul sobre
coral dá 4,48:1 e reprova em AA no tamanho do botão; a Tinta (também cor de marca) chega a 9,86:1 e
a diferença visual é pequena.

A variante "sólido azul" que a DM usa em ações dentro de seções brancas **não foi implementada**
no projeto: não há classe para ela.

**Hover:** o botão sobe 2px; o primário e o secundário escurecem o fundo (`--dm-aqua-escuro` e
`--dm-coral-escuro`) e ganham uma sombra da própria cor.

Regra de composição da DM: **um único CTA primário por seção**. Quando há dois botões lado a lado,
o segundo é ghost ou secundário — nunca dois aqua. No projeto, a regra vale no hero, em "Como
funciona" e na chamada final; as exceções são o cabeçalho (um primário e um ghost) e a seção
"Escolha o cartão", onde cada um dos três cards tem o seu CTA primário.

---

## 4. Componentes recorrentes

### Faixa multicolor
Divisor horizontal de 5 blocos de largura igual, **14px** de altura, na ordem:
`azul · coral · amarelo · aqua · verde`. Usada entre o hero e a primeira seção de conteúdo. No
formulário de solicitação, o indicador de progresso reaproveita as cores da faixa, uma por etapa.

### Ritmo de seções
Ordem das superfícies na landing page:

`cabeçalho + hero (azul)` → `faixa` → `Escolha o cartão (branco)` → `Benefícios (azul)` →
`Como funciona (coral)` → `Sobre a DM (azul)` → `Dúvidas (lilás)` → `Chamada final (azul)` →
`rodapé (tinta)`

A DM alterna `branco → azul → branco`, com **uma** seção coral funcionando como acento. Nunca duas
seções azuis seguidas: o lilás e a tinta do rodapé separam os blocos azuis.

### Cards de cartão (`.cartao`)
Fundo branco, borda `1px solid --dm-cinza`, `border-radius` 16px (`--raio-card`) e sombra sutil
(`--sombra-card`). Ao passar o mouse, o card sobe 4px e ganha uma sombra mais alta. Estrutura:
título em `--dm-azul`, resumo em `--dm-cinza-texto`, lista de pontos e o CTA. Não leva ícone.

### Card de benefício (`.beneficio`)
Usado sobre fundo azul: fundo branco a 8% de opacidade, borda branca a 16%, `border-radius` 16px.
Título em `--dm-aqua` e texto em branco.

### Acordeão (FAQ) (`.duvida`)
Elemento `<details>` com fundo branco (sobre a seção lilás), borda `1px solid --dm-cinza` e
`border-radius` 10px (`--raio-mini`). A borda vira azul ao passar o mouse e quando está aberto. A
pergunta usa `--dm-tinta` com peso 600, e o marcador é um **+** à direita que gira para **×**
quando o item abre.

### Marca-texto
Palavra-chave da headline com fundo `--dm-aqua` e texto **sempre em azul** (o branco herdado do
hero não passa sobre o aqua) — recurso editorial forte da marca no Instagram.
No HTML: `<mark>`. Usa `border-radius` de 6px.

### Telas de resultado
O cartão de resultado tem uma borda superior de 8px que indica o desfecho: `--dm-verde`
(aprovado), `--dm-amarelo` (em análise) e `--dm-coral` (negado). O resumo do pedido usa fundo
`--dm-lilas`.

### Faixa de produtos
Faixa discreta fixa na base da tela, com fundo `--dm-lilas`, que oferece DM Cred e Empréstimo
Pessoal. Aparece 1,5 segundo depois do carregamento, fecha pelo botão × ou pela tecla Esc e, depois
de fechada, não volta a aparecer na mesma sessão do navegador.

### Selos de status (painéis)
Nas tabelas dos painéis, o status da solicitação aparece num selo em pílula:

| Status | Cor do selo |
|---|---|
| Aprovado | `--dm-verde` |
| Em análise | `--dm-amarelo` |
| Negado | `#C94A4A` (fora dos tokens) |

As telas restritas (`admin.html` e `painel_vendedor.html`) combinam o Bootstrap 5.3.8 com esses
mesmos tokens.

---

## 5. Voz da marca

- Assinatura: **"Toda história merece crédito"**
- Tom: direto, acolhedor, sem jargão financeiro. Trata o leitor por "você".
- Frases curtas e afirmativas: *"Peça seu cartão"*, *"A DM resolve"*, *"É fácil"*.
- Sempre incluir o disclaimer `*Sujeito à análise de crédito.` abaixo de CTA de solicitação.

---

## 6. Assets em `app/frontend/static/img/`

Fotos recortadas dos banners oficiais da DM — o recorte isola a pessoa modelo e descarta o texto
publicitário que vinha embutido no banner original.

| Arquivo | Dimensão | Alt sugerido | Onde usar |
|---|---|---|---|
| `modelo-cartao-visa.{webp,jpg}` | 800×1025 | Mulher sorrindo segurando um cartão DM Visa | Hero da landing page |
| `modelo-celular.{webp,jpg}` | 700×1068 | Mulher sorrindo usando o celular | Seção "Como funciona" |
| `modelo-emprestimo.{webp,jpg}` | 900×920 | Homem sorrindo olhando o celular ao ar livre | Oferta alternativa em `negado.html` |
| `modelo-computador.{webp,jpg}` | 800×952 | Mulher sorrindo trabalhando no computador | Seção de benefícios |
| `colaboradores-dm.{webp,jpg}` | 980×451 | Dois colaboradores da DM conversando no escritório | Seção "Sobre a DM" |
| `cartoes-dm.{webp,png}` | 768×515 | Cartões DM Visa e Cartão Loja em perspectiva | Seção "Escolha o cartão" |
| `logo-dm.svg` | 32×34 | Logo da DM | Cabeçalho e rodapé |
| `dm-favicon-32x-32x.ico` | — | — | Favicon das páginas |
| `gear-fill.svg` | — | "config" | Ícone de engrenagem no cabeçalho, que leva ao `/admin` |

Servir sempre com `<picture>` e WebP à frente do fallback. Nos templates, os caminhos passam por
`url_for`:

```html
<picture>
  <source srcset="{{ url_for('static', filename='img/modelo-cartao-visa.webp') }}" type="image/webp">
  <img src="{{ url_for('static', filename='img/modelo-cartao-visa.jpg') }}" width="800" height="1025"
       alt="Mulher sorrindo segurando um cartão DM Visa">
</picture>
```

**Logo.** O arquivo `logo-dm.svg` usa `fill="currentColor"`, mas, como é carregado por uma tag
`<img>`, o SVG não herda a cor do CSS. Por isso o `base.css` aplica
`filter: brightness(0) invert(1)` e o logo aparece **sempre branco** — sobre o cabeçalho azul e
sobre o rodapé tinta. Para usá-lo em azul sobre fundo claro seria preciso embutir o SVG na página
ou criar uma segunda versão do arquivo. O ícone `gear-fill.svg` recebe o mesmo filtro.

---

## 7. Fonte dos valores

Extraídos via `getComputedStyle` nas páginas
`vocedm.com.br/portal/` e `vocedm.com.br/portal/dm-visa/` em 08/09/2026.
Ao revisar, reconferir — a DM atualiza campanhas com frequência.

Desvios deliberados em relação aos valores da DM:

- `--dm-cinza-texto` escurecido de `#91909A` para `#5F5E6B`, para passar em AA;
- texto do CTA secundário em `--dm-tinta`, em vez de azul;
- tokens de hover (`--dm-azul-escuro`, `--dm-aqua-escuro` e `--dm-coral-escuro`), criados no
  projeto.