import openai
import os
import datetime
from glob import glob

# Caminho onde os arquivos de ideia estão
diretorio_arquivos = "./"
padrao_arquivo = "ideias_tiktok_*.txt"

# Encontre o arquivo mais recente
arquivos = sorted(glob(os.path.join(diretorio_arquivos, padrao_arquivo)), reverse=True)
arquivo_mais_recente = arquivos[0] if arquivos else None

# Garante que há um arquivo para processar
if not arquivo_mais_recente:
    raise FileNotFoundError("Nenhum arquivo de ideias foi encontrado.")

# Lê o conteúdo da ideia
with open(arquivo_mais_recente, "r", encoding="utf-8") as f:
    conteudo_ideia = f.read()

# Prompt base com placeholders
prompt_roteiro = f"""
Com base nesta ideia de vídeo:

{conteudo_ideia}

Crie um roteiro completo para um vídeo de TikTok com cerca de 1 minuto. O roteiro deve:

- Começar com o gancho (forte e impactante)
- Apresentar a ideia de forma clara e direta
- Ter frases curtas e simples, adequadas para narração ou legenda
- Incluir sugestões de pausa ou corte onde for natural
- Usar um tom acessível, empático e educativo

Formate a resposta como um roteiro com quebras de linha para cada frase ou bloco.
"""

# Chave da API via variável de ambiente
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Envia para o modelo
response = client.chat.completions.create(
    model="gpt-4.1-mini-2025-04-14",
    messages=[{"role": "user", "content": prompt_roteiro}],
    temperature=0.7,
    max_tokens=1000
)

roteiro = response.choices[0].message.content

# Salva o roteiro em novo arquivo
data = datetime.date.today().isoformat()
nome_arquivo = f"roteiro_tiktok_{data}.txt"

with open(nome_arquivo, "w", encoding="utf-8") as f:
    f.write(roteiro)

print(f"Roteiro gerado com sucesso e salvo como {nome_arquivo}")