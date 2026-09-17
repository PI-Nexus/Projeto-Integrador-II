##aqui vai ficar a conexão com o mysql
import pymysql
import os
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3307")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_ROOT_PASSWORD", "nexus"),
        database=os.getenv("MYSQL_DATABASE", "bd_analise")
    )

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
