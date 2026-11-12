# 🛠️ Manual de Instalação

## 1. Configuração do Ambiente

### 1.1 Requisitos

Para executar a aplicação localmente é necessário possuir os seguintes pré-requisitos instalados em sua máquina:

* **Conexão com a Internet** (a aplicação consulta o [ViaCEP](https://viacep.com.br) e a API do Banco Central em tempo de execução, além de carregar a fonte do Google Fonts);
* [Git](https://git-scm.com/downloads) para clonar o repositório, ou uma ferramenta para extrair arquivos `.zip`;
* [Docker](https://www.docker.com/) e **Docker Compose** *(recomendado: sobe o banco e a aplicação já configurados; o `docker-compose.yml` usa a imagem `mysql:9.7`)*;
* Para a **instalação manual/local** (sem Docker):
  * [Python 3.12](https://www.python.org/downloads/) ou superior *(o container usa Python 3.14; versões anteriores à 3.12 não executam o código)*;
  * Servidor [MySQL](https://www.mysql.com/downloads/) 8 ou superior em execução.

**Portas utilizadas**

| Serviço | Porta | Observação |
|---|---|---|
| Aplicação web — **Docker** | `80` no seu computador → `5000` no container | Acesse em `http://localhost` (sem número de porta) |
| Aplicação web — **execução manual** | `5000` | Acesse em `http://localhost:5000` |
| MySQL (no Docker) | `3308` no seu computador → `3306` no container | Definida pela variável `MYSQL_HOST_PORT` do `.env` (opcional; se não for informada, vale `3308`) |

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

Abra o `.env` e preencha as variáveis abaixo. O `.env.example` traz **textos de instrução no lugar de alguns valores** (por exemplo, em `FLASK_SECRET_KEY`, seguido de uma linha com um comando entre parênteses): substitua o texto de instrução pelo valor desejado e **apague as linhas de instrução**, para que sobrem apenas linhas no formato `NOME=valor`.

| Variável | O que informar | Exemplo |
|---|---|---|
| `MYSQL_ROOT_PASSWORD` | Senha do usuário `root` do MySQL (a mesma será usada pela aplicação) | `MinhaSenha@123` |
| `DATABASE` | Nome do banco de dados. **Use `db_cartoes`**, pois é o nome criado pelo script `mysql/schema_cartoes.sql` | `db_cartoes` |
| `MYSQL_HOST_PORT` | *(Opcional)* Porta do seu computador que será ligada ao MySQL do container. Se a linha não existir, vale `3308`. **Se informar, use um número** | `3308` |
| `ADMIN_PASSWORD` | Senha de acesso ao painel administrativo (`/admin`) | `SenhaDoAdmin@123` |
| `FLASK_SECRET_KEY` | Chave secreta usada pelo Flask para proteger a sessão de login do painel. **Obrigatória:** sem ela a aplicação não inicia. Use um texto longo e aleatório | `troque-por-um-texto-longo-e-aleatorio` |

Exemplo de `.env` pronto:

```env
MYSQL_ROOT_PASSWORD=MinhaSenha@123
DATABASE=db_cartoes
MYSQL_HOST_PORT=3308
ADMIN_PASSWORD=SenhaDoAdmin@123
FLASK_SECRET_KEY=troque-por-um-texto-longo-e-aleatorio
```

> As linhas `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` e `DB_PORT` que já vêm no `.env.example` podem ficar como estão: no Docker, o `docker-compose.yml` define o endereço, o usuário, a senha e o nome do banco usados pela aplicação.

> ℹ️ O `.env.example` pode trazer o nome da porta escrito como `MYSQL_HOST_SPORT` (com um **S** a mais). O Docker Compose **não lê** esse nome: para escolher a porta do MySQL, use `MYSQL_HOST_PORT`.

Para gerar uma chave aleatória para o `FLASK_SECRET_KEY`, execute:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
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

> As tabelas são criadas automaticamente pelo `schema_cartoes.sql`, **somente na primeira vez** em que o volume do banco é criado.

#### Passo 2: Carregar os dados iniciais (uma única vez)

O script `schema_cartoes.sql` cria apenas as tabelas. É preciso cadastrar os estados, os tipos de cartão (`dm_visa`, `loja` e `loja_digital`) e as lojas parceiras, senão o envio do formulário retorna erro. Com os containers em execução, abra **outro terminal** na raiz do projeto:

**Linux / macOS / Git Bash:**
```bash
docker exec -i mysql-cartoes sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" db_cartoes' < mysql/seed_dados_iniciais.sql
```

**Windows PowerShell** (substitua `SUA_SENHA` pela senha do `.env`):
```powershell
Get-Content mysql/seed_dados_iniciais.sql -Raw | docker exec -i mysql-cartoes mysql -uroot -pSUA_SENHA db_cartoes
```

> Alternativa: abra o arquivo `mysql/seed_dados_iniciais.sql` no MySQL Workbench ou DBeaver, conectado em `localhost` na porta definida em `MYSQL_HOST_PORT` (padrão `3308`), e execute-o.

Se o comando retornar erro de *duplicate entry*, os dados já foram carregados antes — não é preciso repetir.

> 💡 **Colaboradores da DM:** o Cartão DM Visa só é aprovado para CPFs que estejam na tabela `colaborador` com `ativo = 1`. Para testar a aprovação, cadastre ao menos um colaborador nessa tabela (via MySQL Workbench, DBeaver ou terminal).

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

O primeiro cria o banco `db_cartoes` e suas tabelas; o segundo carrega os estados, os tipos de cartão e as lojas parceiras. Execute o segundo **apenas uma vez**. Para testar a aprovação do Cartão DM Visa, cadastre também ao menos um colaborador ativo na tabela `colaborador` (veja a dica da Opção 1, Passo 2).

> ⚠️ O `schema_cartoes.sql` não recria tabelas que já existem: rodá-lo uma segunda vez retorna erro. Para **recomeçar do zero** (isso **apaga todos os dados** do banco), apague o banco e rode os dois scripts novamente:
>
> ```bash
> mysql -u root -p -e "DROP DATABASE db_cartoes;"
> mysql -u root -p < mysql/schema_cartoes.sql
> mysql -u root -p < mysql/seed_dados_iniciais.sql
> ```

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
| `FLASK_SECRET_KEY` | **Sim** | — | Chave secreta do Flask (texto longo e aleatório), usada na sessão de login do painel. **Sem ela o servidor não inicia** |
| `ADMIN_PASSWORD` | Sim, para entrar no painel `/admin` | — | Senha de acesso ao painel administrativo |

**Linux / macOS:**
```bash
export DB_PASSWORD='MinhaSenha@123'
export DB_PORT=3306
export ADMIN_PASSWORD='SenhaDoAdmin@123'
export FLASK_SECRET_KEY='troque-por-um-texto-longo-e-aleatorio'
```

**Windows (PowerShell):**
```powershell
$env:DB_PASSWORD = "MinhaSenha@123"
$env:DB_PORT = "3306"
$env:ADMIN_PASSWORD = "SenhaDoAdmin@123"
$env:FLASK_SECRET_KEY = "troque-por-um-texto-longo-e-aleatorio"
```

**Windows (CMD):**
```cmd
set DB_PASSWORD=MinhaSenha@123
set DB_PORT=3306
set ADMIN_PASSWORD=SenhaDoAdmin@123
set FLASK_SECRET_KEY=troque-por-um-texto-longo-e-aleatorio
```

#### Passo 4: Execução da Aplicação

Na raiz do repositório, com o ambiente virtual ativo e as variáveis definidas, inicie o servidor:

```bash
python app/app.py
```

Você verá a mensagem **"BACKEND RODANDO COM SUCESSO!"** no terminal.

---

## 3. Acesso ao Sistema

Após a inicialização do servidor (via Docker ou execução local):

1. Abra seu navegador de preferência.
2. Acesse a URL:
   * **Docker:** **`http://localhost`** (a aplicação é publicada na porta 80 do seu computador);
   * **Execução manual:** **`http://localhost:5000`**.

   A variável `MYSQL_HOST_PORT` do `.env` refere-se somente ao MySQL.
3. A landing page deve ser exibida. Clique em **`Peça seu cartão`** para abrir o formulário de solicitação.
4. Para acessar o painel administrativo, abra o endereço do site seguido de `/admin` (por exemplo, `http://localhost/admin`) e informe a senha definida em `ADMIN_PASSWORD`.

**Verificação rápida**

Os caminhos abaixo valem para qualquer instalação: no Docker, use-os depois de `http://localhost`; na execução manual, depois de `http://localhost:5000`.

| Caminho | O que deve acontecer |
|---|---|
| `/` | Landing page com os três cartões |
| `/solicitar` | Formulário de solicitação |
| `/consultar-cep/12245000` | JSON com o endereço do CEP (`"sucesso": true`) |
| `/filtrar-lojas-parceiras/uf/SP` | JSON com as lojas de SP e as lojas digitais (só retorna lojas depois de carregados os dados iniciais) |
| `/admin` | Tela de acesso administrativo, protegida por senha (`ADMIN_PASSWORD`); com a senha correta, abre o painel |

Para aprender a usar o site e o painel administrativo, consulte o [Manual do Usuário](Manual%20do%20Usuário.md).

---

## 4. Solução de Problemas

| Sintoma | Causa provável | Solução |
|---|---|---|
| Erro de porta inválida (*invalid port*) ao subir o Docker | `MYSQL_HOST_PORT` no `.env` com texto em vez de número (por exemplo, o texto de exemplo `PortaDeSuaEscolha`) | Informe um número, por exemplo `3308`, ou apague a linha para usar o padrão (`3308`) |
| `Bind for 0.0.0.0:3308 failed` | A porta do MySQL já está em uso | Informe outro número livre em `MYSQL_HOST_PORT`, no `.env` |
| `Bind for 0.0.0.0:80 failed` (Docker) | Outro programa do seu computador já usa a porta 80 | Encerre esse programa ou, no `docker-compose.yml`, troque `"80:5000"` por outra porta (por exemplo, `"8080:5000"`) e acesse `http://localhost:8080` |
| Porta 5000 ocupada (execução manual) | Outro programa usa a porta 5000 (no macOS, o *AirPlay Receiver*) | Encerre o programa que usa a porta 5000 (no macOS: *Ajustes do Sistema → Geral → AirDrop e Handoff → Receptor AirPlay*, desative) |
| `KeyError: 'FLASK_SECRET_KEY'` ao iniciar a aplicação | `FLASK_SECRET_KEY` não está definida | Defina a variável: no Docker, no `.env`; na execução manual, no terminal (Passo 3 da Opção 2) |
| `RuntimeError: DB_PASSWORD não foi configurada no ambiente` | Na execução manual, `DB_PASSWORD` não está definida no terminal | Defina `DB_PASSWORD` (Passo 3 da Opção 2) |
| `SyntaxError` ao iniciar em `repository.py` | Python anterior à 3.12 | Instale o Python 3.12 ou superior |
| `Access denied for user 'root'` ou `Unknown database` | Senha divergente ou `DATABASE` diferente de `db_cartoes` | Confira o `.env`. Se mudou a senha depois da primeira execução do Docker, rode `docker compose down -v` e suba novamente |
| `Table ... already exists` ao rodar o `schema_cartoes.sql` | O banco já foi criado antes | Para recomeçar do zero, apague o banco (veja o Passo 1 da Opção 2) ou, no Docker, use `docker compose down -v` |
| Erro 500 (*Internal Server Error*) ao enviar o formulário | Dados iniciais não carregados (o terminal mostra erros como *UF inexistente* ou *Cartão inexistente*) ou MySQL fora do ar | Execute o `seed_dados_iniciais.sql`; confira se o MySQL está saudável |
| A lista da Etapa 4 mostra *"Nenhuma loja encontrada neste estado"* para qualquer estado | Dados iniciais (lojas parceiras) não carregados | Execute o `seed_dados_iniciais.sql` |
| CEP não preenche o endereço | Sem Internet ou serviço ViaCEP indisponível | Verifique a conexão e tente novamente, ou preencha os campos e escolha o estado manualmente |
| Pedido de Cartão Loja / Loja Digital cai em *Em análise* | A consulta ao salário mínimo no Banco Central falhou (sem Internet ou serviço indisponível); o terminal mostra *"Falha ao validar cliente; enviando para análise"* | Verifique a conexão. Veja as [regras de pré-qualificação](Manual%20do%20Usuário.md#45-como-o-pedido-é-avaliado-regras-de-pré-qualificação) |
| `/admin` não aceita a senha | Aparece *"Senha incorreta."*: a senha digitada difere de `ADMIN_PASSWORD` | Confira o `.env` (Docker) ou as variáveis do terminal (execução manual). No Docker, depois de alterar o `.env`, execute `docker compose down` e `docker compose up --build` |
| Erro 500 ao entrar em `/admin` | `ADMIN_PASSWORD` não está definida | Defina `ADMIN_PASSWORD` (no `.env` ou no terminal) e reinicie a aplicação |