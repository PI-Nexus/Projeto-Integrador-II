## 📖 Manual do Usuário

### 1. Apresentação

O site de **captação e pré-qualificação de clientes** permite que qualquer pessoa conheça os cartões da **DM**, escolha o que mais combina com ela e **solicite o cartão online**, recebendo o resultado da pré-qualificação na mesma hora: **Aprovado**, **Em análise** ou **Não aprovado** (com oferta de outros produtos).

Os cartões disponíveis são:

* **Cartão DM Visa** — bandeirado, aceito em qualquer estabelecimento que aceite Visa, em todo o Brasil.
* **Cartão Loja** — private label, válido apenas nas unidades da rede parceira escolhida.
* **Cartão Loja Digital** — versão digital do Cartão Loja, sem cartão físico e sem restrição de estado.


---

### 2. Público-alvo e Dores Atendidas 👤💳

#### Usuários atendidos

* **Clientes interessados em crédito:** Pessoas maiores de 18 anos, com CPF regular, que querem solicitar um cartão DM.
* **Clientes de lojas parceiras:** Pessoas que desejam o cartão da sua loja preferida (Cartão Loja).
* **Clientes que preferem o digital:** Pessoas que querem um cartão sem versão física e sem restrição de estado (Cartão Loja Digital).
* **Colaboradores da DM:** Funcionários que possuem regras próprias de aprovação.

#### Dores que o site atende

* **Dificuldade em escolher o cartão:** A página inicial compara os três cartões lado a lado, com as diferenças de aceitação e de restrição geográfica.
* **Processo demorado:** O pedido é 100% online e leva menos de cinco minutos; a resposta sai na hora.
* **Preenchimento cansativo de endereço:** Ao digitar o CEP, rua, bairro, cidade e estado são preenchidos automaticamente.
* **Escolha de loja confusa:** A lista de lojas parceiras é filtrada pelo estado do seu CEP.
* **Ficar sem alternativa quando o cartão não é aprovado:** Mesmo quando o pedido não é aprovado, o site apresenta outros produtos (DM Cred e Empréstimo Pessoal).

---

### 3. Acessando o Site

1. Abra o navegador (computador ou celular).
2. Acesse o endereço do site. Ao executar o projeto na sua máquina (veja o [Manual de Instalação](Manual%20de%20Instalação.md)), o endereço é `http://localhost:5000`.
3. A página inicial será exibida.

> **Requisito:** é necessária conexão com a Internet. O site consulta o CEP no serviço ViaCEP, o salário mínimo vigente no Banco Central e carrega a fonte do Google Fonts.

---

### 4. Fluxo principal de uso

#### 4.1 Página inicial

A página inicial apresenta, de cima para baixo:

* **Cabeçalho:** logo DM, links `Cartões`, `Benefícios`, `Como funciona` e `Dúvidas`, e os botões `Peça seu cartão` e `Já sou cliente` (este abre o portal da DM em outra aba).
* **Destaque (hero):** chamada principal e o botão `Peça seu cartão`.
* **Escolha o cartão ideal pra você:** os três cartões, cada um com suas características.
* **Um cartão, vários benefícios:** aprovação em minutos, aumento de limite automático, pagamento por aproximação, código de segurança dinâmico, descontos em lojas e mais prazo para pagar.
* **Peça agora, é fácil!:** os três passos do pedido.
* **Sobre a DM** e **Dúvidas frequentes** (clique em uma pergunta para ver a resposta).
* **Rodapé:** links de produtos e de ajuda.

Qualquer botão `Peça seu cartão` / `Pedir o ...` leva ao formulário de solicitação.

---

#### 4.2 Escolhendo o cartão

| | Cartão DM Visa | Cartão Loja | Cartão Loja Digital |
|---|---|---|---|
| **Onde vale** | Qualquer lugar que aceite Visa | Unidades da rede parceira escolhida | Parceiros do ramo digital; pronto para uso assim que aprovado |
| **Restrição de estado** | Nenhuma | Loja do mesmo estado do seu CEP | Nenhuma |
| **Cartão físico** | Sim | Sim | **Não é emitido** |

A escolha do cartão é feita na **Etapa 1** do formulário.

---

#### 4.3 Preenchendo o formulário de solicitação

O formulário fica em uma única página, organizado em **quatro etapas** (com um indicador de progresso no topo) mais a confirmação final.

**Etapa 1 · Qual cartão você quer?**
Selecione uma das três opções: `Cartão DM Visa`, `Cartão Loja` ou `Cartão Loja Digital`.

**Etapa 2 · Seus dados**

| Campo | O que informar | Observações |
|---|---|---|
| Nome completo | Como está no documento | Mínimo de 5 caracteres |
| CPF | Somente números | A pontuação entra sozinha; o CPF é validado (dígito verificador) |
| Data de nascimento | `DD/MM/AAAA` | É preciso ter **18 anos ou mais** |
| E-mail | `voce@email.com` | É por ele que o resultado é comunicado |
| Celular | Com DDD | O formato `(12) 99999-9999` entra sozinho |
| Renda mensal | Em reais | Use **vírgula** para os centavos (ex.: `3500,00` ou `3.500,00`). É usada na análise |
| Sou colaborador da DM | Marque só se for o seu caso | Ao marcar, informe a **matrícula DM** |

**Etapa 3 · Onde você está**

1. Digite o **CEP**. Ao sair do campo, `Rua`, `Bairro`, `Cidade` e `Estado` são preenchidos automaticamente.
2. Informe o **número** e, se quiser, o **complemento**.
3. Se o CEP não for encontrado, você ainda pode preencher os campos e escolher o estado manualmente na lista.

> O estado do seu CEP define quais lojas parceiras aparecem na Etapa 4.

**Etapa 4 · Sua loja**

* **Loja parceira:** escolha uma loja na lista. Ela mostra as lojas do **estado selecionado** e também a **loja digital** (que não tem restrição de estado).
* **Vendedor que te atendeu** *(opcional)*: se alguém da loja te ajudou, informe o nome ou o código.
* Para **Cartão Loja** e **Cartão Loja Digital**, escolher a loja é **obrigatório**.

> 💡 **Dica:** mesmo no **Cartão DM Visa**, selecione uma loja da lista para que o envio seja concluído com sucesso (veja [Limitações conhecidas](#6-limitações-conhecidas-desta-versão)).

**Confirmação**

Marque a autorização para consulta dos seus dados na análise de crédito e clique em **`Enviar solicitação`**. O botão muda para *Enviando...* enquanto o pedido é processado.

Se algum campo estiver incorreto ou faltando, uma mensagem em vermelho aparece abaixo dele (por exemplo: *"CPF inválido. Confira os números digitados."* ou *"Você precisa ter 18 anos ou mais."*) e o cursor vai para o primeiro campo com problema.

---

#### 4.4 Resultado da solicitação

Ao enviar, você é levado automaticamente a uma das três telas:

**✅ Aprovado!**

```
Aprovado!
Boa notícia: seu cartão foi aprovado. Agora é só concluir a ativação.

Próximos passos
1. Confirme seu e-mail pelo link que acabamos de enviar.
2. Separe um documento com foto para a retirada.
3. Assim que o cartão estiver pronto, avisamos por e-mail e SMS.
```

**🕒 Sua solicitação está em análise**

```
Recebemos seu pedido e ele está passando por uma análise mais detalhada.
Isso é normal e não significa que foi negado.

O que acontece agora
1. Nosso time analisa as informações que você enviou.
2. Você recebe o resultado por e-mail em até 48 horas.
3. Se precisarmos de algum documento, avisamos pelo mesmo e-mail.
```

**❌ Não foi dessa vez**

```
Não conseguimos aprovar seu cartão agora.
Você pode tentar de novo em 90 dias.

Mas temos outras opções pra você
• DM Cred — microcrédito, com parcelas que cabem no bolso.
• Empréstimo Pessoal — dinheiro na conta para quitar dívidas ou cobrir imprevistos.
```

Nas telas **Aprovado** e **Em análise** há o botão `Voltar para o início`. Na tela **Não foi dessa vez**, os botões `Conhecer o DM Cred` e `Simular empréstimo` abrem o portal da DM em outra aba; para voltar ao site, clique no logo DM no cabeçalho.

---

#### 4.5 Como o pedido é avaliado (regras de pré-qualificação)

O resultado depende do seu perfil e do cartão escolhido:

| Perfil | Cartão DM Visa | Cartão Loja / Loja Digital |
|---|---|---|
| **Colaborador DM** com CPF e matrícula cadastrados | Aprovado | Não aprovado |
| **Colaborador DM** não localizado na base | Em análise | Não aprovado |
| **Não colaborador**, renda ≥ 1,5 × salário mínimo | Em análise | Em análise |
| **Não colaborador**, renda < 1,5 × salário mínimo | Não aprovado | Não aprovado |

* O **salário mínimo** usado no cálculo é o vigente, consultado no Banco Central. Por exemplo, com o salário mínimo em R$ 1.621,00, a renda mínima é de R$ 2.431,50.
* Colaboradores da DM utilizam apenas o **Cartão DM Visa**; pedidos de Cartão Loja de colaboradores não são aprovados.

**Restrições geográficas**

| Cartão | Regra |
|---|---|
| **DM Visa** | Pode ser solicitado de **qualquer estado** |
| **Cartão Loja** | Só permite escolher lojas do **mesmo estado do CEP** informado |
| **Cartão Loja Digital** | **Sem restrição de estado**. Não é emitido cartão físico |

---

### 5. Dúvidas e problemas comuns

| Situação | O que fazer |
|---|---|
| *"CPF inválido"* | Confira os números digitados. Digite apenas os 11 dígitos |
| *"Você precisa ter 18 anos ou mais"* | O pedido só pode ser feito por maiores de 18 anos |
| Endereço não foi preenchido | Confira o CEP (8 dígitos) e sua conexão. Você pode preencher manualmente e escolher o estado na lista |
| Lista de lojas mostra *"Informe um CEP válido primeiro"* | Digite um CEP válido ou selecione o estado manualmente |
| *"Nenhuma loja encontrada neste estado"* | Escolha outro estado, o Cartão DM Visa ou o Cartão Loja Digital |
| Alerta *"Erro de comunicação com o servidor"* | Verifique sua conexão e tente novamente. Se persistir, confirme com a equipe que o servidor está em execução |
| Tela de erro ao enviar | Veja as [Limitações conhecidas](#6-limitações-conhecidas-desta-versão) |

---

### 6. Limitações conhecidas desta versão

Este manual descreve a **Sprint 1** do projeto. Os pontos abaixo estão em ajuste e podem ser removidos deste manual quando forem corrigidos:

* **Um CPF, uma solicitação:** enviar novamente o mesmo CPF retorna erro do servidor.
* **Loja no Cartão DM Visa:** apesar de a Etapa 4 indicar que pode ser pulada, o envio sem loja selecionada retorna erro. Selecione uma loja da lista.
* **Aprovação automática de colaborador:** como o CPF do colaborador já precisa existir na base, o envio dessa combinação ainda pode retornar erro do servidor em vez de abrir a tela *Aprovado*.
* **Dados ainda não gravados:** o endereço e o vendedor informados ainda não são salvos no banco de dados (previsto para a Sprint 2).
* **Resumo nas telas de resultado:** os campos *Protocolo*, *Cartão solicitado* e *Loja* aparecem com "—".
* **Lojas de demonstração:** a lista de lojas parceiras vem de um catálogo fixo de 33 lojas usado para desenvolvimento.

---

### 7. Observações

* O servidor precisa estar **em execução** para o site responder.
* O tempo de resposta pode levar alguns segundos, pois o site consulta serviços externos (CEP e salário mínimo).
* Os prazos exibidos nas telas de resultado (48 horas, 90 dias) e as mensagens de e-mail/SMS são **ilustrativos**: o envio de cartão, e-mail e SMS está fora do escopo deste projeto.

---

# 🛠️ Manual de Instalação

## 1. Configuração do Ambiente

### 1.1 Requisitos

Para executar a aplicação localmente é necessário possuir os seguintes pré-requisitos instalados em sua máquina:

* **Conexão com a Internet** (a aplicação consulta o [ViaCEP](https://viacep.com.br) e a API do Banco Central em tempo de execução, além de carregar a fonte do Google Fonts);
* [Git](https://git-scm.com/downloads) para clonar o repositório, ou uma ferramenta para extrair arquivos `.zip`;
* [Docker](https://www.docker.com/) e **Docker Compose** *(recomendado: sobe o banco e a aplicação já configurados)*;
* Para a **instalação manual/local** (sem Docker):
  * [Python 3.12](https://www.python.org/downloads/) ou superior *(o container usa Python 3.14; versões anteriores à 3.12 não executam o código)*;
  * Servidor [MySQL](https://www.mysql.com/downloads/) 8 ou superior em execução.

**Portas utilizadas**

| Serviço | Porta | Observação |
|---|---|---|
| Aplicação web (Flask) | `5000` | Fixa. Acesse em `http://localhost:5000` |
| MySQL (no Docker) | `3308` no seu computador → `3306` no container | Definida pela variável `PORT` do `.env` |

---

### 1.2 Obtenção do Código Fonte

Faça o download e extração do arquivo `.zip` ou clone o repositório através do terminal executando o comando:

```bash
git clone https://github.com/PI-Nexus/Projeto-Integrador-II.git
cd Projeto-Integrador-II
```

---

### 1.3 Variáveis de Ambiente (.env)

Crie o arquivo `.env` a partir do modelo `.env.example` disponibilizado na raiz do projeto:

**No Linux / macOS:**
```bash
cp .env.example .env
```

**No Windows (CMD / PowerShell):**
```cmd
copy .env.example .env
```

Abra o `.env` e preencha as **três** variáveis:

| Variável | O que informar | Exemplo |
|---|---|---|
| `MYSQL_ROOT_PASSWORD` | Senha do usuário `root` do MySQL (a mesma será usada pela aplicação) | `MinhaSenha@123` |
| `DATABASE` | Nome do banco de dados. **Use `db_cartoes`**, pois é o nome criado pelo script `mysql/schema_cartoes.sql` | `db_cartoes` |
| `PORT` | Porta do seu computador que será ligada ao MySQL do container. **Troque o texto de exemplo por um número** | `3308` |

Exemplo de `.env` pronto:

```env
MYSQL_ROOT_PASSWORD=MinhaSenha@123
DATABASE=db_cartoes
PORT=3308
```

> ⚠️ O arquivo `.env` contém senha e **não deve ser enviado ao GitHub** (já está no `.gitignore`).

---

## 2. Instalação e Execução

O projeto pode ser executado de duas maneiras: via **Docker Compose** (método automatizado) ou **Manual/Local** (configurando Python e MySQL diretamente no sistema operacional).

Em ambos os casos, ao final é necessário carregar os **dados iniciais** do banco (passo obrigatório, explicado em cada opção).

---

### Opção 1: Execução via Docker Compose (Recomendado)

Esta forma inicializa automaticamente o banco de dados MySQL (criando as tabelas) e a aplicação Flask em containers isolados.

#### Passo 1: Subir os containers

1. Garanta que o Docker esteja em execução.
2. Na pasta raiz do projeto (com o `.env` já configurado), execute:

```bash
docker compose up --build
```

> Em instalações mais antigas do Docker, o comando é `docker-compose up --build`.

3. Aguarde o término do build. A aplicação só inicia depois que o MySQL estiver saudável (*healthy*); na primeira execução isso pode levar alguns segundos. Você verá a mensagem **"BACKEND RODANDO COM SUCESSO!"** no terminal.

#### Passo 2: Carregar os dados iniciais (uma única vez)

O script `schema_cartoes.sql` cria apenas as tabelas. É preciso cadastrar os estados, os tipos de cartão e as lojas parceiras, senão o envio do formulário retorna erro. Com os containers em execução, abra **outro terminal** na raiz do projeto:

**Linux / macOS / Git Bash:**
```bash
docker exec -i mysql-cartoes sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" db_cartoes' < mysql/seed_dados_iniciais.sql
```

**Windows PowerShell** (substitua `SUA_SENHA` pela senha do `.env`):
```powershell
Get-Content mysql/seed_dados_iniciais.sql -Raw | docker exec -i mysql-cartoes mysql -uroot -pSUA_SENHA db_cartoes
```

> Alternativa: abra o arquivo `mysql/seed_dados_iniciais.sql` no MySQL Workbench ou DBeaver, conectado em `localhost` na porta definida em `PORT`, e execute-o.

Se o comando retornar erro de *duplicate entry*, os dados já foram carregados antes — não é preciso repetir.

#### Encerrando

* Para parar: `Ctrl + C` ou, em outro terminal, `docker compose down`.
* Os dados do banco ficam guardados em um volume (`mysql_data`) e **permanecem** entre execuções.
* Para **apagar tudo e recomeçar do zero** (por exemplo, para trocar a senha do banco): `docker compose down -v` e depois repita os passos 1 e 2.

---

### Opção 2: Instalação Manual e Execução Local

Caso prefira rodar a aplicação diretamente na sua máquina:

#### Passo 1: Criação da Base de Dados e dados iniciais

1. Com o MySQL em execução, acesse-o (via MySQL Workbench, DBeaver ou terminal).
2. Execute, **nesta ordem**, os dois scripts SQL:

```bash
mysql -u root -p < mysql/schema_cartoes.sql
mysql -u root -p < mysql/seed_dados_iniciais.sql
```

O primeiro cria o banco `db_cartoes` e suas tabelas; o segundo carrega os estados, os tipos de cartão e as lojas parceiras. Execute o segundo **apenas uma vez**.

#### Passo 2: Instalação das Dependências do Python

1. Crie e ative um ambiente virtual (`venv`):

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
.\venv\Scripts\activate
```

2. Instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r app/requirements.txt
```

#### Passo 3: Configurar as variáveis de ambiente da aplicação

Na execução manual, a aplicação **não lê o arquivo `.env` automaticamente**: as variáveis precisam estar definidas no terminal em que o servidor será iniciado. Elas são diferentes das usadas pelo Docker:

| Variável | Obrigatória | Padrão | Descrição |
|---|---|---|---|
| `DB_PASSWORD` | **Sim** | — | Senha do usuário do MySQL |
| `DB_HOST` | Não | `localhost` | Endereço do servidor MySQL |
| `DB_USER` | Não | `root` | Usuário do MySQL |
| `DB_NAME` | Não | `db_cartoes` | Nome do banco de dados |
| `DB_PORT` | Não | `3306` | Porta do MySQL (use `3308` se estiver usando o MySQL do Docker) |

**Linux / macOS:**
```bash
export DB_PASSWORD='MinhaSenha@123'
export DB_PORT=3306
```

**Windows (PowerShell):**
```powershell
$env:DB_PASSWORD = "MinhaSenha@123"
$env:DB_PORT = "3306"
```

**Windows (CMD):**
```cmd
set DB_PASSWORD=MinhaSenha@123
set DB_PORT=3306
```

#### Passo 4: Execução da Aplicação

Na raiz do repositório, com o ambiente virtual ativo e as variáveis definidas, inicie o servidor:

```bash
python app/app.py
```

---

## 3. Acesso ao Sistema

Após a inicialização do servidor (via Docker ou execução local):

1. Abra seu navegador de preferência.
2. Acesse a URL: **`http://localhost:5000`** (a porta da aplicação é fixa; a variável `PORT` do `.env` refere-se somente ao MySQL).
3. A landing page deve ser exibida. Clique em **`Peça seu cartão`** para abrir o formulário de solicitação.

**Verificação rápida**

| Endereço | O que deve acontecer |
|---|---|
| `http://localhost:5000/` | Landing page com os três cartões |
| `http://localhost:5000/solicitar` | Formulário de solicitação |
| `http://localhost:5000/consultar-cep/12245000` | JSON com o endereço do CEP (`"sucesso": true`) |
| `http://localhost:5000/filtrar-lojas-parceiras/uf/SP` | JSON com as lojas de SP e a loja digital |

Para aprender a usar o site, consulte o [Manual do Usuário](Manual%20do%20Usuário.md).

---

## 4. Solução de Problemas

| Sintoma | Causa provável | Solução |
|---|---|---|
| Erro de porta inválida (*invalid port*) ao subir o Docker | `PORT` no `.env` ainda com o texto de exemplo (`PortaDeSuaEscolha`) | Substitua por um número, por exemplo `3308` |
| `Bind for 0.0.0.0:3308 failed` | A porta escolhida em `PORT` já está em uso | Informe outro número livre no `.env` |
| `Bind for 0.0.0.0:5000 failed` / porta 5000 ocupada | Outro programa usa a porta 5000 (no macOS, o *AirPlay Receiver*) | Encerre o programa que usa a porta 5000 (no macOS: *Ajustes do Sistema → Geral → AirDrop e Handoff → Receptor AirPlay*, desative) |
| `RuntimeError: MYSQL_ROOT_PASSWORD não foi configurada no ambiente` | Na execução manual, `DB_PASSWORD` não está definida no terminal | Defina `DB_PASSWORD` (Passo 3 da Opção 2). A mensagem cita outro nome de variável, mas é a `DB_PASSWORD` que falta |
| `SyntaxError` ao iniciar em `repository.py` | Python anterior à 3.12 | Instale o Python 3.12 ou superior |
| `Access denied for user 'root'` ou `Unknown database` | Senha divergente ou `DATABASE` diferente de `db_cartoes` | Confira o `.env`. Se mudou a senha depois da primeira execução do Docker, rode `docker compose down -v` e suba novamente |
| Erro 500 (*Internal Server Error*) ao enviar o formulário | Dados iniciais não carregados, CPF já utilizado em outro envio, ou MySQL fora do ar | Execute o `seed_dados_iniciais.sql`; teste com outro CPF; confira se o MySQL está saudável |
| CEP não preenche o endereço / erro ao enviar como não colaborador | Sem Internet ou serviço externo (ViaCEP, Banco Central) indisponível | Verifique a conexão e tente novamente |
