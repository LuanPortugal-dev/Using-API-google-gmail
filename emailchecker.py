import email
import imaplib
import urllib.parse
import re
import os
from pathlib import Path

from dotenv import load_dotenv
from conexao import transferencia, abertura


# Passando o arquivo .env
env_path = Path('./.env')
load_dotenv()


# Buscando o login e a senha dentro do .env
EMAIL = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_PASSWORD")
SERVER = 'imap.gmail.com'


# Fazer a conexão com o servidor gmail, realizar o login e navegar a inbox.
try:

    # Abre uma conexão com o servidor do gmail
    # realiza o login e navega para a pasta que vc deseja ler
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('Teste')


    # Realiza uma busca na inbox com o critério de busca ALL
    # para pegar todos os emails da imbox
    # a busca retorna o status da operação e uma lista com
    # os ids dos emails
    status, data = mail.search(None, 'ALL')

    # data é uma lista com ids em blocos de bytes separados
    # por espaço neste formato: [b'1 2 3', b'4 5 6']
    # então para separar os ids nós primeiramente criamos
    # uma lista vazia

    mail_ids = []
    # e em seguida iteramos pelo data separando os blocos
    # de bytes e concatenando a lista resultante com nossa
    # lista inicial 

    for block in data:
        # a função split chamada sem nenhum parâmetro
        # transforma texto ou bytes em listas usando como
        # ponto de divisão o espaço em branco:
        # b'1 2 3'.split() => [b'1', b'2', b'3']
        mail_ids += block.split()

    # agora para cada id de email baixaremos ele do gmail
    # e extrairemos o conteúdo
    for i in mail_ids:
        # a função fetch baixa o email do gmail passando id
        # e o padrão RFC que você deseja que a mensagem venha
        # formatada
        status, data = mail.fetch(i, '(RFC822)')
        
        # data por algum motivo que eu desconheç vem naquele
        # formato que um item é uma tupla e o outro é só b')'
        # por isso vamos iterar pelo data até encontrar a tupla
        for response_part in data:
            # se for a tupla a gente extrai o conteúdo
            if isinstance(response_part, tuple):

                # usando a função e extrair os dados do email
                # a gente pasa o segundo item da tupla que tem o
                # conteúdo porque o primeiro é só a informação
                # do formato do conteúdo
                message = email.message_from_bytes(response_part[1])


                # daí com o resultado conseguimos tirar as
                # informações de quem enviou o email e o assunto
                mail_from = message['from']
                mail_subject = message['subject']


                # agora para o conteúdo precisa de um pouco mais de
                # trabalho porque ele pode vir em texto puro
                # ou multipart, se for texto puro é só ir para o
                # else e extrair o conteúdo, senao tem que extrair
                # somente o que precisa
                if message.is_multipart():
                    mail_content = ''

                    # no caso do multipart vem junto com o email
                    # anexos e outras versões do mesmo email em
                    # diferentes formatos tipo texto imagem e html
                    # para isso vamos andar pelo payload do email
                    for part in message.get_payload():
                        # se o conteúdo for texto text/plain que é o
                        # texto puro nós extraímos, senão não faz nada.
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()

                else:
                    mail_content = message.get_payload()
                    

                tipoDeDado = mail_subject

                # corrigindo o problema de caracteres, que no caso é o ' ´ ' 
                mensagem = mail_content.replace('=', '%')
                mensagem = urllib.parse.unquote(mensagem)


                # verifica se 'Abertura de conta cliente' está dentro de Tipo de dado
                if tipoDeDado in ['Abertura de conta cliente']:
                    reg = re.compile(r'.*Cliente\s+(.*)\s+abriu\s+.*\s+codigo\s+(\d+)\s+cpf\s+(\d\d\d.\d\d\d.\d\d\d-\d\d)', re.IGNORECASE | re.DOTALL)
                    res = reg.search(mensagem)
                
                    nomeAbertura = res.group(1)
                    codigoAbertura = res.group(2)
                    cpfAbertura = res.group(3).replace('.', '').replace('-', '')
                    
                    #atribui os valores aos parametros da função transferencia da conexao
                    abertura(nomeAbertura, codigoAbertura, cpfAbertura)


                # verifica se 'Transferencia de cliente' está dentro de Tipo de dado
                if tipoDeDado in ['Transferencia de cliente', 'Transferencia de clientes']:
                    reg = re.compile(r'.*Cliente\s+(.*)\s+solicitou\s+.*\s+codigo\s+(\d+)\s+cpf\s+(\d\d\d.\d\d\d.\d\d\d-\d\d)', re.IGNORECASE | re.DOTALL)
                    res = reg.search(mensagem)

                    nomeTransf = res.group(1)
                    codigoTransf = res.group(2)
                    cpfTransf = res.group(3).replace('.', '').replace('-', '')

                    # atribui os valores aos parametros da função transferencia da conexao
                    transferencia(nomeTransf, codigoTransf, cpfTransf)

                    
except Exception as exception:
    print(exception)
