from mysql.connector import connection
from mysql.connector import Error

import os
from pathlib import Path
from dotenv import load_dotenv

# Passando o arquivo .env
env_path = Path('./.env')
load_dotenv()

# Buscando a senha dentro do .env
senha = os.getenv("BD_PASSWORD")



"""
#libs para conectar no DB
from sqlalchemy import create_engine, text
import mysql.connector
from mysql.connector import connection
import pandas as pd

#Conexão com o banco de dados
con = connection.MySQLConnection(user='USERNAME_DO_LOGIN', password='SENHA_DO_LOGIN', host='LINK_DO_DB', database='NOME_DO_DB')
#Conexão sendo usada na lib do pandas para conseguir a tabela direto como um dataframe

df = pd.read_sql("SELECT * FROM table", con = con)
#Usando conexão para criar um cursor, cursores são necessários para UPDATE E INSERT no DB

cursor = con.cursor()
#Query que será executada        

query = INSERT INTO table (COL_1)
           VALUES ('VALUE_1')

cursor.execute(query) #Executando query
con.commit()  #"Salvando" as alterações feitas no DB, COMMIT é sempre necessário!
cursor.close() #Fechando cursor
con.close()  #Fechando conexão com o DB

"""




# Função para receber as variaveis e salvá-las dentro do nosso banco de dados, na tabela tb_abertura
def abertura(nomeAbertura, codigoAbertura, cpfAbertura):
    try:
        con = connection.MySQLConnection(
                host='localhost',
                user='root',
                password= senha,
                database='emailsclientes'
                )

        cursor = con.cursor()
        
        query = """INSERT INTO tb_abertura (nome, codigo, cpf, tipo)
                   VALUES ('%s', '%d', '%s', 'ABERTURA')""" % (nomeAbertura, int(codigoAbertura), cpfAbertura)

        cursor.execute(query)
        con.commit()
        cursor.close()
        print('Abertura inserida no banco de dados com sucesso')
    except Error as erro:
        print("Falha ao inserir dados de abertura: {}".format(erro))
    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()
            print("Conexão encerrada com sucesso")


# Função para receber as variaveis e salvá-las dentro do nosso banco de dados, na tabela tb_transferencia
def transferencia(nomeTransf, codigoTransf, cpfTransf):
    try:
        con = connection.MySQLConnection(
                host='localhost',
                user='root',
                password= senha,
                database='emailsclientes'
                )

        cursor = con.cursor()
        
        query = """INSERT INTO tb_transferencia (nome, codigo, cpf, tipo)
                   VALUES ('%s', '%d', '%s', 'TRANSFERENCIA')""" % (nomeTransf, int(codigoTransf), cpfTransf)

        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        cursor.close()
        print('Transferencia inserida no banco de dados com sucesso')
    except Error as erro:
        print("Falha ao inserir dados de transferencia: {}".format(erro))
    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()
            print("Conexão encerrada com sucesso")

