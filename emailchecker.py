import email
import imaplib
import emailchecker

EMAIL = 'luanportugal.profissional.tec@gmail.com'
PASSWORD = 'amorloveyou'
SERVER = 'imap.gmail.com'


# Fazer a conexão com o servidor gmail, realizar o login e navegar a inbox.
def read_email_from_gmail():
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

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


                print('From: {}'.format(mail_from))
                print('Subject: {}'.format(mail_subject))
                print('Content: {}'.format(mail_content))


if __name__ == '__main__':
    read_email_from_gmail()
