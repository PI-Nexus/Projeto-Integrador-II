# Escopo do Front-end — Landing Page de Captação DM

> Subtarefa **SCRUM-26** · Card pai **SCRUM-5** · Sprint 1 (07/09 → 27/09/2026)
> Branch: `feat/frontend`

Documento de escopo da landing page de captação e pré-qualificação de clientes do desafio do
parceiro acadêmico **DM**. Define o que o front-end entrega, o fluxo do usuário, a matriz de
regras de negócio e os wireframes de baixa fidelidade.

---

## 1. Objetivo

Permitir que um visitante solicite um **Cartão DM (Visa)** ou um **Cartão Loja** informando seus
dados, e receba na hora o resultado da pré-qualificação — aprovado, em análise ou reprovado —
aplicando corretamente as regras da DM e as restrições geográficas de seleção de loja.

Fora do escopo (definido no PDF do desafio): emissão e envio do cartão físico.

---

## 2. Páginas

| Arquivo | Papel |
|---|---|
| `frontend/index.html` | Landing page de marketing — apresenta os cartões e leva ao formulário |
| `frontend/solicitar.html` | Wizard de solicitação em 4 etapas |
| `frontend/resultado.html` | Desfecho da pré-qualificação |

---

## 3. Mapa de seções da landing page

| # | Seção | Conteúdo | Fundo |
|---|---|---|---|
| 1 | Header | Logo DM, navegação, CTAs "Peça seu cartão" e "Já sou cliente" | azul |
| 2 | Hero | Foto de modelo + card branco com headline, subtítulo, disclaimer e CTA | imagem |
| 3 | Faixa multicolor | Divisor de 5 blocos (azul · coral · amarelo · aqua · verde) | — |
| 4 | Escolha seu cartão | 3 cards: DM Visa, Cartão Loja, Cartão Loja Digital | branco |
| 5 | Benefícios | Grid de 6 feature-pills com ícone | branco |
| 6 | Como funciona | 3 passos numerados + foto de modelo | coral |
| 7 | Sobre a DM | Texto institucional + foto de colaboradores | azul |
| 8 | FAQ | Accordion com as dúvidas frequentes da captação | branco |
| 9 | Footer | Colunas de links, CNPJ e redes sociais | azul |

---

## 4. Fluxo do usuário

```
index.html
   │
   │  clique em qualquer CTA "Peça seu cartão"
   ▼
solicitar.html
   │
   ├─ Etapa 1 · Qual cartão você quer?
   │     ( ) DM Visa   ( ) Cartão Loja   ( ) Cartão Loja Digital
   │
   ├─ Etapa 2 · Seus dados
   │     nome · CPF · nascimento · e-mail · celular · renda
   │     [ ] Sou colaborador da DM  →  revela campo "matrícula"
   │
   ├─ Etapa 3 · Onde você está
   │     CEP  →  preenche cidade/UF  →  logradouro · número · complemento
   │
   └─ Etapa 4 · Sua loja                (pulada quando o cartão é DM Visa)
         busca de loja parceira, filtrada pela UF quando for Cartão Loja
         campo opcional de vendedor
   │
   ▼
resultado.html
   ├─ Aprovado      → parabéns + próximos passos
   ├─ Em análise    → prazo de retorno + canal de acompanhamento
   └─ Reprovado     → oferta alternativa (DM Cred / Empréstimo Pessoal)
```

**Por que wizard e não página única:** a etapa 4 depende do CEP informado na etapa 3, e parceiros
da DM podem ter mais de 1000 estabelecimentos. Separar em etapas permite filtrar a lista antes de
exibi-la e reduz o abandono do formulário.

---

## 5. Matriz de pré-qualificação

Regras extraídas de *Desafio do Parceiro Academico 2ADS - DM.pdf*.

| Cliente | Cartão DM (Visa) | Cartão Loja | Cartão Loja Digital |
|---|---|---|---|
| **Colaborador DM** | **Aprovado automático** | **Reprovado automático** | ⚠️ ver questão aberta |
| **Não colaborador** | Análise → apto = aprovado, senão *em análise* | Análise → mesma regra | Análise → mesma regra |

### Restrições geográficas

| Cartão | Regra |
|---|---|
| **DM Visa** | Aprovável em **qualquer estado** — é bandeirado e passa em qualquer lugar |
| **Cartão Loja** | Só permite escolher lojas na **mesma UF do CEP informado** (é private label e só passa nas unidades do parceiro) |
| **Cartão Loja Digital** | **Sem restrição de estado**. A interface precisa deixar explícito que **não há cartão físico** |

### Questão aberta para o PO (Davi)

> Colaborador da DM solicitando **Cartão Loja Digital**: a reprovação automática do Cartão Loja
> vale também para a variante digital?

O PDF define reprovação automática para "Cartão Loja" sem distinguir a variante digital.
Até a resposta, o front trata o Loja Digital como **Cartão Loja** (reprova o colaborador),
com a regra isolada em uma constante para virar uma linha de mudança.

---

## 6. Campos do formulário

### Etapa 1 — Tipo de cartão
`tipo_cartao` — radio, obrigatório: `dm_visa` | `loja` | `loja_digital`

### Etapa 2 — Dados pessoais
| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `nome` | text | sim | nome completo |
| `cpf` | text | sim | máscara + dígito verificador |
| `nascimento` | date | sim | maior de 18 anos |
| `email` | email | sim | — |
| `celular` | tel | sim | máscara (DD) 9XXXX-XXXX |
| `renda` | number | sim | usado na análise de aptidão |
| `colaborador` | checkbox | não | revela `matricula` |
| `matricula` | text | condicional | só quando `colaborador` marcado |

### Etapa 3 — Endereço
`cep` (obrigatório, dispara consulta), `logradouro`, `numero`, `complemento`, `bairro`,
`cidade` e `uf` — os três últimos preenchidos a partir do CEP.

### Etapa 4 — Loja
`loja` (obrigatório quando o cartão não é DM Visa) e `vendedor` (opcional — atende a US SCRUM-12).

---

## 7. Wireframes

### Landing page (desktop)

```
┌────────────────────────────────────────────────────────────┐
│ [dm]  Cartões  Benefícios  Dúvidas      (Peça seu cartão)  │ azul
├────────────────────────────────────────────────────────────┤
│                                       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│   ┌──────────────────────────┐        ▓▓ foto modelo  ▓▓▓  │
│   │ Toda história            │        ▓▓ com o cartão ▓▓▓  │
│   │ merece [crédito]         │        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│   │ Peça seu cartão em       │        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│   │ minutos, 100% online.    │        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│   │ ( Peça seu cartão )      │        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│   └──────────────────────────┘        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
├──────────┬──────────┬──────────┬──────────┬────────────────┤ faixa
│  azul    │  coral   │ amarelo  │   aqua   │     verde      │
├──────────┴──────────┴──────────┴──────────┴────────────────┤
│              Escolha o cartão ideal pra você                │
│   ┌───────────┐    ┌───────────┐    ┌───────────┐          │
│   │  DM Visa  │    │Cartão Loja│    │Loja Digital│         │
│   │  [cartão] │    │ [cartão]  │    │ [cartão]  │          │
│   │  Aceito   │    │ Na sua    │    │ Sem cartão│          │
│   │ em qualquer│   │ loja      │    │ físico    │          │
│   │  lugar    │    │ preferida │    │           │          │
│   │ ( Pedir ) │    │ ( Pedir ) │    │ ( Pedir ) │          │
│   └───────────┘    └───────────┘    └───────────┘          │
├────────────────────────────────────────────────────────────┤
│                  Um cartão, vários benefícios               │
│   [◐] limite       [◐] segurança      [◐] aprovação        │
│   [◐] descontos    [◐] aproximação    [◐] prazo            │
├────────────────────────────────────────────────────────────┤
│  Peça agora, é fácil!              ▓▓▓▓▓▓▓▓▓▓              │ coral
│   ① Escolha o cartão               ▓▓ modelo ▓▓             │
│   ② Preencha seus dados            ▓▓ celular▓▓             │
│   ③ Receba a resposta na hora      ▓▓▓▓▓▓▓▓▓▓              │
│   ( Peça seu cartão )                                       │
├────────────────────────────────────────────────────────────┤
│  Dúvidas frequentes                                         │
│  ▸ Quem pode pedir o cartão DM?                       (+)   │
│  ▸ Preciso ter conta na DM?                           (+)   │
├────────────────────────────────────────────────────────────┤
│  DM │ Produtos │ Explore │ Transparência                    │ azul
└────────────────────────────────────────────────────────────┘
```

### Wizard (mobile)

```
┌──────────────────────┐   ┌──────────────────────┐
│ ●──●──○──○   2 de 4  │   │ ●──●──●──●   4 de 4  │
│                      │   │                      │
│ Onde você está       │   │ Sua loja             │
│                      │   │                      │
│ CEP *                │   │ ⓘ Mostrando apenas   │
│ ┌──────────────────┐ │   │   lojas de SP        │
│ │ 12245-000        │ │   │                      │
│ └──────────────────┘ │   │ Buscar loja          │
│ São José dos Campos  │   │ ┌──────────────────┐ │
│ SP                   │   │ │ 🔍 super...      │ │
│                      │   │ └──────────────────┘ │
│ Logradouro *         │   │ ○ Supermercado A     │
│ ┌──────────────────┐ │   │   Jardim Aquarius/SP │
│ │                  │ │   │ ○ Supermercado B     │
│ └──────────────────┘ │   │   Centro/SP          │
│                      │   │                      │
│ Nº *      Compl.     │   │ Vendedor (opcional)  │
│ ┌─────┐   ┌────────┐ │   │ ┌──────────────────┐ │
│ │     │   │        │ │   │ │                  │ │
│ └─────┘   └────────┘ │   │ └──────────────────┘ │
│                      │   │                      │
│ ( Voltar )(Continuar)│   │ ( Voltar )( Enviar ) │
└──────────────────────┘   └──────────────────────┘
```

### Resultado

```
┌────────────────────────────┐  ┌────────────────────────────┐
│          ✓                 │  │          ✕                 │
│  Aprovado!                 │  │  Não foi dessa vez         │
│  Seu Cartão DM Visa foi    │  │  Não conseguimos aprovar   │
│  aprovado.                 │  │  seu cartão agora.         │
│                            │  │                            │
│  Próximos passos:          │  │  ── Mas temos outra opção ─│
│  1. Confirme por e-mail    │  │  ▓▓▓▓  DM Cred             │
│  2. Retire na loja         │  │  ▓▓▓▓  Empréstimo Pessoal  │
│                            │  │  ( Conhecer o DM Cred )    │
│  ( Voltar para o início )  │  │  ( Voltar para o início )  │
└────────────────────────────┘  └────────────────────────────┘
```

---

## 8. Sequência de entrega

| Sprint | Subtarefa | Entrega |
|---|---|---|
| 1 | SCRUM-26 | Este documento |
| 1 | SCRUM-27 | Design tokens e assets da DM |
| 1 | SCRUM-28 | `index.html` semântico, sem CSS |
| 1 | SCRUM-29 | `solicitar.html` e `resultado.html` semânticos, sem CSS |
| 2 | *a criar* | CSS base, componentes e responsividade |
| 2 | *a criar* | JavaScript: wizard, validação, motor de regras, busca de loja |
| 3 | *a criar* | Migração para Bootstrap 5 e integração com a API Flask |

---

## 9. Dependências de outros cards

- **SCRUM-6 (back-end):** o motor de decisão definitivo. Até existir, a pré-qualificação roda em
  JavaScript no cliente atrás de uma camada `api.js`, para que a troca por `fetch` seja pontual.
- **SCRUM-7 (banco):** origem das lojas parceiras e da base de colaboradores. Até lá, mocks em
  `frontend/static/data/`.
