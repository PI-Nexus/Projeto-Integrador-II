# Todas as consultas SQL (Lojas, Pré-qualificação, Cadastro)

from app.database import get_connection


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
                filter = ", ".join(f"{k} = '{v}'" for k, v in filter.items())
    
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