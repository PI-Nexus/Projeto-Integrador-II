# 📌 MVP - Gestão de Parceiros, Vendedores e Elegibilidade Nacional do Cartão DM (Sprint 2)

## 🎯 Objetivo do MVP

O MVP da segunda sprint consiste em evoluir a Landing Page entregue na Sprint 1, tornando a **adesão de novos parceiros** e a **atribuição de vendedores** processos autónomos, geridos através de um painel administrativo e sem depender de intervenção direta no banco de dados pela equipa de desenvolvimento. A sprint consolida ainda a regra de **elegibilidade nacional do Cartão DM**.

Nesta segunda versão, a aplicação deverá:

- Permitir ao administrador **adicionar parceiros** (lojas físicas e digitais) de forma simples, para que os clientes consigam realizar um PAC para o estabelecimento logo após o cadastro.
- Permitir ao administrador **cadastrar vendedores** associados aos parceiros, quando existirem.
- Permitir que o PAC seja **atribuído ao vendedor** que atendeu o cliente, ficando registado na base de dados e visível no painel.
- Garantir que o **Cartão DM possa ser aprovado independentemente da localização** do cliente.
- Manter intactas as regras da Sprint 1 (restrição geográfica do Cartão Loja, Cartão Loja Digital e regras para colaboradores DM).

O objetivo central deste MVP é **eliminar a dependência da equipa de desenvolvimento** para incluir novos parceiros nas jornadas de captação, garantindo que as regras de negócio continuam a ser aplicadas corretamente a cada novo estabelecimento.

---

## 📝 Descrição da Solução

A aplicação mantém a base tecnológica da Sprint 1: aplicação Web em Python (Flask) com interface gráfica em HTML5, CSS3, JavaScript e Bootstrap, integrada com uma base de dados relacional MySQL. A Sprint 2 estende o **painel administrativo** (`/admin`, protegido por senha definida na variável `ADMIN_PASSWORD`) com os módulos de parceiros e vendedores, e liga o campo **Vendedor** do formulário às requisições registadas.

**Funcionalidades principais incluídas (Sprint 2)**
- Formulário de cadastro de parceiros no painel administrativo (nome, CNPJ, cidade/UF, tipo físico ou digital e descrição).
- Listagem dos parceiros cadastrados.
- Disponibilização imediata do novo parceiro na Etapa 4 do formulário, respeitando as regras geográficas (físico: apenas clientes do mesmo estado) e digitais (sem restrição de estado).
- Formulário de cadastro de vendedores vinculados a um parceiro.
- Atribuição do PAC ao vendedor, com gravação na base de dados e coluna **Vendedor** na lista de solicitações do painel.
- Elegibilidade nacional do Cartão DM, aplicada no servidor e validada por cenários de teste (sem restrição de estado e sem exigência de loja).

**Modelo de dados (proposta)**

| Tabela | Alteração |
|---|---|
| `loja` | Reaproveitada. Já possui nome, CNPJ, estado, cidade, descrição e indicador de loja digital; passa a ser alimentada pelo painel administrativo. |
| `vendedor` *(nova)* | Identificador, nome, código do vendedor, parceiro (FK para `loja`) e estado (ativo/inativo). |
| `solicitacao_cartao` | Nova coluna `id_vendedor` (FK para `vendedor`, aceita nulo, pois o vendedor é opcional). |

**Limitações conhecidas**
- Apresentação de ofertas alternativas para clientes reprovados fora do escopo (escopo da Sprint 3).
- O cadastro de parceiros é feito um a um; a importação em lote (por exemplo, via CSV) não está incluída, embora existam unidades parceiras com mais de 1000 estabelecimentos.
- A edição e a exclusão de parceiros e vendedores não fazem parte desta sprint (apenas cadastro e listagem).
- O acesso administrativo continua a usar uma única senha partilhada, sem utilizadores ou perfis individuais.

---

## 👥 Personas / Utilizadores-Alvo

- **Cliente:** procura uma forma simples e transparente de solicitar o cartão e, quando foi atendido por um vendedor, de o identificar no pedido.
- **Responsável pela Análise de Cartões:** necessita de ter a certeza de que o Cartão DM é avaliado apenas pelas regras de pré-qualificação, sem bloqueios por localização.
- **Administrador:** pretende incluir novos parceiros e vendedores no sistema sem recorrer ao banco de dados nem à equipa de desenvolvimento.
- **Parceiro Lojista:** pretende que o seu estabelecimento fique disponível para captação assim que for cadastrado, com as regras geográficas e de canal (físico ou digital) corretamente aplicadas.
- **Vendedor:** pretende que os PACs que atendeu fiquem atribuídos a si.

---

## 🔑 User Stories (Backlog do MVP - Sprint 2)

| ID | User Story | Prioridade | Estimativa |
|---|---|---|---|
| US8 | Como responsável pela análise de cartões, quero que cartões DM possam ser aprovados independentemente da localização do cliente. | Alta | 2 pontos |
| US9 | Como administrador, quero adicionar parceiros ao sistema de forma simples, para permitir que os clientes realizem um PAC para o estabelecimento. | Média | 5 pontos |
| US10 | Como administrador, quero cadastrar vendedores quando existirem, para atribuir os PACs aos respetivos vendedores. | Média | 3 pontos |

**Total planejado:** 10 pontos (capacidade da sprint: 15 pontos).

---

## 🏅 DoR - Definition of Ready <a id="dor"></a>

| Critério | Descrição |
| :---: | --- |
| User Stories Definidas | User Stories possuem **Critérios de Aceitação** especificados e estruturados. |
| Decomposição em Tarefas | Subtarefas devidamente divididas a partir das US no Jira. |
| Mapeamento de Fluxos | Mapeamento das rotas do painel administrativo (parceiros e vendedores) e do modelo de dados (`loja`, `vendedor`, `solicitacao_cartao`) concluído. |
| Ambiente Configurado | Ambiente configurado com ficheiro **.env** (Dotenv, incluindo `ADMIN_PASSWORD` e `FLASK_SECRET_KEY`), dependências registadas no **requirements.txt** e dados iniciais carregados na base de dados. |
| Integração Git/Jira | Repositório no **GitHub** com branches criadas e associadas aos respetivos cards do Jira. |

---

## 🏅 DoD - Definition of Done <a id="dod"></a>

| Critério | Descrição |
| :---: | --- |
| Código Revisado | Código completo, limpo e devidamente **revisado** no GitHub, com consultas SQL parametrizadas nas novas rotas. |
| Testes Funcionais | Funcionalidade **testada e a funcionar** na aplicação Web, incluindo os cenários de elegibilidade e de cadastro. |
| Servidor & Rotas | Rotas do servidor **Flask** a responder corretamente, com as rotas administrativas protegidas por autenticação. |
| Documentação Atualizada | **Manual de Instalação** e **Manual do Usuário** atualizados com o fluxo do administrador (cadastro de parceiros e vendedores) e com as alterações de base de dados. |
| Rastreabilidade | Card da US **fechado e atualizado no Jira**. |
| Evidências / Demonstração | Vídeo da entrega da Sprint gravado e disponibilizado. |

---

## 📅 Sprint(s) Relacionadas

| Sprint | Entregas Principais | Estado |
|---|---|---|
| 01 | Landing Page, formulário, aprovação automática e regras de elegibilidade (US1 a US7) — [MVP](sp2.md) | Em andamento 🟡 |
| 02 | Elegibilidade nacional do Cartão DM, adição de parceiros e cadastro de vendedores (US8 a US10) | A fazer |

**Previsão de entrega da Sprint 2:** 25/10/2026.

---

## 📊 Critérios de Aceitação

**US8 — Cartão DM independente da localização**
- O Cartão DM pode ser solicitado e processado com CEP de qualquer estado, sem exigir a seleção de loja.
- O resultado depende apenas das regras de pré-qualificação (colaborador DM ou análise por renda), nunca do estado do cliente.
- A restrição geográfica continua a aplicar-se somente ao Cartão Loja.

**US9 — Adição de parceiros**
- Apenas o administrador autenticado acede ao formulário de cadastro; o acesso sem autenticação é bloqueado.
- Os campos obrigatórios (nome, CNPJ válido, cidade/UF e tipo físico ou digital) são validados antes da gravação.
- Um CNPJ já cadastrado é rejeitado com mensagem clara.
- O parceiro físico aparece no formulário apenas para clientes do mesmo estado; o parceiro digital aparece para todos, com o aviso de que não há cartão físico.
- O parceiro é gravado na base de dados e fica disponível para captação sem alteração de código nem acesso direto ao banco.

**US10 — Cadastro e atribuição de vendedores**
- O administrador cadastra um vendedor vinculado a um parceiro existente.
- O vendedor é opcional: um PAC sem vendedor continua a ser registado normalmente.
- Quando o vendedor é informado, só é aceite se pertencer à loja escolhida, e o PAC fica gravado com essa atribuição.
- O painel administrativo apresenta o vendedor em cada solicitação.

**Gerais**
- As requisições continuam a ser registadas na base de dados MySQL com os respetivos estados (aprovado, reprovado ou em análise).

---

## 📈 Métricas de Validação

- Execução com sucesso dos fluxos de cadastro (parceiro e vendedor) e de requisição no frontend e rotas Flask.
- Cartão DM processado com CEPs de diferentes estados (por exemplo, SP, AM e RS) com o mesmo resultado para o mesmo perfil de cliente.
- Parceiro físico recém-cadastrado visível apenas no seu estado e parceiro digital recém-cadastrado visível em todos os estados.
- Rejeição de CNPJ duplicado e de acesso administrativo sem autenticação.
- PAC com vendedor gravado com a atribuição correta e PAC sem vendedor registado sem erros.
- Conformidade do código com os padrões definidos pelo projeto.

---

## 🚀 Próximos Passos

- Desenvolvimento do sistema de apresentação de ofertas alternativas de produtos para clientes reprovados (Sprint 3).
- Avaliar a importação em lote de estabelecimentos para parceiros com grande número de unidades.
- Preparação da apresentação final para a Feira de Soluções (03/12/2026).

---

## 📂 Anexos / Evidências

**Vídeo de Demonstração**\
Confira o website em funcionamento: