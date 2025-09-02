import requests
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import acesso_email

# Configuração de e-mail
email_remetente = acesso_email.username
senha = acesso_email.password
email_destinatario = [acesso_email.username]
email_cc = ["lemmy@gmail.com", "ozzy@gmail.com"]
smtp_server = "smtp.gmail.com"
smtp_port = 587

def checar_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            enviar_alerta(url, response.status_code)
    except requests.exceptions.RequestException as e:
        enviar_alerta(url, f"Erro ao acessar: {e}")

def enviar_alerta(url, status):
    assunto = f"ALERTA: URL {url} fora do ar"
    corpo = f"A URL {url} retornou status: {status}"

    msg = MIMEMultipart()
    msg["From"] = email_remetente
    msg["To"] = ", ".join(email_destinatario)
    msg["Cc"] = ", ".join(email_cc)
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_remetente, senha)
            todos_destinatarios = email_destinatario + email_cc
            server.sendmail(email_remetente, todos_destinatarios, msg.as_string())
        print("E-mail de alerta enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python monitor.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    checar_url(url)

