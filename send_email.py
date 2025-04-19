import os
import smtplib
import mimetypes
import datetime
from email.message import EmailMessage
import re
from glob import glob

# Encontrar o arquivo de roteiro mais recente
arquivos = sorted(glob("roteiro_tiktok_*.txt"), reverse=True)
arquivo_roteiro = arquivos[0] if arquivos else None

if not arquivo_roteiro:
    raise FileNotFoundError("Nenhum arquivo de roteiro encontrado.")

# Ler conteúdo do roteiro
with open(arquivo_roteiro, "r", encoding="utf-8") as f:
    conteudo_roteiro = f.read()

# Extrair marcações de imagem
marcacoes = "\n".join(re.findall(r"\[Imagem: .*?\]", conteudo_roteiro))

# Criar arquivo com apenas as marcações
data = datetime.date.today().isoformat()
arquivo_marcacoes = f"imagens_para_gerar_{data}.txt"
with open(arquivo_marcacoes, "w", encoding="utf-8") as f:
    f.write(marcacoes)

# Montar o e-mail
msg = EmailMessage()
msg["Subject"] = f"Novo roteiro gerado - {data}"
msg["From"] = os.getenv("EMAIL_SENDER")
msg["To"] = os.getenv("EMAIL_RECIPIENT")
msg.set_content(f"Segue em anexo o roteiro gerado para hoje ({data}) e o arquivo com as marcações de imagem para o ChatGPT.")

# Adicionar anexo: roteiro completo
with open(arquivo_roteiro, "rb") as f:
    file_data = f.read()
    msg.add_attachment(file_data, maintype="text", subtype="plain", filename=arquivo_roteiro)

# Adicionar anexo: marcações
with open(arquivo_marcacoes, "rb") as f:
    file_data = f.read()
    msg.add_attachment(file_data, maintype="text", subtype="plain", filename=arquivo_marcacoes)

# Enviar o e-mail via SMTP (ex: Gmail)
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
    smtp.send_message(msg)

print("E-mail enviado com sucesso!")