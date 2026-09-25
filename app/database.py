import os
from contextlib import contextmanager

import pymysql
from dotenv import load_dotenv


@contextmanager
def get_connection():
    load_dotenv()

    password = os.getenv("MYSQL_ROOT_PASSWORD")
    if not password:
        raise RuntimeError("MYSQL_ROOT_PASSWORD não foi configurada no ambiente.")

    conn = pymysql.connect(
        host=os.getenv("HOST", "localhost"),
        user=os.getenv("USER", "root"),
        password=password,
        database=os.getenv("DATABASE", "db_cartoes"),
        port=int(os.getenv("DB_PORT", os.getenv("MYSQL_PORT", os.getenv("PORT", "3306")))),
    )

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
