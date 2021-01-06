import email
import imaplib
import emailchecker
import urllib.parse

import re
import os


from dotenv import load_dotenv
load_dotenv()

from pathlib import Path

logfile = Path("../arquivo.txt")


EMAIL = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_PASSWORD")
SERVER = 'imap.gmail.com'




def writeFileSendEmail(mensagem, typeMessage):
    try:
        global logfile
        reg = re.compile(r'.*Cliente\s+(.*)\s+[abriu, solicitou]\s+.*\s+codigo\s+(\d+)\s+cpf\s+(\d\d\d.\d\d\d.\d\d\d-\d\d)', re.IGNORECASE | re.DOTALL)
        res = reg.search(mensagem)
        if res:
            nome = res.group(1)
            codigo = res.group(2)
            cpf = res.group(3)
            print("\n\n-----------------------------------------------------------------------------------")
            print(f'O cliente {nome} foi cadastrado como {typeMessage}, com código {codigo} e cpf {cpf}\n')
            with logfile.open("a") as arquivo:
                arquivo.write(f"\n\n{typeMessage}-------------------------------------------------------------------\n")
                arquivo.write(f'O cliente {nome} foi cadastrado como {typeMessage}, com código {codigo} e cpf {cpf}\n') 

            return True
    except:
        return False


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
                        

                    mensagem = mail_content


                    
                    # verifica se o cliente é transferencia 
                    if mail_subject in ['Transferencia de cliente', 'Transferencia de clientes',
                        'Abertura de conta cliente']:
                        mensagem = mensagem.replace('=', '%')
                        mensagem = urllib.parse.unquote(mensagem)
                        writeFileSendEmail(mensagem, mail_subject)
    except:
        print("Erro")

if __name__ == '__main__':
    read_email_from_gmail()

