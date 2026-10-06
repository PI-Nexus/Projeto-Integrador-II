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