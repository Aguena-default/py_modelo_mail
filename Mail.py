import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP = os.getenv("SENHA_APP")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

CAMINHO_RELATORIO = "resultado_previsto.pdf"

msg = EmailMessage()
msg["Subject"] = "📊 Relatório de Prevenção de Evasão - Academia NovaForma"
msg["From"] = EMAIL_REMETENTE
msg["To"] = EMAIL_DESTINO
msg.set_content("Segue em anexo o relatório atualizado com as previsões de risco de evasão dos alunos.")

with open(CAMINHO_RELATORIO, "rb") as f:
    conteudo = f.read()
    msg.add_attachment(conteudo, maintype="application", subtype="pdf", filename=CAMINHO_RELATORIO)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_REMETENTE, SENHA_APP)
    smtp.send_message(msg)

print("✅ Relatório enviado com sucesso para a gestora.")
