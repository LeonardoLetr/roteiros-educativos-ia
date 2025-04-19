import os
import smtplib
import mimetypes
import datetime
from email.message import EmailMessage
import re
from glob import glob

# Encontrar o arquivo de roteiro mais recente
roteiros = sorted(glob("roteiro_tiktok_*.txt"), reverse=True)
arquivo_roteiro = roteiros[0] if roteiros else None
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

# Procurar narração gerada
audios = sorted(glob(f"narracao_tiktok_{data}.mp3"), reverse=True)
arquivo_audio = audios[0] if audios else None

# Montar o e-mail
msg = EmailMessage()
msg["Subject"] = f"Novo roteiro gerado - {data}"
msg["From"] = os.getenv("EMAIL_SENDER")
msg["To"] = os.getenv("EMAIL_RECIPIENT")
msg.set_content(f"Segue em anexo o roteiro gerado para hoje ({data}), as marcações de imagem para o ChatGPT e a narração em áudio gerada automaticamente.")

# Anexar roteiro
with open(arquivo_roteiro, "rb") as f:
    msg.add_attachment(f.read(), maintype="text", subtype="plain", filename=arquivo_roteiro)

# Anexar marcações
with open(arquivo_marcacoes, "rb") as f:
    msg.add_attachment(f.read(), maintype="text", subtype="plain", filename=arquivo_marcacoes)

# Anexar áudio (se existir)
if arquivo_audio:
    with open(arquivo_audio, "rb") as f:
        msg.add_attachment(f.read(), maintype="audio", subtype="mpeg", filename=arquivo_audio)

# Enviar o e-mail
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
    smtp.send_message(msg)

print("E-mail enviado com sucesso!")