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
def selectdb(*, tab: str, col: tuple[str, ...], filter: dict | None = None) -> tuple:
    filter = filter or {}
    query = f"SELECT {', '.join(col)} FROM {tab}"
    params = ()
    if filter:
        query += " WHERE " + " AND ".join(f"{k} = %s" for k in filter)
        params = tuple(filter.values())
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

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


def cadastrar_cliente(dados: dict, status: str) -> int:
    eh_colab = 1 if dados["colaborador"] else 0
    matricula = (dados.get("matricula") or None) if eh_colab else None
    id_loja = int(dados["loja"]) if dados.get("loja") else None

    # get_connection faz commit ao sair e rollback se houver exceção
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id_cliente FROM cliente WHERE cpf_cliente = %s",
                        (dados["cpf"],))
            row = cur.fetchone()

            if row:
                id_cliente = row[0]
            else:
                cur.execute(
                    """INSERT INTO cliente
                       (nome_cliente, cpf_cliente, data_nasc_cliente, telefone_cliente,
                        email_cliente, colaborador_dm, matricula_dm, renda_mensal)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (dados["nome"], dados["cpf"], dados["nascimento"], dados["celular"],
                     dados["email"], eh_colab, matricula, dados["renda"]),
                )
                id_cliente = cur.lastrowid

                cur.execute("SELECT id_estado FROM estado WHERE uf = %s", (dados["uf"],))
                estado = cur.fetchone()
                if not estado:
                    raise ValueError(f"UF inexistente: {dados['uf']}")

                cur.execute(
                    "SELECT id_cidade FROM cidade WHERE nome_cidade = %s AND id_estado = %s",
                    (dados["cidade"], estado[0]),
                )
                cidade = cur.fetchone()
                if cidade:
                    id_cidade = cidade[0]
                else:
                    cur.execute(
                        "INSERT INTO cidade (nome_cidade, id_estado) VALUES (%s, %s)",
                        (dados["cidade"], estado[0]),
                    )
                    id_cidade = cur.lastrowid

                cur.execute(
                    """INSERT INTO endereco
                       (id_cliente, cep, logradouro, numero, bairro, id_cidade)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (id_cliente, dados["cep"], dados["logradouro"], dados["numero"],
                     dados["bairro"], id_cidade),
                )

            cur.execute("SELECT id_cartao FROM cartao WHERE tipo_cartao = %s",
                        (dados["tipo_cartao"],))
            cartao = cur.fetchone()
            if not cartao:
                raise ValueError(f"Cartão inexistente: {dados['tipo_cartao']}")

            cur.execute(
                """INSERT INTO solicitacao_cartao (id_cliente, id_cartao, id_loja, status)
                   VALUES (%s, %s, %s, %s)""",
                (id_cliente, cartao[0], id_loja, status),
            )
            id_solicitacao = cur.lastrowid
    return id_solicitacao

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

def listar_lojas_parceiras() -> list[dict]:
    query = """
        SELECT l.id_loja AS id, l.nome_loja AS nome, c.nome_cidade AS cidade,
               e.uf, l.eh_digital
        FROM loja AS l
        JOIN cidade AS c ON c.id_cidade = l.id_cidade
        JOIN estado AS e ON e.id_estado = c.id_estado
        WHERE l.status_loja = 'ATIVA'
        ORDER BY e.uf, c.nome_cidade, l.nome_loja
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            colunas = [d[0] for d in cur.description]
            return [dict(zip(colunas, linha)) for linha in cur.fetchall()]

def buscar_solicitacao(id_solicitacao: int) -> dict | None:
    query = """
        SELECT s.id_solicitacao, s.status, ca.nome_cartao, l.nome_loja
        FROM solicitacao_cartao AS s
        JOIN cartao AS ca ON ca.id_cartao = s.id_cartao
        LEFT JOIN loja AS l ON l.id_loja = s.id_loja
        WHERE s.id_solicitacao = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (id_solicitacao,))
            linha = cur.fetchone()
            if not linha:
                return None
            colunas = [d[0] for d in cur.description]
            return dict(zip(colunas, linha))