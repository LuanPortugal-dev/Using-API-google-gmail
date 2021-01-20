import email
import imaplib
import urllib.parse
import re
import os
from pathlib import Path
import conexao


logfile = Path("../arquivo.txt")

from dotenv import load_dotenv
env_path = Path('./.env')
load_dotenv()



EMAIL = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_PASSWORD")
SERVER = 'imap.gmail.com'


try:
    def writeFileSendEmail(mensage, typeMessage):
        reg = re.compile(r'.*Cliente\s+(.*)\s+abriu|solicitou\s+.*\s+codigo\s+(\d+)\s+cpf\s+(\d\d\d.\d\d\d.\d\d\d-\d\d)', re.IGNORECASE | re.DOTALL)
        res = reg.search(mensage)
        if res:
            nome = res.group(1)
            codigo = res.group(2)
            cpf = res.group(3)
            #print("\n\n-----------------------------------------------------------------------------------")
            #print(f'O cliente {nome} foi cadastrado como {typeMessage}, com código {codigo} e cpf {cpf}\n')

        return res.group(1), res.group(2), res.group(3)
 
    nome, codigo, cpf = writeFileSendEmail('ABC', 'ABC')
 
    conexao.con.inserir_dados = f'INSERT INTO (nome, codigo, cpf) VALUES ({nome}, {codigo}, {cpf})'

except:
    print('Error')
    

# Fazer a conexão com o servidor gmail, realizar o login e navegar a inbox.
def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select('Teste')

        status, data = mail.search(None, 'ALL')

        mail_ids = []

        for block in data:
            # transformar texto ou bytes em listas
            mail_ids += block.split()

        for i in mail_ids:
            # formatação para o padrão RFC
            status, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                # Extração do conteúdo se caso for tupla
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])

                    mail_from = message['from']
                    mail_subject = message['subject']


                    if message.is_multipart():
                        mail_content = ''

                        for part in message.get_payload():
                            if part.get_content_type() == 'text/plain':
                                mail_content += part.get_payload()

                    else:
                        mail_content = message.get_payload()
                        

                    tipoDeDado = mail_subject
                    mensage = mail_content
                    
                    mensage = mensage.replace('=', '%')
                    mensage = urllib.parse.unquote(mensage)

                    # verifica se o cliente é transferencia 
                    if mail_subject in ['Transferencia de cliente', 'Transferencia de clientes',
                        'Abertura de conta cliente']:
                        mensage = mensage.replace('=', '%')
                        mensage = urllib.parse.unquote(mensage)
                        writeFileSendEmail(mensage, mail_subject)

    except:
        print("Error")

if __name__ == '__main__':
    read_email_from_gmail()
