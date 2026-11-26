# Todas as consultas SQL (Lojas, Pré-qualificação, Cadastro)

from database import get_connection
from datetime import datetime
from zoneinfo import ZoneInfo

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

    id_loja = None
    id_unidade = None

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Recupera o ID da loja conforme o cartão selecionado
            if dados["tipo_cartao"] == "loja":
                id_unidade = int(dados["loja"])

                cur.execute(
                    """
                    SELECT id_loja
                    FROM unidade_loja
                    WHERE id_unidade = %s
                    """,
                    (id_unidade,)
                )

                unidade = cur.fetchone()

                if not unidade:
                    raise ValueError("Unidade parceira não encontrada.")

                id_loja = unidade[0]

            elif dados["tipo_cartao"] == "loja_digital":
                id_loja = int(dados["loja"])

            # Busca cliente existente
            cur.execute(
                "SELECT id_cliente FROM cliente WHERE cpf_cliente = %s",
                (dados["cpf"],)
            )

            row = cur.fetchone()

            if row:
                id_cliente = row[0]

            else:
                cur.execute(
                    """
                    INSERT INTO cliente
                    (nome_cliente, cpf_cliente, data_nasc_cliente,
                     telefone_cliente, email_cliente, renda_mensal)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        dados["nome"],
                        dados["cpf"],
                        dados["nascimento"],
                        dados["celular"],
                        dados["email"],
                        dados["renda"]
                    )
                )

                id_cliente = cur.lastrowid

                cur.execute(
                    "SELECT id_estado FROM estado WHERE uf = %s",
                    (dados["uf"],)
                )

                estado = cur.fetchone()

                if not estado:
                    raise ValueError(f"UF inexistente: {dados['uf']}")

                cur.execute(
                    """
                    SELECT id_cidade
                    FROM cidade
                    WHERE nome_cidade = %s AND id_estado = %s
                    """,
                    (dados["cidade"], estado[0])
                )

                cidade = cur.fetchone()

                if cidade:
                    id_cidade = cidade[0]

                else:
                    cur.execute(
                        """
                        INSERT INTO cidade (nome_cidade, id_estado)
                        VALUES (%s, %s)
                        """,
                        (dados["cidade"], estado[0])
                    )

                    id_cidade = cur.lastrowid

                cur.execute(
                    """
                    INSERT INTO endereco
                    (id_cliente, cep, logradouro, numero, bairro, id_cidade)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        id_cliente,
                        dados["cep"],
                        dados["logradouro"],
                        dados["numero"],
                        dados["bairro"],
                        id_cidade
                    )
                )

            # Busca cartão
            cur.execute(
                "SELECT id_cartao FROM cartao WHERE tipo_cartao = %s",
                (dados["tipo_cartao"],)
            )

            cartao = cur.fetchone()

            if not cartao:
                raise ValueError(
                    f"Cartão inexistente: {dados['tipo_cartao']}"
                )

            # Horário de São Paulo
            data_solicitacao = datetime.now(
                ZoneInfo("America/Sao_Paulo")
            )

            # Cadastra solicitação
            cur.execute("""
                INSERT INTO solicitacao_cartao
                    (id_cliente, id_cartao, id_loja, id_unidade, status, data_solicitacao)
                    VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                id_cliente,
                cartao[0],
                id_loja,
                id_unidade,
                status,
                data_solicitacao
            ))

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
               col.ativo,
               c.cpf_cliente,
               c.renda_mensal,
               s.id_cartao,
               ca.nome_cartao,
               l.nome_loja,
               s.data_solicitacao,
               s.status
        FROM solicitacao_cartao AS s
        INNER JOIN cliente AS c ON c.id_cliente = s.id_cliente
        LEFT JOIN colaborador as col ON col.cpf = c.cpf_cliente
        INNER JOIN cartao AS ca ON ca.id_cartao = s.id_cartao
        LEFT JOIN loja AS l ON l.id_loja = s.id_loja
        ORDER BY s.data_solicitacao DESC, s.id_solicitacao DESC
        LIMIT %s
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limite,))
            colunas = [d[0] for d in cur.description]
            return [dict(zip(colunas, linha)) for linha in cur.fetchall()]

def listar_unidades_parceiras() -> list[dict]:
    query = """
        SELECT
            u.id_unidade AS id,
            l.id_loja,
            l.nome_loja AS nome,
            u.cep_unidade AS cep,
            c.nome_cidade AS cidade,
            e.uf
        FROM unidade_loja AS u
        JOIN loja AS l
            ON l.id_loja = u.id_loja
        JOIN cidade AS c
            ON c.id_cidade = u.id_cidade
        JOIN estado AS e
            ON e.id_estado = c.id_estado
        WHERE
            l.status_loja = 'ATIVA'
            AND u.status_unidade = 'ATIVA'
        ORDER BY
            e.uf,
            c.nome_cidade,
            l.nome_loja
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            colunas = [d[0] for d in cur.description]

            return [
                dict(zip(colunas, linha))
                for linha in cur.fetchall()
            ]

def listar_lojas_digitais() -> list[dict]:
    query = """
        SELECT
            id_loja AS id,
            nome_loja AS nome,
            eh_digital
        FROM loja
        WHERE
            status_loja = 'ATIVA'
            AND eh_digital = 1
        ORDER BY nome_loja
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            colunas = [d[0] for d in cur.description]

            return [
                dict(zip(colunas, linha))
                for linha in cur.fetchall()
            ]

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

def listar_colaboradores() -> list[dict]:
    query = """
        SELECT col.matricula, c.nome_cliente, col.cpf, col.ativo
        FROM colaborador AS col
        LEFT JOIN cliente AS c ON col.cpf = c.cpf_cliente
        WHERE col.ativo = 1
        ORDER BY col.matricula
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            colunas = [d[0] for d in cur.description]
            return [dict(zip(colunas, linha)) for linha in cur.fetchall()]

def cpf_possui_solicitacao(cpf: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 1
                FROM solicitacao_cartao sc
                INNER JOIN cliente c
                    ON sc.id_cliente = c.id_cliente
                WHERE c.cpf_cliente = %s
                LIMIT 1
            """, (cpf,))

            return cur.fetchone() is not None


def cadastrar_vendedor(nome: str, cpf: str, email: str, id_unidade: int):
    cpf = ''.join(filter(str.isdigit, cpf))
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO vendedor
                    (id_unidade, nome_vendedor, cpf_vendedor,
                     email_vendedor, status_vendedor)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    id_unidade,
                    nome,
                    cpf,
                    email,
                    "Ativo"
                )
            )

            return cur.lastrowid

def buscar_lojas_vendedor(termo: str):

    with get_connection() as conn:
        with conn.cursor() as cur:

            pesquisa = f"%{termo}%"

            cur.execute(
                """
                SELECT
                    id_loja,
                    nome_loja
                FROM loja
                WHERE
                    nome_loja LIKE %s
                    AND status_loja = 'ATIVA'
                    AND eh_digital = 0
                ORDER BY nome_loja
                LIMIT 20
                """,
                (pesquisa,)
            )

            lojas = cur.fetchall()

            return [
                {
                    "id_loja": loja[0],
                    "nome_loja": loja[1]
                }
                for loja in lojas
            ]

def buscar_unidades_da_loja(id_loja: int, termo: str):

    with get_connection() as conn:
        with conn.cursor() as cur:

            pesquisa = f"%{termo}%"

            cur.execute(
                """
                SELECT
                    u.id_unidade,
                    u.cep_unidade,
                    c.nome_cidade,
                    e.uf
                FROM unidade_loja u
                INNER JOIN cidade c
                    ON c.id_cidade = u.id_cidade
                INNER JOIN estado e
                    ON e.id_estado = c.id_estado
                WHERE
                    u.id_loja = %s
                    AND (
                        c.nome_cidade LIKE %s
                        OR u.cep_unidade LIKE %s
                    )
                    AND u.status_unidade = 'ATIVA'
                ORDER BY c.nome_cidade
                LIMIT 20
                """,
                (id_loja, pesquisa, pesquisa)
            )

            unidades = cur.fetchall()

            return [
                {
                    "id_unidade": unidade[0],
                    "cep": unidade[1],
                    "cidade": unidade[2],
                    "uf": unidade[3]
                }
                for unidade in unidades
            ]

def autenticar_vendedor(email: str, cpf: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    v.id_vendedor,
                    v.nome_vendedor,
                    v.id_unidade,
                    l.nome_loja
                FROM vendedor v
                INNER JOIN unidade_loja u
                    ON u.id_unidade = v.id_unidade
                INNER JOIN loja l
                    ON l.id_loja = u.id_loja
                WHERE v.email_vendedor = %s
                  AND v.cpf_vendedor = %s
                  AND v.status_vendedor = 'ATIVO'
                """,
                (email, cpf)
            )

            vendedor = cur.fetchone()

            if not vendedor:
                return None

            return {
                "id_vendedor": vendedor[0],
                "nome": vendedor[1],
                "id_unidade": vendedor[2],
                "nome_loja": vendedor[3]
            }

def listar_solicitacoes_vendedor(id_unidade: int):

    query = """
        SELECT
            s.id_solicitacao,
            c.nome_cliente,
            c.cpf_cliente,
            c.renda_mensal,
            ca.nome_cartao,
            l.nome_loja,
            s.data_solicitacao,
            s.status,
            s.motivo_decisao,
            s.id_vendedor_analise,
            v.nome_vendedor AS nome_vendedor_analise
        FROM solicitacao_cartao s
        INNER JOIN cliente c
            ON c.id_cliente = s.id_cliente
        INNER JOIN cartao ca
            ON ca.id_cartao = s.id_cartao
        LEFT JOIN loja l
            ON l.id_loja = s.id_loja
        LEFT JOIN vendedor v
            ON v.id_vendedor = s.id_vendedor_analise
        WHERE s.id_unidade = %s
        ORDER BY s.data_solicitacao DESC
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(query, (id_unidade,))

            colunas = [coluna[0] for coluna in cur.description]

            return [
                dict(zip(colunas, linha))
                for linha in cur.fetchall()
            ]

def decidir_solicitacao_vendedor(
    id_solicitacao: int,
    id_unidade: int,
    id_vendedor: int,
    decisao: str,
    motivo: str | None = None
) -> bool:

    query = """
        UPDATE solicitacao_cartao
        SET
            status = %s,
            id_vendedor_analise = %s,
            motivo_decisao = %s
        WHERE id_solicitacao = %s
          AND id_unidade = %s
          AND LOWER(REPLACE(status, ' ', '_')) IN ('analise', 'em_analise')
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    decisao,
                    id_vendedor,
                    motivo,
                    id_solicitacao,
                    id_unidade
                )
            )

            return cur.rowcount == 1