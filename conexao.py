from mysql.connector import connection
from mysql.connector import Error

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('./.env')
load_dotenv()

senha = os.getenv("BD_PASSWORD")

try:
    con = connection.MySQLConnection(
            host='localhost',
            user='root',
            password= senha,
            database='emailsclientes',        
            )

    inserir_dados = """INSERT INTO tb_clientes
                (nome, codigo, cpf, tipo)
            VALUES
                ( nome, codigo, cpf, tipo) 
    """

    cursor = con.cursor()
    cursor.execute(inserir_dados)
    con.commit()
    cursor.close()
except Error as erro:
    print("Falha ao inserir dados: {}".format(erro))
finally:
    if (con.is_connected()):
        cursor.close()
        con.close()
        print("Conexão realizada com sucesso")