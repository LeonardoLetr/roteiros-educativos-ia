import os
import datetime
import re
import requests
from glob import glob

# Variáveis de ambiente necessárias
api_key = os.getenv("SPEECH_KEY")
region = os.getenv("SPEECH_REGION")

if not api_key or not region:
    raise EnvironmentError("SPEECH_KEY e SPEECH_REGION precisam estar definidas.")

# Endpoint TTS
endpoint = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"

# Busca o roteiro mais recente
arquivos = sorted(glob("roteiro_tiktok_*.txt"), reverse=True)
arquivo_roteiro = arquivos[0] if arquivos else None
if not arquivo_roteiro:
    raise FileNotFoundError("Arquivo de roteiro não encontrado.")

# Limpa o texto
with open(arquivo_roteiro, "r", encoding="utf-8") as f:
    texto = "\n".join([
        linha.strip() for linha in f.readlines()
        if not linha.strip().startswith("[Imagem:") and linha.strip()
    ])

# Nome do arquivo de saída
data = datetime.date.today().isoformat()
arquivo_saida = f"narracao_tiktok_{data}.mp3"

# SSML com estilo narrativo e entonação leve
ssml = f'''
<speak version='1.0' xml:lang='pt-BR'
       xmlns:mstts='https://www.w3.org/2001/mstts'
       xmlns='http://www.w3.org/2001/10/synthesis'>
  <voice name='pt-BR-FranciscaNeural'>
    <mstts:express-as style='narration'>
      <prosody rate='medium' pitch='+2%'>
        {texto}
      </prosody>
    </mstts:express-as>
  </voice>
</speak>
'''.strip()

# Requisição
headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/ssml+xml",
    "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
    "User-Agent": "TiktokNarrador"
}

print("Solicitando narração com estilo narrativo ao Azure...")
response = requests.post(endpoint, headers=headers, data=ssml.encode("utf-8"))

if response.status_code == 200:
    with open(arquivo_saida, "wb") as f:
        f.write(response.content)
    print(f"Narração salva como: {arquivo_saida}")
else:
    print("Erro ao gerar narração:")
    print(response.status_code, response.text)