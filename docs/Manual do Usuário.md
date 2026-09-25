# 🛠️ Manual de Instalação

## 1. Configuração do Ambiente

### 1.1 Requisitos

Para executar a aplicação localmente é necessário possuir os seguintes pré-requisitos instalados em sua máquina:

* Conexão com a Internet;
* [Git](https://git-scm.com/downloads) para clonar o repositório ou ferramenta para extrair arquivos `.zip`;
* [Python 3.9](https://www.python.org/downloads/) ou superior;
* Servidor [MySQL](https://www.mysql.com/downloads/) em execução (para instalação manual/local);
* [Docker](https://www.docker.com/) e **Docker Compose** *(opcional, porém recomendado para execução via containers)*.

---

### 1.2 Obtenção do Código Fonte

Faça o download e extração do arquivo `.zip` ou clone o repositório através do terminal executando o comando:

```bash
git clone https://github.com/PI-Nexus/Projeto-Integrador-II.git
cd Projeto-Integrador-II
```

---

### 1.3 Variáveis de Ambiente

Crie o arquivo de variáveis de ambiente `.env` a partir do modelo `.env.example` disponibilizado na raiz do projeto:

**No Linux / macOS:**
```bash
cp .env.example .env
```

**No Windows (CMD / PowerShell):**
```cmd
copy .env.example .env
```

Abra o arquivo `.env` gerado e configure as credenciais do seu banco de dados MySQL (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, etc.), conforme necessário.

---

## 2. Instalação e Execução

O projeto pode ser executado de duas maneiras: via **Docker Compose** (método automatizado) ou **Manual/Local** (configurando Python e MySQL diretamente no SO).

---

### Opção 1: Execução via Docker Compose (Recomendado)

Esta forma inicializa automaticamente o banco de dados MySQL e a aplicação Flask em containers isolados.

1. Garanta que o Docker e o Docker Compose estejam ativos em seu sistema.
2. Na pasta raiz do projeto, execute:

```bash
docker-compose up --build
```

3. Aguarde o término do build e a inicialização dos serviços.

Para encerrar a execução, utilize `Ctrl + C` ou execute `docker-compose down`.

---

### Opção 2: Instalação Manual e Execução Local

Caso prefira rodar a aplicação diretamente na sua máquina:

#### Step 1: Criação da Base de Dados
1. Acesse seu SGBD MySQL (via MySQL Workbench, DBeaver ou terminal).
2. Execute o script SQL localizado em `mysql/schema_cartoes.sql` para estruturar a base de dados do sistema.

#### Step 2: Instalação das Dependências do Python
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

#### Step 3: Execução da Aplicação
Na raiz do repositório, inicie o servidor com o comando:

```bash
python app/app.py
```

---

## 3. Acesso ao Sistema

Após a inicialização do servidor (via Docker ou execução local):

1. Abra seu navegador de preferência.
2. Acesse a URL: `http://localhost:5000` (ou a porta configurada no seu arquivo `.env`).