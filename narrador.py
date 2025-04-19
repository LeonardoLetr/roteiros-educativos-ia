import os
import datetime
import re
import requests
from glob import glob

# Obter API Key e ID da voz (padrão: Bella)
api_key = os.getenv("ELEVENLABS_API_KEY")
voice_id = "EXAVITQu4vr4xnSDxMaL"  # Bella (suporta PT-BR)

# Encontrar o roteiro mais recente
arquivos = sorted(glob("roteiro_tiktok_*.txt"), reverse=True)
arquivo_roteiro = arquivos[0] if arquivos else None

if not arquivo_roteiro:
    raise FileNotFoundError("Nenhum arquivo de roteiro encontrado.")

# Ler e limpar o roteiro
with open(arquivo_roteiro, "r", encoding="utf-8") as f:
    conteudo = f.read()

# Remover linhas com [Imagem: ...]
texto_narrado = "\n".join([linha.strip() for linha in conteudo.splitlines() if not linha.strip().startswith("[Imagem:") and linha.strip() != ""])

# Gerar nome de saída
data = datetime.date.today().isoformat()
arquivo_saida = f"narracao_tiktok_{data}.mp3"

# Fazer requisição à ElevenLabs
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
headers = {
    "xi-api-key": api_key,
    "Content-Type": "application/json"
}
payload = {
    "text": texto_narrado,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.4,
        "similarity_boost": 0.8
    }
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    with open(arquivo_saida, "wb") as f:
        f.write(response.content)
    print(f"Narração salva como: {arquivo_saida}")
else:
    print("Erro ao gerar narração:", response.status_code, response.text)