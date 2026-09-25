# 📌 MVP - Landing Page de Captação e Pré-Qualificação de Clientes (Sprint 1)

## 🎯 Objetivo do MVP

O MVP da primeira sprint consiste em disponibilizar uma **Landing Page funcional e intuitiva** para captação e pré-qualificação de clientes, capaz de permitir a seleção do cartão pretendido, preenchimento do formulário de requisição e aplicação automática de regras de aprovação e elegibilidade com base nos dados do cliente e nas diretrizes dos parceiros.

Nesta primeira versão, a aplicação deverá:

- Apresentar uma **Landing Page clara e atrativa** detalhando as principais funcionalidades e produtos.
- Permitir a **seleção do tipo de cartão** pretendido pelo cliente.
- Disponibilizar um **formulário simples e intuitivo** para recolha dos dados necessários.
- Processar e aplicar automaticamente as **regras de aprovação/reprovação e elegibilidade** (incluindo validações geográficas por estado/loja, cartões digitais e cartões DM).
- Permitir a **visualização e acompanhamento das requisições** (clientes aptos e em análise).

O objetivo central deste MVP é **simplificar o processo de adesão de clientes**, garantindo uma experiência fluida e a correta aplicação das regras de negócio de forma automatizada.

---

## 📝 Descrição da Solução

Será desenvolvida uma aplicação Web em Python (Flask) com interface gráfica em HTML5, CSS3, JavaScript e Bootstrap, integrada com uma base de dados relacional MySQL. A solução irá verificar a pré-qualificação dos clientes e encaminhar os processos de forma automática.

**Funcionalidades principais incluídas (Sprint 1)**
- Apresentação da Landing Page do produto.
- Seleção do tipo de cartão.
- Formulário de registo e envio de dados do cliente.
- Motor de regras para aprovação e reprovação automática.
- Painel/módulo de visualização de clientes aptos e em análise.
- Regras de restrição geográfica por loja/estado para parceiros.
- Elegibilidade nacional para cartões digitais e cartões DM.

**Limitações conhecidas**
- Módulo de adição de parceiros e vendedores ainda não incluído (escopo da Sprint 2).
- Apresentação de ofertas alternativas para clientes reprovados fora do escopo (escopo da Sprint 3).

---

## 👥 Personas / Utilizadores-Alvo

- **Cliente:** procura uma forma simples, rápida e transparente de conhecer os produtos e solicitar o cartão adequado às suas necessidades.
- **Responsável pela Análise de Cartões:** necessita de acompanhar os pedidos, visualizando rapidamente quais os clientes aptos ou em análise.
- **Parceiro Lojista:** pretende assegurar que as regras geográficas e de canal (físico ou digital) sejam devidamente aplicadas no momento da requisição.

---

## 🔑 User Stories (Backlog do MVP - Sprint 1)

| ID | User Story | Prioridade | Estimativa |
|---|---|---|---|
| US1 | Como cliente, quero aceder a uma landing page clara e atrativa, para conhecer o produto e entender as suas principais funcionalidades. | Alta | 5 pontos |
| US2 | Como cliente, quero escolher qual o tipo de cartão desejo requisitar, para iniciar o processo adequado às minhas necessidades. | Alta | 3 pontos |
| US3 | Como cliente, quero preencher um formulário simples e intuitivo, para enviar os dados necessários à minha requisição. | Alta | 5 pontos |
| US4 | Como responsável pela análise de cartões, quero que o sistema aprove ou reprove automaticamente os clientes com base no cartão selecionado e nas regras de elegibilidade. | Alta | 8 pontos |
| US5 | Como responsável pela análise de cartões, quero visualizar quais os clientes que estão aptos e quais estão em análise, para acompanhar as requisições. | Alta | 5 pontos |
| US6 | Como parceiro, quero que apenas clientes do mesmo estado da minha loja possam requisitar cartões com restrição geográfica. | Alta | 3 pontos |
| US7 | Como parceiro, quero permitir que clientes requisitem o meu cartão digital independentemente da sua localização. | Alta | 2 pontos |

---

## 🏅 DoR - Definition of Ready <a id="dor"></a>

| Critério | Descrição |
| :---: | --- |
| User Stories Definidas | User Stories possuem **Critérios de Aceitação** especificados e estruturados. |
| Decomposição em Tarefas | Subtarefas devidamente divididas a partir das US no Jira. |
| Mapeamento de Fluxos | Mapeamento de rotas e fluxo da landing page e validação de elegibilidade concluído. |
| Ambiente Configurado | Ambiente configurado com ficheiro **.env** (Dotenv) e dependências registadas no **requirements.txt**. |
| Integração Git/Jira | Repositório no **GitHub** com branches criadas e associadas aos respetivos cards do Jira. |

---

## 🏅 DoD - Definition of Done <a id="dod"></a>

| Critério | Descrição |
| :---: | --- |
| Código Revisado | Código completo, limpo e devidamente **revisado** no GitHub. |
| Testes Funcionais | Funcionalidade **testada e a funcionar** na aplicação Web. |
| Servidor & Rotas | Rotas do servidor **Flask** a responder corretamente. |
| Documentação Atualizada | **Manual de Instalação** e **Manual do Usuário** com instruções de instalação, configuração e execução local concluídos. |
| Rastreabilidade | Card da US **fechado e atualizado no Jira**. |
| Evidências / Demonstração | Vídeo da entrega da Sprint gravado e disponibilizado. |

---

## 📅 Sprint(s) Relacionadas

| Sprint | Entregas Principais | Estado |
|---|---|---|
| 01 | Landing Page, formulário, aprovação automática e regras de elegibilidade (US1 a US7) | Em Andamento 🟡 |

---

## 📊 Critérios de Aceitação

- A Landing Page deve carregar corretamente e permitir a navegação fluida.
- O formulário deve recolher os dados obrigatórios do cliente e validar a sua submissão.
- O sistema deve aplicar as regras de elegibilidade automática com base na localização e no cartão escolhido (cartões com restrição geográfica, cartões digitais e cartões DM).
- As requisições devem ser registadas na base de dados MySQL com os respetivos estados (aprovado, reprovado ou em análise).

---

## 📈 Métricas de Validação

- Execução com sucesso dos fluxos de requisição no frontend e rotas Flask.
- Validação das regras de negócio através de cenários de teste com dados de teste pré-qualificados.
- Conformidade do código com os padrões definidos pelo projeto.

---

## 🚀 Próximos Passos

- Implementação do módulo de adição de parceiros e atribuição de vendedores (Sprint 2).
- Desenvolvimento do sistema de apresentação de ofertas alternativas de produtos para clientes reprovados (Sprint 3).

---

## 📂 Anexos / Evidências

**Vídeo de Demonstração:**\
Confira o website em funcionamento: