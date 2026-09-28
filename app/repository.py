# Todas as consultas SQL (Lojas, Pré-qualificação, Cadastro)

from database import get_connection


#método para inserção na database
#tab = nome da tabela, col = colunas da tabela, val = valores a serem inseridos
#usa keywords insertdb(tab="tabNome"). Passe val e col como tuplas preferencialmente
#ex:
#insertdb(tab="pessoa", col=("nome", "idade"), val=("João", 20))
#insertdb(tab="pessoa", val=("João", 20))
def insertdb(
        *, 
        tab:str, 
        val:tuple[any, ...], 
        col:tuple[str, ...] = ()
        ):
        with get_connection() as conn:
            with conn.cursor() as cur:
                placeholders = ", ".join(["%s"] * len(val))
            
                query = f"""
                    INSERT INTO {tab} ({", ".join(col)})
                    VALUES ({placeholders})
                """
                cur.execute(query, val)

#método para recuperar valores da database
#col = colunas a serem selecionadas, filter = filtro do where
#selectdb(tab="pessoa", col=("nome", "idade"), filter={"nome": "João"})
#filter não é necessário
def selectdb(
        *, 
        tab:str, 
        col:tuple[str, ...], 
        filter:dict[any] = {}
        ) -> tuple:
    with get_connection() as conn:
        with conn.cursor() as cur:
            if(len(filter) > 0):
                col = ", ".join(col)
                filter = " and ".join(f"{k} = '{v}'" for k, v in filter.items())
    
                query = f"""
                select {col} from {tab}
                where {filter}
                """
            else:
                col = ", ".join(col)

                query = f"""
                select {col} from {tab}
                """
            
            cur.execute(query)
            result = cur.fetchall()
            return result


def listar_lojas_parceiras() -> list[dict]:
    """Retorna as lojas ativas no formato esperado pelos services."""
    colunas = ("id", "nome", "cidade", "uf", "eh_digital")
    registros = selectdb(
        tab="lojas_parceiras",
        col=colunas,
        filter={"ativo": 1}
    )

    return [dict(zip(colunas, registro)) for registro in registros]

#método para alterar valor na database
#col = colunas a serem alteradas, filter = filtro do where
#updatedb(tab="pessoa", col={"idade": 15 }, filter={"nome": "João"})
def updatedb(
        *, 
        tab:str, 
        col:dict[any], 
        filter:dict[str]
        ):
    with get_connection() as conn:
        with conn.cursor() as cur:

            col = ", ".join(f"{k} = {v}" for k, v in col.items())
            filter = ", ".join(f"{k} = '{v}'" for k, v in filter.items())

            query = f"""
            UPDATE {tab} SET {col}
            WHERE {filter}
            """

            cur.execute(query)

#Verifica se existe no banco outro registro com características iguais
def verificador(
    tab:str, 
    col:tuple[str, ...], 
    filter:dict[any] = {}
    ) -> bool:

    with get_connection() as conn:
        with conn.cursor() as cur:

            if(len(filter) > 0):
                col = ", ".join(col)
                filter = " and ".join(f"{k} = '{v}'" for k, v in filter.items())
    
                query = f"""
                select {col} from {tab}
                where {filter} LIMIT 1
                """
            
            cur.execute(query)
            result = cur.fetchone()
            return result if result else False


def cadastrar_cliente(dados: dict, status: str):
    
    #insere dados da tabela clientes
    col = ("nome_cliente", "cpf_cliente", "data_nasc_cliente", "telefone_cliente", "email_cliente", "colaborador_dm", "renda_mensal")

    if "colaborador" in dados:
        val = (dados["nome"], dados["cpf"], dados["nascimento"], dados["celular"], dados["email"], 0, dados["renda"])
    else:
        val = (dados["nome"], dados["cpf"], dados["nascimento"], dados["celular"], dados["email"], dados["matricula"], dados["renda"])

    insertdb(tab="cliente", col=col, val=val)

    
    
    try:
        id_estado = verificador(tab="estado", col=("id_estado", ), filter={"uf" : f"{dados["uf"]}"})
    except Exception:
        raise RuntimeError("Estado não existe na db")

    if id_estado:
        id_estado = id_estado[0]
    else:
        pass

    #verifica se existe a cidade no banco. Caso não exista, registra
    id_cidade = verificador(tab="cidade", col=("id_cidade", ), filter={"nome_cidade" : f"{dados["cidade"]}"})

    if id_cidade:
        id_cidade = id_cidade[0]
    else:
        insertdb(tab="cidade", col=("nome_cidade", "id_estado"), val=(f"{dados['cidade']}", f"{id_estado}"))

    
    #insere dados do endereço
    
    id_cliente = verificador(tab="cliente", col=("id_cliente", ), filter={"cpf_cliente" : f"{dados["cpf"]}"})[0]

    col = ("id_cliente", "cep", "logradouro", "numero", "bairro", "id_cidade")
    val = (id_cliente, dados["cep"], dados["logradouro"], dados["numero"], id_cidade)

    #insere dados da solicitação
    try:
        id_cartao = verificador(tab="cartao", col=("id_cartao", ), filter={"tipo_cartao" : f"{dados["tipo_cartao"]}"})[0]
    except Exception:
        raise RuntimeError("Cartão não existe na db")
    
    insertdb(tab="solicitacao_cartao", col=("id_cliente", "id_cartao", "id_loja", "status"), val=(id_cliente, id_cartao, f"{dados["loja"]}", status))


def listar_solicitacoes_dashboard(limite: int = 200) -> list[dict]:
    """
    Solicitações de cartão com dados do cliente e da loja, da mais nova
    para a mais antiga. Sem valores vindos do usuário na string SQL:
    o único parâmetro (limite) vai por %s.
 
    INNER JOIN em cliente: id_cliente é NOT NULL, toda solicitação tem cliente.
    LEFT JOIN em loja: id_loja pode ser NULL, e a solicitação continua na lista
    (nome_loja vem como None).
 
    Ajuste o nome da tabela/coluna da loja se for diferente de loja.nome_loja.
    """
    query = """
        SELECT s.id_solicitacao,
               c.nome_cliente,
               c.cpf_cliente,
               c.renda_mensal,
               s.id_cartao,
               l.nome_loja,
               s.data_solicitacao,
               s.status
        FROM solicitacao_cartao AS s
        INNER JOIN cliente AS c ON c.id_cliente = s.id_cliente
        LEFT JOIN loja AS l ON l.id_loja = s.id_loja
        ORDER BY s.data_solicitacao DESC, s.id_solicitacao DESC
        LIMIT %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limite,))
            colunas = [d[0] for d in cur.description]
            return [dict(zip(colunas, linha)) for linha in cur.fetchall()]