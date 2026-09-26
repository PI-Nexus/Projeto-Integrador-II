import os
from contextlib import contextmanager
import pymysql

@contextmanager
def get_connection():

    password = os.getenv("DB_PASSWORD")
    if not password:
        raise RuntimeError("MYSQL_ROOT_PASSWORD não foi configurada no ambiente.")

    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=password,
        database=os.getenv("DB_NAME", "db_cartoes"),
        port=int(os.getenv("DB_PORT", os.getenv("MYSQL_PORT", os.getenv("PORT", "3306")))),
        charset="utf8mb4",
    )

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
