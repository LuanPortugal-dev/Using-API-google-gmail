import email
import imaplib
import emailchecker
import re
import os

from pathlib import Path
env_path = Path('.env')

from dotenv import load_dotenv
load_dotenv(dotenv_path=env_path)

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



                nome = 'Luan' 
                codigo = '0000000'
                cpf = '222222222'




                # Diz se é abertura ou transferência
                if mail_subject == 'Abertura de conta cliente':
                    print(f'{nome} cadastrado como Abertura, com código {codigo} e cpf {cpf}')
                elif 'Transferencia de cliente' or 'Transferencia de clientes':
                    print(f'{nome} cadastrado como transferência, com código {codigo} e cpf {cpf}')
                else:
                    print("Nenhum tipo de dado válido")        


                #arquivo = open("./texto.txt", "a")
                #arquivo.write('From: {}'.format(mail_from))
                #print('Subject: {}'.format(mail_subject))
                #print('Content: {}'.format(mail_content))
                

                

if __name__ == '__main__':
    read_email_from_gmail()
