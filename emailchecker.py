import email
import imaplib
import emailchecker

import re
import os


from dotenv import load_dotenv
load_dotenv()

from pathlib import Path

logfile = Path("../arquivo.txt")


EMAIL = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_PASSWORD")
SERVER = 'imap.gmail.com'


# Fazer a conexão com o servidor gmail, realizar o login e navegar a inbox.
def read_email_from_gmail():
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
                if mail_subject == 'Transferencia de cliente' or 'Transferencia de clientes':
                    reg = re.compile(r'.*Cliente\s+(.*)\s+solicitou\s+.*\s+codigo\s+(\d+)\s+cpf\s+(\d\d\d.\d\d\d.\d\d\d-\d\d)', re.IGNORECASE|re.DOTALL)
                    res = reg.search(mensagem)
                    if res:
                        nome = res.group(1)
                        codigo = res.group(2)
                        cpf = res.group(3)
                        print("\n\n-----------------------------------------------------------------------------------")
                        print(f'O cliente {nome} foi cadastrado como transferência, com código {codigo} e cpf {cpf}\n')
                        with logfile.open("a") as arquivo:
                            arquivo.write("\n\nTransferencia-------------------------------------------------------------------\n")
                            arquivo.write(f'O cliente {nome} foi cadastrado como transferência, com código {codigo} e cpf {cpf}\n')
                else:
                    print("Erro na busca")


                # verifica se o cliente é abertura
                if mail_subject == 'Abertura de conta cliente':
                    reg = re.compile(r'.*Cliente\s+(.*)\s+abriu\s+.*\s+codigo\s+(\d+)\s+cpf\s+(\d\d\d.\d\d\d.\d\d\d-\d\d)', re.IGNORECASE)
                    res = reg.search(mensagem)
                    if res:
                        nome = res.group(1)
                        codigo = res.group(2)
                        cpf = res.group(3)
                        print("\n\n-----------------------------------------------------------------------------------")
                        print(f'O cliente {nome} foi cadastrado como Abertura, com código {codigo} e cpf {cpf}\n')
                        with logfile.open("a") as arquivo:
                            arquivo.write("\n\nTransferencia-------------------------------------------------------------------\n")
                            arquivo.write(f'O cliente {nome} foi cadastrado como transferência, com código {codigo} e cpf {cpf}\n')
                else:
                    print("Erro na busca")


if __name__ == '__main__':
    read_email_from_gmail()
