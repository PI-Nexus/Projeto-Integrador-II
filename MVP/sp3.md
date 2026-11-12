# 📌 MVP - Gestão de Vendedores e Ofertas Alternativas para Clientes Reprovados (Sprint 3)

## 🎯 Objetivo do MVP

O MVP da terceira sprint consiste em evoluir a aplicação entregue na Sprint 2, permitindo ao administrador **cadastrar vendedores** pelo painel administrativo, quando existirem, para que os **PACs sejam atribuídos aos respectivos vendedores**, e garantindo que o cliente com a requisição de cartão reprovada **receba ofertas de outros produtos**, em vez de encerrar a jornada sem alternativas. A sprint contempla as duas últimas user stories do backlog planejado (US11 e US12) e antecede a apresentação final na Feira de Soluções.

Nesta terceira versão, a aplicação deverá:

- Permitir ao administrador **cadastrar vendedores** de forma simples, quando existirem, vinculando cada um ao parceiro (loja) em que atua.
- Permitir que o cliente **identifique o vendedor** que o atendeu, para que o PAC seja **atribuído ao respectivo vendedor**.
- Apresentar **ofertas de outros produtos** ao cliente cuja requisição de cartão seja reprovada, para que conheça outras opções disponíveis.
- Manter intactas as regras das Sprints 1 e 2 (restrição geográfica do Cartão Loja, Cartão Loja Digital, elegibilidade nacional do Cartão DM, regras para colaboradores DM e cadastro de parceiros).

O objetivo central deste MVP é **permitir a atribuição dos PACs aos vendedores sem depender da equipe de desenvolvimento** e **oferecer alternativas ao cliente reprovado**, garantindo que as regras de negócio continuam sendo aplicadas corretamente.

---

## 📝 Descrição da Solução

A aplicação mantém a base tecnológica das Sprints anteriores: aplicação Web em Python (Flask) com interface gráfica em HTML5, CSS3, JavaScript e Bootstrap, integrada com um banco de dados relacional MySQL. A Sprint 3 estende o **painel administrativo** (`/admin`, protegido por senha definida na variável `ADMIN_PASSWORD`) com o módulo de **vendedores**, liga o campo **Vendedor** do formulário aos vendedores cadastrados e atualiza a página de resultado das requisições reprovadas (`negado`) com a apresentação de **ofertas de outros produtos**.

**Funcionalidades principais incluídas (Sprint 3)**
- Formulário de cadastro de vendedores no painel administrativo (nome e parceiro ao qual o vendedor está vinculado).
- Campo Vendedor no formulário de requisição, listando apenas os vendedores do parceiro selecionado, quando existirem.
- Atribuição do PAC ao vendedor escolhido e visualização dessa atribuição no painel administrativo.
- Apresentação de ofertas de outros produtos na página de resultado das requisições reprovadas, respeitando as regras de elegibilidade do cliente.

**Limitações conhecidas**
- O cadastro de parceiros e de vendedores é feito um a um; a importação em lote (por exemplo, via CSV) não está incluída, embora existam unidades parceiras com mais de 1000 estabelecimentos.
- A edição e a exclusão de parceiros e de vendedores não fazem parte desta sprint (apenas cadastro).
- O acesso administrativo continua utilizando uma única senha compartilhada, sem usuários ou perfis individuais.
- As ofertas de outros produtos têm caráter informativo: a contratação dos produtos ofertados e a gestão do catálogo de ofertas pelo painel administrativo não fazem parte desta sprint.

---

## 👥 Personas / Utilizadores-Alvo

- **Cliente:** procura uma forma simples e transparente de solicitar o cartão e, quando foi atendido por um vendedor, de identificá-lo no pedido; se a requisição for reprovada, quer conhecer outras opções de produtos disponíveis.
- **Responsável pela Análise de Cartões:** necessita ter a certeza de que a apresentação de ofertas não altera o resultado da análise: a requisição reprovada continua registrada como reprovada e as regras de elegibilidade permanecem inalteradas.
- **Administrador:** pretende cadastrar os vendedores dos parceiros e acompanhar a quais vendedores os PACs foram atribuídos, sem recorrer ao banco de dados nem à equipe de desenvolvimento.
- **Vendedor (quando existir):** pretende que os PACs captados por si sejam atribuídos ao seu nome.
- **Parceiro Lojista:** pretende que os PACs do seu estabelecimento sejam associados aos respectivos vendedores, com as regras geográficas e de canal (físico ou digital) corretamente aplicadas.

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
| Mapeamento de Fluxos | Mapeamento das rotas do painel administrativo (vendedores) e do fluxo de resultado das requisições reprovadas concluído. |
| Ambiente Configurado | Ambiente configurado com arquivo **.env** (Dotenv, incluindo `ADMIN_PASSWORD` e `FLASK_SECRET_KEY`), dependências registradas no **requirements.txt** e dados iniciais (incluindo os parceiros da Sprint 2) carregados no banco de dados. |
| Integração Git/Jira | Repositório no **GitHub** com branches criadas e associadas aos respectivos cards do Jira. |

---

## 🏅 DoD - Definition of Done <a id="dod"></a>

| Critério | Descrição |
| :---: | --- |
| Código Revisado | Código completo, limpo e devidamente **revisado** no GitHub, com consultas SQL parametrizadas nas novas rotas. |
| Testes Funcionais | Funcionalidade **testada e funcionando** na aplicação Web, incluindo os cenários de cadastro de vendedores, de atribuição do PAC e de apresentação de ofertas para requisições reprovadas. |
| Servidor & Rotas | Rotas do servidor **Flask** respondendo corretamente, com as rotas administrativas protegidas por autenticação. |
| Documentação Atualizada | **Manual de Instalação** e **Manual do Usuário** atualizados com o fluxo do administrador (cadastro de vendedores) e com as ofertas apresentadas ao cliente reprovado. |
| Rastreabilidade | Card da US **fechado e atualizado no Jira**. |
| Evidências / Demonstração | Vídeo da entrega da Sprint gravado e disponibilizado. |

---

## 📅 Sprint(s) Relacionadas

| Sprint | Entregas Principais | Estado |
|---|---|---|
| 01 | Landing Page, formulário, aprovação automática e regras de elegibilidade (US1 a US8) — [MVP](sp1.md) | Concluída ✅ |
| 02 | Dashboard administrativo, adição de parceiros e consolidação da elegibilidade nacional do Cartão DM (US9 e US10) — [MVP](sp2.md) | Concluída ✅ |
| 03 | Cadastro de vendedores e ofertas de outros produtos para clientes reprovados (US11 e US12) | Em andamento 🟡 |

**Previsão de entrega da Sprint 3:** 22/11/2026.

---

## 📊 Critérios de Aceitação

**US11 — Cadastro de Vendedores e Atribuição de PACs**
- Apenas o administrador autenticado acessa o formulário de cadastro de vendedores; o acesso sem autenticação é bloqueado.
- Os campos obrigatórios (nome do vendedor e parceiro ao qual está vinculado) são validados antes da gravação.
- O vendedor só pode ser vinculado a um parceiro já cadastrado.
- Um vendedor já cadastrado no mesmo parceiro é rejeitado com mensagem clara.
- O vendedor é gravado no banco de dados e fica disponível para atribuição de PACs sem alteração de código nem acesso direto ao banco.
- No formulário de requisição, o campo Vendedor lista apenas os vendedores do parceiro selecionado, e o servidor rejeita um vendedor que não pertença ao parceiro escolhido.
- Quando o parceiro não possui vendedores cadastrados, o campo Vendedor é opcional e a requisição segue normalmente.
- O PAC é gravado com a atribuição ao vendedor selecionado, e essa atribuição é exibida no painel administrativo.
- A atribuição a um vendedor não altera as regras de aprovação e elegibilidade: o resultado é o mesmo com ou sem vendedor.

**US12 — Ofertas de Outros Produtos para Clientes Reprovados**
- Quando a requisição é reprovada, a página de resultado (`negado`) apresenta ao cliente ofertas de outros produtos, mantendo a informação da reprovação.
- As ofertas apresentadas respeitam as regras de elegibilidade do cliente (por exemplo, um produto com restrição geográfica não é ofertado a um cliente de outro estado).
- Cada oferta apresenta o nome e uma breve descrição do produto, para que o cliente conheça as opções disponíveis.
- A apresentação das ofertas não altera o estado da requisição, que continua registrada como reprovada.
- Clientes com requisição aprovada ou em análise não visualizam ofertas: o fluxo desses resultados permanece inalterado.

**Gerais**
- As requisições continuam sendo registradas no banco de dados MySQL com os respectivos estados (aprovado, reprovado ou em análise).
- As regras das Sprints 1 e 2 (restrição geográfica do Cartão Loja, Cartão Loja Digital, elegibilidade nacional do Cartão DM e regras para colaboradores DM) continuam sendo aplicadas sem alterações.

---

## 📈 Métricas de Validação

- Execução com sucesso dos fluxos de cadastro (vendedor) e de requisição no frontend e rotas Flask.
- Vendedor recém-cadastrado listado apenas no formulário do parceiro ao qual está vinculado, com o PAC gravado e a atribuição visível no painel administrativo.
- Requisição em parceiro sem vendedores cadastrados concluída normalmente, com o mesmo resultado de elegibilidade.
- Rejeição de vendedor duplicado no mesmo parceiro e de acesso administrativo sem autenticação.
- Cliente reprovado (por exemplo, ao solicitar o Cartão Loja fora do estado da loja) visualizando ofertas de outros produtos compatíveis com o seu perfil, com a requisição mantida como reprovada.
- Fluxos de requisições aprovadas e em análise sem alteração.
- Regras das Sprints 1 e 2 (Cartão Loja, Cartão Loja Digital, Cartão DM e colaboradores DM) com os mesmos resultados nos cenários de teste anteriores.
- Conformidade do código com os padrões definidos pelo projeto.

---

## 🚀 Próximos Passos

- Preparação da apresentação final para a Feira de Soluções (03/12/2026).
- Avaliar a importação em lote de estabelecimentos e de vendedores para parceiros com grande número de unidades.
- Avaliar a edição e a exclusão de parceiros e de vendedores no painel administrativo.
- Avaliar o acesso administrativo com usuários e perfis individuais, em substituição à senha compartilhada.
- Avaliar a gestão do catálogo de ofertas pelo painel administrativo e a personalização das ofertas conforme o perfil do cliente.

---

## 📂 Anexos / Evidências

**Vídeo de Demonstração**\
Confira o website em funcionamento: 