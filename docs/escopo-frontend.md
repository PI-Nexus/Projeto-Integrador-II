# Escopo do Front-end — Landing Page de Captação DM

> Subtarefa **SCRUM-26** · Card pai **SCRUM-5** · Sprint 1 (07/09 → 27/09/2026)
> Branch: `feat/frontend`

Documento de escopo da landing page de captação e pré-qualificação de clientes do desafio do
parceiro acadêmico **DM**. Define o que o front-end entrega, o fluxo do usuário, a matriz de
regras de negócio, a integração com o back-end e os wireframes de baixa fidelidade.

> **Sobre esta revisão.** A versão da Sprint 1 descrevia um plano: páginas HTML estáticas,
> wizard com troca de tela, regras de aprovação em JavaScript e dados mockados. O projeto seguiu
> outro caminho — as páginas viraram templates Flask, as regras rodam no servidor e os dados
> vêm do MySQL. Este documento descreve **o que está implementado hoje**. A seção 10 compara o
> plano original com o resultado e a seção 11 lista as limitações conhecidas.

---

## 1. Objetivo

Permitir que um visitante solicite um **Cartão DM (Visa)**, um **Cartão Loja** ou um **Cartão Loja
Digital** informando seus dados, e receba na hora o resultado da pré-qualificação — **aprovado**,
**em análise** ou **negado** — aplicando corretamente as regras da DM e as restrições geográficas
de seleção de loja.

Além do fluxo do cliente, o front-end entrega duas áreas restritas: o **painel administrativo**
(acompanhar solicitações e cadastrar parceiros, colaboradores e vendedores) e o **painel do
vendedor** (analisar as solicitações da própria unidade).

Fora do escopo (definido no PDF do desafio): emissão e envio do cartão físico.

---

## 2. Páginas

Os templates ficam em `app/frontend/templates/` e são servidos pelo Flask (`app/routes.py`).

### Área pública

| Rota | Template | Papel |
|---|---|---|
| `/` | `index.html` | Landing page de marketing — apresenta os cartões e leva ao formulário |
| `/solicitar` | `solicita.html` | Formulário de solicitação, em 4 etapas numeradas mais a confirmação |
| `/aprovado` | `aprovado.html` | Resultado: aprovado |
| `/analise` | `analise.html` | Resultado: em análise |
| `/negado` | `negado.html` | Resultado: negado, com oferta de outros produtos (DM Cred e Empréstimo Pessoal) |

As três telas de resultado mostram o cartão e a loja da última solicitação enviada na sessão do
navegador.

### Área restrita

| Rota | Template | Papel |
|---|---|---|
| `/admin` | `admin_login.html` → `admin.html` | Painel administrativo, protegido pela senha `ADMIN_PASSWORD`. Abas: *Solicitações de cartão*, *Adição de parceiros*, *Adição de colaboradores* e *Cadastro de vendedores* |
| `/vendedor` | `vendedor.html` | Login do vendedor (e-mail + CPF) |
| `/vendedor/painel` | `painel_vendedor.html` | Solicitações da unidade do vendedor, com aprovação ou negativa |

### Arquivos de apoio

| Arquivo | Papel |
|---|---|
| `_popup_produtos.html` | Faixa "Conheça também" (DM Cred e Empréstimo Pessoal), incluída no formulário e nas três telas de resultado |
| `resultado.html` | **Legado.** Versão da Sprint 1 que reunia os três desfechos numa só página. Nenhuma rota a serve; fica no repositório só como referência |
| `static/css/tokens.css`, `base.css`, `components.css` | Tokens da identidade (ver [identidade-visual-dm.md](identidade-visual-dm.md)), base da página e componentes |
| `static/js/util.js`, `mascaras.js`, `main.js` | Validadores e formatadores, máscaras de digitação (CPF, data de nascimento, celular) e a lógica do formulário de solicitação (CEP, lista de lojas, validação e envio), além do modal de detalhes do admin |
| `static/js/parceiros.js`, `unidades.js`, `colaborador.js`, `vendedor.js` | Formulários e buscas dos painéis administrativo e do vendedor |
| `static/js/popup-produtos.js` | Abertura e fechamento da faixa de produtos |

O **Bootstrap 5.3.8** (CDN) é usado apenas nas telas restritas (`admin.html` e
`painel_vendedor.html`). As páginas públicas usam somente o CSS próprio.

---

## 3. Mapa de seções da landing page

| # | Seção | Conteúdo | Fundo |
|---|---|---|---|
| 1 | Cabeçalho | Logo DM, navegação (Cartões, Benefícios, Como funciona, Dúvidas), CTAs "Peça seu cartão" e "Já sou cliente" (abre o portal da DM em outra aba) e o ícone de engrenagem que leva ao `/admin` | azul |
| 2 | Hero | Headline "Toda história merece **crédito**", subtítulo, disclaimer, CTA e foto de modelo com o cartão | azul |
| 3 | Faixa multicolor | Divisor de 5 blocos (azul · coral · amarelo · aqua · verde) | — |
| 4 | Escolha o cartão (`#cartoes`) | Ilustração e 3 cards: DM Visa, Cartão Loja e Cartão Loja Digital, cada um com seu CTA | branco |
| 5 | Benefícios (`#beneficios`) | 6 cards de benefício e foto de modelo | azul |
| 6 | Como funciona (`#como-funciona`) | 3 passos numerados, CTA e foto de modelo | coral |
| 7 | Sobre a DM (`#sobre`) | Texto institucional e foto de colaboradores | azul |
| 8 | Dúvidas frequentes (`#duvidas`) | 6 perguntas em acordeão (`<details>`) | lilás |
| 9 | Chamada final | "Pronto pra começar?" e CTA | azul |
| 10 | Rodapé | Logo, colunas "Nossos produtos" e "Ajuda", aviso de projeto acadêmico | tinta (`#000033`) |

---

## 4. Fluxo do usuário

```text
/  (index.html)
   │
   │  clique em "Peça seu cartão" ou no CTA de um dos cartões
   ▼
/solicitar  (solicita.html) — uma única página, com 4 etapas numeradas
   │
   ├─ Etapa 1 · Qual cartão você quer?
   │     ( ) DM Visa   ( ) Cartão Loja   ( ) Cartão Loja Digital
   │
   ├─ Etapa 2 · Seus dados
   │     nome · CPF · nascimento · e-mail · celular · renda mensal
   │
   ├─ Etapa 3 · Onde você está
   │     CEP  →  preenche rua, bairro, cidade e UF (ViaCEP)  →  número · complemento
   │
   ├─ Etapa 4 · Sua loja               (não se aplica ao DM Visa)
   │     lista de lojas conforme o cartão e a UF · vendedor (opcional)
   │
   └─ Confirmação · autorização de consulta  →  [ Enviar solicitação ]
   │
   ▼  POST /api/solicitacoes
   │
   ├─ dado inválido ou CPF já cadastrado → mensagem de erro; a pessoa continua no formulário
   ├─ Aprovado    → /aprovado   próximos passos + resumo do pedido
   ├─ Em análise  → /analise    prazo de retorno + resumo do pedido
   └─ Negado      → /negado     oferta alternativa (DM Cred / Empréstimo Pessoal)
```

**Colaborador DM.** O formulário não tem campo "sou colaborador" nem matrícula. O servidor
identifica o colaborador pelo **CPF** informado, consultando a tabela `colaborador`, que o
administrador alimenta na aba *Adição de colaboradores*.

**Um CPF, uma solicitação.** Se o CPF já tem uma solicitação registrada, o envio é recusado
(HTTP 409) e a mensagem aparece no formulário.

**Por que as etapas seguem esta ordem.** A lista de lojas (etapa 4) depende da UF obtida pelo CEP
(etapa 3), e o DM Visa dispensa a etapa 4. Como parceiros da DM podem ter mais de 1000
estabelecimentos, a lista chega do servidor já filtrada por UF, em vez de carregar todas as
unidades no navegador.

**Página única, não wizard.** O plano original previa uma etapa por tela, com *Voltar* e
*Continuar*. A versão final mostra as quatro etapas na mesma página: o indicador de progresso no
topo leva, por âncora, a cada bloco, e a validação roda ao enviar, com a mensagem de erro junto
de cada campo.

---

## 5. Matriz de pré-qualificação

Regras extraídas de *Desafio do Parceiro Academico 2ADS - DM.pdf* e aplicadas no **servidor**
(`validar_cliente` em `app/services.py` e `processar_solicitacao` em `app/routes.py`). O
front-end não decide nada: ele envia o formulário e exibe a página do resultado.

| Cliente | Cartão DM (Visa) | Cartão Loja | Cartão Loja Digital |
|---|---|---|---|
| **Colaborador DM ativo** | **Aprovado** automático | **Negado** automático | **Negado** automático |
| **Não colaborador**, renda ≥ 1,5 × salário mínimo | Em análise | Em análise | Em análise |
| **Não colaborador**, renda < 1,5 × salário mínimo | Negado | Negado | Negado |

Como a decisão é tomada:

1. O CPF consta na tabela `colaborador` com `ativo = 1`? Então vale a primeira linha da matriz.
2. Se não, o servidor consulta o salário mínimo vigente na API de dados abertos do Banco Central
   e compara com a renda informada (limite de 1,5 × salário mínimo).
3. Se a consulta ao Banco Central falhar, a solicitação **não é negada**: vai para *Em análise*.

Os status gravados no banco são `Aprovado`, `Analise` e `Negado`.

**Quem decide o "Em análise".** O vendedor da unidade escolhida, no painel `/vendedor/painel`:
*Aprovar solicitação* ou *Recusar solicitação* (o motivo é obrigatório na recusa, e o status gravado é `Negado`). Só é possível decidir
solicitações da própria unidade que ainda estejam em análise.

> **Diferença para o texto do PDF.** O PDF diz que, para não colaboradores, "clientes
> considerados aptos na análise podem ser aprovados, o restante fica com status em análise". A
> implementação adota o desenho inverso: o cliente **apto** fica *Em análise* (e é aprovado ou
> negado pelo vendedor) e o **não apto** é *Negado* de imediato, passando a ver a oferta de
> outros produtos, que é um dos desafios extras do PDF.

### Restrições geográficas

| Cartão | Regra | Onde é aplicada |
|---|---|---|
| **DM Visa** | Aprovável em **qualquer estado** — é bandeirado e passa em qualquer lugar. Não exige loja: o campo "Loja parceira" fica desabilitado | O servidor descarta a loja enviada (`tratar_solicitacao`) |
| **Cartão Loja** | Só permite escolher unidades na **mesma UF** informada, que o formulário preenche a partir do CEP (é private label e só passa nas unidades do parceiro) | A lista é filtrada por UF (`/filtrar-lojas-parceiras/uf/<uf>?tipo=loja`) e o servidor confere de novo em `validar_loja_do_cartao` |
| **Cartão Loja Digital** | **Sem restrição de estado**. A interface deixa explícito que **não há cartão físico** | A lista traz todas as lojas digitais ativas (`tipo=loja_digital`) |

### Colaborador solicitando Cartão Loja Digital

O PDF define reprovação automática para "Cartão Loja" sem citar a variante digital. A
implementação trata **todo cartão diferente do DM Visa** como Cartão Loja; logo, o colaborador
ativo que pede o Loja Digital também é **negado automaticamente**. Para mudar essa regra basta
alterar uma condição em `validar_cliente` (`app/services.py`). Convém confirmar a decisão com o
PO (Davi), caso ainda não tenha sido formalizada.

---

## 6. Campos do formulário

### Etapa 1 — Tipo de cartão
`tipo_cartao` — radio, obrigatório: `dm_visa` | `loja` | `loja_digital`

### Etapa 2 — Dados pessoais
| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `nome` | text | sim | nome completo, no mínimo 5 caracteres |
| `cpf` | text | sim | máscara + dígito verificador conferido no navegador; o servidor exige 11 dígitos |
| `nascimento` | text | sim | formato DD/MM/AAAA; o servidor exige 18 anos ou mais |
| `email` | email | sim | — |
| `celular` | tel | sim | máscara (DD) 9XXXX-XXXX |
| `renda` | text | sim | em reais, maior que zero; usada na análise (1,5 × salário mínimo) |

### Etapa 3 — Endereço
| Campo | Obrigatório | Observação |
|---|---|---|
| `cep` | sim | ao sair do campo consulta `/consultar-cep/<cep>` (ViaCEP) |
| `logradouro`, `bairro`, `cidade` | sim | preenchidos pelo CEP, mas editáveis |
| `uf` | sim | `select`; preenchido pelo CEP; define a lista de lojas da etapa 4 |
| `numero` | sim | — |
| `complemento` | não | enviado, mas ainda não gravado no banco (ver seção 11) |

### Etapa 4 — Loja
| Campo | Obrigatório | Observação |
|---|---|---|
| `loja` | sim, exceto no DM Visa | `select`. No Cartão Loja o valor é a **unidade** escolhida; no Loja Digital, a **loja** digital |
| `vendedor` | não | texto livre; enviado, mas ainda não gravado (ver seção 11) |

### Confirmação
`consentimento` — checkbox obrigatório ("Autorizo a DM a consultar meus dados para a análise de
crédito desta solicitação").

### Onde cada validação acontece

| Onde | O que confere |
|---|---|
| Navegador (`main.js`, `util.js`) | cartão escolhido; nome; CPF com dígito verificador; e-mail; celular com DDD; renda maior que zero; CEP; rua, número, bairro, cidade e UF; loja (exceto DM Visa); consentimento |
| Servidor (`tratar_solicitacao`, `validar_loja_do_cartao`, `processar_solicitacao`) | data de nascimento válida e idade ≥ 18; CPF com 11 dígitos; tipo de cartão válido; loja obrigatória fora do DM Visa; unidade ou loja existente e ativa; mesma UF no Cartão Loja; CPF sem solicitação anterior |

---

## 7. Wireframes

### Landing page (desktop)

```text
┌──────────────────────────────────────────────────────────────┐
│ [dm]   Cartões  Benefícios  Como funciona  Dúvidas           │ azul
│            (Peça seu cartão) (Já sou cliente) [config]       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Toda história merece [crédito]          ┌──────────────┐    │
│  Peça seu cartão DM sem sair de casa.    │ foto: modelo │    │
│  *Sujeito à análise de crédito.          │ com o cartão │    │
│  ( Peça seu cartão )                     │              │    │
│                                          └──────────────┘    │
│                                                              │
├────────────┬────────────┬────────────┬────────────┬──────────┤
│   azul     │   coral    │  amarelo   │   aqua     │   verde  │
├────────────┴────────────┴────────────┴────────────┴──────────┤
│              Escolha o cartão ideal pra você                 │ branco
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐        │
│   │   DM Visa   │   │ Cartão Loja │   │Loja Digital │        │
│   │  qualquer   │   │só no estado │   │ sem cartão  │        │
│   │   estado    │   │ do seu CEP  │   │   físico    │        │
│   │  ( Pedir )  │   │  ( Pedir )  │   │  ( Pedir )  │        │
│   └─────────────┘   └─────────────┘   └─────────────┘        │
├──────────────────────────────────────────────────────────────┤
│              Um cartão, vários benefícios                    │ azul
│      6 cards: aprovação em minutos · limite automático ·     │
│      aproximação · código dinâmico · descontos · prazo       │
├──────────────────────────────────────────────────────────────┤
│   Peça agora, é fácil!                  [foto: modelo]       │ coral
│   1. Escolha o seu cartão               [com celular ]       │
│   2. Preencha seus dados                                     │
│   3. Receba a resposta na hora                               │
│   ( Peça seu cartão )                                        │
├──────────────────────────────────────────────────────────────┤
│   Sobre a DM                        [foto: colaboradores]    │ azul
├──────────────────────────────────────────────────────────────┤
│   Dúvidas frequentes (6 perguntas em acordeão)               │ lilás
│   > Quem pode pedir um cartão DM?                       (+)  │
│   > Por que só aparecem lojas do meu estado?            (+)  │
├──────────────────────────────────────────────────────────────┤
│   Pronto pra começar?   ( Peça seu cartão )                  │ azul
├──────────────────────────────────────────────────────────────┤
│   [dm]   Nossos produtos  |  Ajuda  |  aviso acadêmico       │ tinta
└──────────────────────────────────────────────────────────────┘
```

### Formulário (mobile) — etapas 3 e 4

```text
┌──────────────────────────┐   ┌──────────────────────────┐
│ ━━━━ ━━━━ ━━━━ ━━━━      │   │ Etapa 4 · Sua loja       │
│                          │   │                          │
│ Etapa 3 · Onde você      │   │ Loja parceira            │
│ está                     │   │ ┌──────────────────────┐ │
│                          │   │ │ Selecione...      v  │ │
│ CEP *                    │   │ └──────────────────────┘ │
│ ┌──────────────────────┐ │   │ Cartão Loja: só lojas    │
│ │ 12245-000            │ │   │ do estado do seu CEP.    │
│ └──────────────────────┘ │   │                          │
│ Rua ou avenida *         │   │ Vendedor (opcional)      │
│ ┌──────────────────────┐ │   │ ┌──────────────────────┐ │
│ │ (vem do CEP)         │ │   │ │                      │ │
│ └──────────────────────┘ │   │ └──────────────────────┘ │
│ Número *                 │   │                          │
│ ┌──────────────────────┐ │   │ [x] Autorizo a DM a      │
│ │                      │ │   │     consultar meus dados │
│ └──────────────────────┘ │   │ *Sujeito à análise de    │
│ Bairro, cidade e estado  │   │ crédito.                 │
│ (vêm do CEP)             │   │                          │
│                          │   │ ( Voltar )               │
└──────────────────────────┘   │ ( Enviar solicitação )   │
                               │                          │
                               └──────────────────────────┘
```

O indicador de progresso (as quatro barras no topo) reaproveita as cores da faixa multicolor.
Em "Loja parceira", cada opção aparece como *Nome — Cidade/UF (CEP)* no Cartão Loja e como
*Nome — Loja Digital* no Cartão Loja Digital.

### Resultado

```text
┌──────────────────────────────┐   ┌──────────────────────────────┐
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │   │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ Aprovado!                    │   │ Não foi dessa vez            │
│ Boa notícia: seu cartão foi  │   │ Não conseguimos aprovar seu  │
│ aprovado.                    │   │ cartão agora. Você pode      │
│                              │   │ tentar de novo em 90 dias.   │
│ Próximos passos              │   │                              │
│ 1. Confirme seu e-mail       │   │ Mas temos outras opções      │
│ 2. Separe um documento com   │   │ pra você                     │
│    foto para a retirada      │   │                              │
│ 3. Avisaremos quando o       │   │ DM Cred                      │
│    cartão estiver pronto     │   │ ( Conhecer o DM Cred )       │
│                              │   │ Empréstimo Pessoal           │
│ Protocolo            —       │   │ ( Simular empréstimo )       │
│ Cartão solicitado    ...     │   │                              │
│ Loja                 ...     │   │ [foto: homem com celular]    │
│                              │   │                              │
│ ( Voltar para o início )     │   │                              │
│                              │   │                              │
└──────────────────────────────┘   └──────────────────────────────┘
```

A borda superior do cartão de resultado muda de cor conforme o desfecho: verde (aprovado),
amarelo (em análise) e coral (negado). O campo *Protocolo* aparece como "—" (ver seção 11).

---

## 8. Sequência de entrega

| Sprint planejada | Subtarefa | Entrega | Situação no código |
|---|---|---|---|
| 1 | SCRUM-26 | Este documento | Entregue — `docs/escopo-frontend.md` |
| 1 | SCRUM-27 | Design tokens e assets da DM | Entregue — `docs/identidade-visual-dm.md`, `css/tokens.css`, `static/img/` |
| 1 | SCRUM-28 | `index.html` semântico, sem CSS | Entregue — `templates/index.html` |
| 1 | SCRUM-29 | Formulário e telas de resultado semânticos, sem CSS | Entregue — `solicita.html`, `aprovado.html`, `analise.html`, `negado.html` (e o legado `resultado.html`) |
| 2 | SCRUM-30 / SCRUM-31 | CSS base, componentes e responsividade | Entregue — `css/base.css` (SCRUM-30) e `css/components.css` (SCRUM-31) |
| 2 | *a criar* | JavaScript: wizard, validação, motor de regras, busca de loja | Parcial — validação, máscaras, CEP e lista de lojas estão em JS; o **motor de regras foi para o servidor**; wizard e busca de loja não foram implementados |
| 3 | *a criar* | Migração para Bootstrap 5 e integração com a API Flask | Parcial — integração com o Flask concluída; Bootstrap só nas telas restritas |

---

## 9. Integração com o back-end e o banco

### Rotas que o front-end consome

| Rota | Uso |
|---|---|
| `GET /consultar-cep/<cep>` | Preenche logradouro, bairro, cidade e UF a partir do CEP (ViaCEP) |
| `GET /filtrar-lojas-parceiras/uf/<uf>?tipo=…` | Monta a lista da etapa 4. Com `tipo=loja`, unidades físicas ativas da UF; com `tipo=loja_digital`, lojas digitais ativas |
| `POST /api/solicitacoes` | Envia o formulário (`FormData`). Em caso de sucesso, redireciona para `/aprovado`, `/analise` ou `/negado`. Em caso de erro, responde JSON `{"erro": "..."}` com status 400 (dado inválido) ou 409 (CPF já possui solicitação) |

Os formulários do painel administrativo enviam para `/api/adicao-parc`, `/api/adicao-colab` e
`/api/adicao-vendedor`, e usam `/api/buscar-lojas-vendedor` e `/api/buscar-unidades-loja/<id_loja>`
na busca de loja e de unidade do vendedor.

### Serviços externos

| Serviço | Para quê |
|---|---|
| ViaCEP | Endereço a partir do CEP (formulário e cadastro de unidades) |
| API de dados abertos do Banco Central | Salário mínimo vigente, para a análise de renda |
| Google Fonts | Fonte Catamaran |

### Cards de back-end e banco

- **SCRUM-6 (back-end):** o motor de decisão definitivo existe no servidor
  (`app/services.py` e `app/routes.py`). A camada `api.js` prevista não foi necessária: o
  formulário chama o servidor direto com `fetch` em `main.js`.
- **SCRUM-7 (banco):** lojas parceiras, unidades, colaboradores, vendedores e solicitações ficam
  no MySQL (`mysql/schema_cartoes.sql`). Os mocks previstos em `frontend/static/data/` não
  existem. O arquivo `app/mock_lojas.py` continua no repositório, mas nenhum código o utiliza.

---

## 10. Plano original × implementado

| Tema | Plano da Sprint 1 | Implementado |
|---|---|---|
| Arquivos | `frontend/index.html`, `solicitar.html` e `resultado.html` estáticos | Templates Flask em `app/frontend/templates/`, nas rotas `/`, `/solicitar`, `/aprovado`, `/analise` e `/negado` |
| Formulário | Wizard: uma etapa por tela, com *Voltar* e *Continuar* | Página única com 4 etapas numeradas; progresso por âncoras; validação ao enviar |
| Colaborador | Checkbox "Sou colaborador da DM" que revela o campo matrícula | Sem checkbox: o CPF é consultado na tabela `colaborador` |
| Motor de regras | JavaScript no navegador, atrás de uma camada `api.js` | Servidor (Flask + MySQL) |
| Tela de resultado | `resultado.html` com os três desfechos | Uma rota por desfecho (`/aprovado`, `/analise`, `/negado`) |
| Seleção de loja | Busca de loja parceira, filtrada pela UF | Lista suspensa filtrada por UF, sem campo de busca |
| Vendedor | Campo opcional (US SCRUM-12) | Campo de texto opcional no formulário, ainda não gravado, e portal do vendedor com login, ligado à unidade escolhida |
| Dados | Mocks em `frontend/static/data/` | MySQL |
| Bootstrap | Migração do front-end para Bootstrap 5 | Só nas telas restritas |

---

## 11. Limitações conhecidas

- **O link de cada cartão não pré-seleciona a opção.** Os CTAs da landing apontam para
  `/solicitar?cartao=dm_visa` (ou `loja`, `loja_digital`), mas nenhum script lê esse parâmetro:
  a pessoa precisa escolher o cartão de novo na etapa 1.
- **A lista de lojas é um `select` sem busca.** Para estados com muitas unidades, a lista fica
  longa.
- **O campo "vendedor" do formulário não é gravado.** O vínculo com o vendedor acontece pela
  **unidade** escolhida, que aparece no painel do vendedor correspondente.
- **O complemento do endereço não é gravado.** A tabela `endereco` não tem coluna para ele.
- **Avisos por e-mail e SMS, prazo de 48 horas e número de protocolo são apenas texto.** As telas
  de resultado descrevem esses avisos, mas a aplicação não envia mensagens nem gera protocolo (o
  campo aparece como "—").
- **Solicitações de DM Visa e de Cartão Loja Digital que ficam em análise não têm quem as
  decida.** O painel do vendedor lista apenas solicitações ligadas a uma unidade física (Cartão
  Loja), e o painel administrativo só consulta.
- **O Bootstrap só cobre as telas restritas.** As páginas públicas usam apenas o CSS próprio.