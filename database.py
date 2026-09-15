##aqui vai ficar a conexão com o mysql

import pymysql

# Conexão com o banco
conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="nexus",
    database="db_cartoes"
)

cursor = conn.cursor()

# Insert básico
sql = """

"""
valores = ()

cursor.execute(sql, valores)
conn.commit()  # necessário pra salvar o insert de verdade


cursor.close()
conn.close()
