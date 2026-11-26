# 📌 MVP - Área do Vendedor e Ofertas Alternativas de Produtos (Sprint 3)

## 🎯 Objetivo do MVP

O MVP da terceira sprint consiste em evoluir a aplicação entregue na Sprint 2, permitindo ao administrador **cadastrar vendedores** vinculados às unidades das lojas parceiras e dando a esses vendedores uma **área própria** para acompanhar e decidir as requisições de cartão da sua unidade. A sprint apresenta ainda **outros produtos DM** ao cliente cuja requisição seja reprovada.

Nesta terceira versão, a aplicação deverá:

- Permitir ao administrador **cadastrar vendedores** e vinculá-los a uma unidade de uma loja parceira, para atribuir os PACs aos respetivos vendedores.
- Disponibilizar uma **área do vendedor**, com acesso por e-mail e CPF, onde as requisições da unidade são visualizadas e as que estão em análise são aprovadas ou negadas.
- Apresentar **ofertas de outros produtos** (DM Cred e Empréstimo Pessoal) ao cliente com requisição reprovada.
- Manter intactas as regras das Sprints 1 e 2 (restrição geográfica do Cartão Loja, Cartão Loja Digital, Cartão DM e regras para colaboradores DM).

O objetivo central deste MVP é **fechar o ciclo da requisição**: cada PAC feito numa unidade física passa a ser analisado por um vendedor dessa unidade, e o cliente reprovado deixa de ficar sem alternativas.

---

## 📝 Descrição da Solução

A aplicação mantém a base tecnológica das sprints anteriores: aplicação Web em Python (Flask) com interface gráfica em HTML5, CSS3, JavaScript e Bootstrap, integrada com uma base de dados relacional MySQL. A Sprint 3 estende o **painel administrativo** (`/admin`) com as abas de vendedores e de colaboradores, cria a **área do vendedor** (`/vendedor`) e altera o modelo de dados para incluir as **unidades físicas** das lojas parceiras (tabela `unidade_loja`).

**Funcionalidades principais incluídas (Sprint 3)**
- Formulário de cadastro de vendedores no painel administrativo (loja parceira, unidade, nome, CPF e e-mail).
- Área do vendedor com login por e-mail e CPF, resumo e listagem das requisições da sua unidade.
- Decisão sobre requisições em análise: aprovar, ou negar com motivo obrigatório, ficando registados o vendedor responsável e o motivo.
- Ofertas de outros produtos DM na tela de requisição reprovada e faixa "Conheça também" nas telas de resultado.
- Cadastro das unidades físicas dos parceiros por CEP, manualmente ou por importação de arquivo CSV (até 200 unidades por cadastro), com cidade e estado obtidos pelo ViaCEP.
- Cadastro de colaboradores DM (matrícula e CPF) no painel administrativo, base da aprovação automática do Cartão DM.
- Gravação do endereço informado pelo cliente.

**Limitações conhecidas**
- A edição e a exclusão de parceiros, unidades, vendedores e colaboradores não fazem parte desta sprint (apenas cadastro).
- O acesso administrativo continua a usar uma única senha partilhada, sem utilizadores ou perfis individuais; o vendedor acede com e-mail e CPF, sem senha.
- As requisições em análise do Cartão DM e do Cartão Loja Digital não pertencem a nenhuma unidade e, por isso, não aparecem na área do vendedor.
- O campo Vendedor do formulário do cliente ainda não é gravado; a requisição fica ligada à unidade escolhida e ao vendedor que a decide.
- O complemento do endereço informado pelo cliente não é gravado.

---

## 👥 Personas / Utilizadores-Alvo

- **Cliente:** procura uma forma simples e transparente de solicitar o cartão e, caso seja reprovado, de conhecer outros produtos que se encaixem no seu momento.
- **Vendedor:** pretende acompanhar as requisições feitas na sua unidade e decidir rapidamente as que estão em análise.
- **Administrador:** pretende cadastrar vendedores, unidades e colaboradores sem recorrer ao banco de dados nem à equipa de desenvolvimento.
- **Responsável pela Análise de Cartões:** necessita de saber quem decidiu cada requisição e com que justificativa.
- **Parceiro Lojista:** pretende que as requisições feitas nas suas unidades sejam analisadas por vendedores dessas mesmas unidades.

---

## 🔑 User Stories (Backlog do MVP - Sprint 3)

| ID | User Story | Prioridade | Estimativa |
|---|---|---|---|
| US11 | Como administrador, quero cadastrar vendedores quando existirem, para atribuir os PACs aos respectivos vendedores. | Média | 3 pontos |
| US12 | Como cliente, quero receber ofertas de outros produtos mesmo que minha requisição de cartão seja reprovada, para conhecer outras opções disponíveis. | Baixa | 5 pontos |

**Total planejado:** 8 pontos (capacidade da sprint: 15 pontos).

---

## 🏅 DoR - Definition of Ready <a id="dor"></a>

| Critério | Descrição |
| :---: | --- |
| User Stories Definidas | User Stories possuem **Critérios de Aceitação** especificados e estruturados. |
| Decomposição em Tarefas | Subtarefas devidamente divididas a partir das US no Jira. |
| Mapeamento de Fluxos | Mapeamento das rotas do painel administrativo e da área do vendedor concluído. |
| Ambiente Configurado | Ambiente configurado com ficheiro **.env** (Dotenv, incluindo `ADMIN_PASSWORD` e `FLASK_SECRET_KEY`), dependências registadas no **requirements.txt** e dados iniciais carregados na base de dados. |
| Integração Git/Jira | Repositório no **GitHub** com branches criadas e associadas aos respetivos cards do Jira. |

---

## 🏅 DoD - Definition of Done <a id="dod"></a>

| Critério | Descrição |
| :---: | --- |
| Código Revisado | Código completo, limpo e devidamente **revisado** no GitHub, com consultas SQL parametrizadas nas novas rotas. |
| Testes Funcionais | Funcionalidade **testada e a funcionar** na aplicação Web, incluindo os cenários de cadastro de vendedores, decisão das requisições e ofertas alternativas. |
| Servidor & Rotas | Rotas do servidor **Flask** a responder corretamente, com as rotas administrativas e da área do vendedor protegidas por autenticação. |
| Documentação Atualizada | **Manual de Instalação** e **Manual do Usuário** atualizados com o fluxo do administrador (parceiros, colaboradores e vendedores) e o fluxo do vendedor. |
| Rastreabilidade | Card da US **fechado e atualizado no Jira**. |
| Evidências / Demonstração | Vídeo da entrega da Sprint gravado e disponibilizado. |

---

## 📅 Sprint(s) Relacionadas

| Sprint | Entregas Principais | Estado |
|---|---|---|
| 01 | Landing Page, formulário, aprovação automática e regras de elegibilidade (US1 a US7) — [MVP](sp1.md) | Concluída ✅ |
| 02 | Elegibilidade nacional do Cartão DM, adição de parceiros (US9 e US10) — [MVP](sp2.md) | Concluída ✅ |
| 03 | Cadastro de vendedores, área do vendedor e ofertas de outros produtos (US11 e US12) | Concluída ✅ |

**Previsão de entrega da Sprint 3:** 22/11/2026.

---

## 📊 Critérios de Aceitação

**US11 — Cadastro de vendedores e atribuição dos PACs**
- Apenas o administrador autenticado acede ao formulário de cadastro e às buscas de loja e de unidade; o acesso sem autenticação é bloqueado.
- O vendedor só é cadastrado com nome, CPF, e-mail e unidade; todos os campos são obrigatórios.
- Só podem ser selecionadas lojas físicas e unidades ativas.
- Um CPF ou e-mail já cadastrado é rejeitado com mensagem clara.
- O vendedor acede à área do vendedor com o e-mail e o CPF cadastrados e visualiza apenas as requisições da sua unidade.
- Apenas requisições em análise da própria unidade podem ser decididas; a negativa exige um motivo.
- A decisão grava o vendedor responsável e o motivo na requisição.

**US12 — Ofertas de outros produtos**
- O cliente com requisição reprovada visualiza as ofertas de DM Cred e Empréstimo Pessoal na tela de resultado.
- As ofertas abrem o portal da DM em outra aba.
- A faixa "Conheça também" aparece nas telas de resultado, pode ser fechada e não volta a aparecer na mesma sessão do navegador.

**Gerais**
- As requisições continuam a ser registadas na base de dados MySQL com os respetivos estados (aprovado, reprovado ou em análise).

---

## 📈 Métricas de Validação

- Execução com sucesso dos fluxos de cadastro de vendedor, login na área do vendedor e decisão de requisições, nas rotas Flask e no frontend.
- Vendedor visualizando somente as requisições da sua unidade e decisão registada com o vendedor e o motivo.
- Requisição já decidida não podendo ser alterada novamente.
- Rejeição de CPF ou e-mail de vendedor duplicado e de acesso administrativo sem autenticação.
- Tela de requisição reprovada exibindo as ofertas de outros produtos.
- Cadastro de parceiro com unidades informadas manualmente e por arquivo CSV.
- Conformidade do código com os padrões definidos pelo projeto.

---

## 🚀 Próximos Passos

- Preparação da apresentação final para a Feira de Soluções (03/12/2026).
- Avaliar a edição e a exclusão de parceiros, unidades, vendedores e colaboradores.
- Avaliar a autenticação individual dos administradores e uma senha própria para os vendedores.

## 📂 Anexos / Evidências

**Vídeo de Demonstração**\
Confira o website em funcionamento: https://youtu.be/BsbRDVgEaKY?is=V3749dAZOJOLU9hx