# Identidade Visual DM — Referência para o Front-end

> Subtarefa **SCRUM-27** · Card pai **SCRUM-5** · Branch `feat/frontend`

Tokens levantados diretamente do CSS de produção de [vocedm.com.br/portal](https://www.vocedm.com.br/portal/)
e do perfil [@vocedm](https://www.instagram.com/vocedm/). Não são aproximações visuais — são os
valores computados que o site da DM realmente usa.

---

## 1. Cores

| Token | Hex | Onde a DM usa |
|---|---|---|
| `--dm-azul` | `#202AD0` | Cor primária. Header, fundos de seção, texto sobre os CTAs claros |
| `--dm-tinta` | `#000033` | Texto sobre fundos claros |
| `--dm-aqua` | `#7DF4ED` | **CTA primário** (fundo) e marca-texto de palavra-chave em headline |
| `--dm-coral` | `#FF9A98` | **CTA secundário** (fundo) e fundo de seção de destaque |
| `--dm-amarelo` | `#FDE383` | Faixa multicolor |
| `--dm-verde` | `#6DDE9A` | Faixa multicolor e formas de recorte atrás das fotos |
| `--dm-lilas` | `#F1EFFF` | Fundo de card, accordion e feature-pill |
| `--dm-cinza` | `#E3E1EC` | Bordas e estados desabilitados |
| `--dm-cinza-texto` | `#91909A` | Texto secundário e placeholder |
| `--dm-branco` | `#FFFFFF` | Fundo alternado e texto sobre azul |

### Contraste (WCAG)

| Combinação | Razão | Nível |
|---|---|---|
| Aqua `#7DF4ED` sobre Azul `#202AD0` | ≈ 9,3:1 | AAA |
| Branco sobre Azul `#202AD0` | ≈ 11:1 | AAA |
| Coral `#FF9A98` sobre Azul `#202AD0` | ≈ 5,5:1 | AA |
| Tinta `#000033` sobre Branco | ≈ 18:1 | AAA |

⚠️ `--dm-cinza-texto` (`#91909A`) sobre branco fica em ≈ 3,1:1 — **só usar em texto de 18px+
ou 14px bold**, nunca em corpo de texto pequeno.

---

## 2. Tipografia

**Catamaran** — disponível gratuitamente no Google Fonts.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Catamaran:wght@400;600;700;800&display=swap" rel="stylesheet">
```

| Uso | Peso | Observação |
|---|---|---|
| Títulos (h1–h3) | 700 | Sempre em `--dm-azul` sobre claro, branco sobre azul |
| Texto de CTA | 700 | Nunca menos que 700 |
| Subtítulos e labels | 600 | — |
| Corpo de texto | 400 | — |

---

## 3. Botões CTA — padrão obrigatório

Medidas idênticas às do site da DM. **As três variantes compartilham a mesma geometria**;
o que muda é só a cor.

```
border-radius : 100px       ← pill, nunca cantos retos
height        : 48px
padding       : 0 24px
font-weight   : 700
font-family   : Catamaran
border        : 1px solid (mesma cor do fundo)
```

| Variante | Fundo | Texto | Quando usar |
|---|---|---|---|
| **Primário** | `--dm-aqua` `#7DF4ED` | `--dm-azul` `#202AD0` | Ação principal da tela — "Peça seu cartão", "Continuar" |
| **Secundário** | `--dm-coral` `#FF9A98` | `--dm-azul` `#202AD0` | Ação alternativa — "Negocie já", "Saiba mais" |
| **Terciário / ghost** | transparente | branco sobre azul, azul sobre claro | Ação de baixa ênfase — "Voltar", "Ajuda" |
| **Sólido azul** | `--dm-azul` | branco | Usado pela DM em ações dentro de seções brancas |

Regra de composição da DM: **um único CTA primário por seção**. Quando há dois botões lado a
lado, o segundo é ghost ou secundário — nunca dois aqua.

---

## 4. Componentes recorrentes

### Faixa multicolor
Divisor horizontal de 5 blocos de largura igual, ~16px de altura, na ordem:
`azul · coral · amarelo · aqua · verde`. Usada entre o hero e a primeira seção de conteúdo.

### Ritmo de seções
Alternância `branco → azul → branco`, com **uma** seção coral funcionando como acento.
Nunca duas seções azuis seguidas.

### Cards
Fundo branco, borda `1px solid --dm-cinza`, `border-radius` ~16px, sombra sutil.
Ícone em círculo sólido `--dm-azul` com o glifo em branco.

### Feature-pill
Fundo `--dm-lilas`, `border-radius` 8px, ícone circular azul deslocado para fora à esquerda.

### Accordion (FAQ)
Fundo `--dm-lilas`, `border-radius` 10px, texto `--dm-tinta` peso 400, ícone ⊕ à direita.

### Marca-texto
Palavra-chave da headline com fundo `--dm-aqua` — recurso editorial forte da marca no Instagram.
No HTML: `<mark>`.

---

## 5. Voz da marca

- Assinatura: **"Toda história merece crédito"**
- Tom: direto, acolhedor, sem jargão financeiro. Trata o leitor por "você".
- Frases curtas e afirmativas: *"Peça seu cartão"*, *"A DM resolve"*, *"É fácil"*.
- Sempre incluir o disclaimer `*Sujeito à análise de crédito.` abaixo de CTA de solicitação.

---

## 6. Assets em `frontend/static/img/`

Fotos recortadas dos banners oficiais da DM — o recorte isola a pessoa modelo e descarta o texto
publicitário que vinha embutido no banner original.

| Arquivo | Dimensão | Alt sugerido | Onde usar |
|---|---|---|---|
| `modelo-cartao-visa.{webp,jpg}` | 800×1025 | Mulher sorrindo segurando um cartão DM Visa | Hero da landing page |
| `modelo-celular.{webp,jpg}` | 700×1068 | Mulher sorrindo usando o celular | Seção "como funciona" |
| `modelo-emprestimo.{webp,jpg}` | 900×920 | Homem sorrindo olhando o celular ao ar livre | Oferta alternativa em `resultado.html` |
| `modelo-computador.{webp,jpg}` | 800×952 | Mulher sorrindo trabalhando no computador | Seção de benefícios |
| `colaboradores-dm.{webp,jpg}` | 980×451 | Dois colaboradores da DM conversando no escritório | Seção "sobre a DM" |
| `cartoes-dm.{webp,png}` | 768×515 | Cartões DM Visa e Cartão Loja em perspectiva | Seção "escolha seu cartão" |
| `logo-dm.svg` | 32×34 | Logo da DM | Header e footer |

Servir sempre com `<picture>` e WebP à frente do fallback:

```html
<picture>
  <source srcset="static/img/modelo-cartao-visa.webp" type="image/webp">
  <img src="static/img/modelo-cartao-visa.jpg" width="800" height="1025"
       alt="Mulher sorrindo segurando um cartão DM Visa">
</picture>
```

`logo-dm.svg` usa `fill="currentColor"` — herda a cor do CSS, então o mesmo arquivo serve no
header azul (branco) e no fundo claro (azul).

---

## 7. Fonte dos valores

Extraídos via `getComputedStyle` nas páginas
`vocedm.com.br/portal/` e `vocedm.com.br/portal/dm-visa/` em 08/09/2026.
Ao revisar, reconferir — a DM atualiza campanhas com frequência.
