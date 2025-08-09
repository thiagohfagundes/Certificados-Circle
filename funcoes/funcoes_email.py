#Libs para envio dos e-mails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from dotenv import load_dotenv
import os

load_dotenv()

email_remetente = os.getenv('EMAIL_REMETENTE')
senha_remetente = os.getenv('SENHA_REMETENTE')

def enviar_certificado_por_email(nome_destinatario, email_destinatario, caminho_pdf, link_validacao):
    """Envia um e-mail com o certificado para o destinatário."""
    # Corpo HTML do e-mail
    corpo_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
        <h2>Olá, {nome_destinatario}!</h2>
        <p>Parabéns! Você foi aprovado(a) no curso <strong>Financeiro no Superlógica Imobi - Módulo Fundamental</strong>.</p>
        <p>Seu certificado está em anexo.</p>
        <p>Você pode validar sua autenticidade a qualquer momento pelo link abaixo:</p>
        <p><a href="{link_validacao}" style="background-color: #0A7CFF; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Validar Certificado</a></p>
        <p style="margin-top: 40px;">Atenciosamente,<br><strong>Time Professional Services</strong><br>Grupo Superlógica</p>
    </body>
    </html>
    """

    # Criação da mensagem
    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header('Professional Services Superlógica', 'utf-8')), email_remetente))
    msg['To'] = email_destinatario
    msg['Subject'] = "Seu certificado está pronto!"

    # Anexar corpo HTML
    msg.attach(MIMEText(corpo_html, 'html'))

    # Anexar PDF
    with open(caminho_pdf, "rb") as f:
        part = MIMEApplication(f.read(), _subtype="pdf")
        part.add_header('Content-Disposition', 'attachment', filename=caminho_pdf)
        msg.attach(part)

    # Enviar via SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(email_remetente, senha_remetente)
        smtp.send_message(msg)

    print("E-mail enviado com sucesso.")