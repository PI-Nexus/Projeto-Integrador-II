##aqui vai ficar a conexão com o mysql
import pymysql
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="nexus",
        database="db_cartoes"
    )

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
