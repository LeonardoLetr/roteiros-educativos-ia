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

# Prompt atualizado com tom de professora e uso do gancho
prompt_roteiro = f"""
Com base nesta ideia de vídeo:

{conteudo_ideia}

Crie um roteiro para um vídeo de TikTok com cerca de 1 minuto, que será narrado por uma IA e ilustrado com imagens.

⚠️ Use a frase de impacto (gancho) como a introdução do vídeo.

Escreva com o tom de uma professora explicando o conteúdo para outros educadores e responsáveis.

Regras para o roteiro:

- Linguagem técnica, mas acessível para leigos
- Comece com o gancho exatamente como está escrito
- Cada bloco pode conter até 2 ou 3 frases explicativas
- Antes de cada bloco, insira uma sugestão de imagem no formato: [Imagem: descrição da cena]
- Total aproximado entre 100 e 130 palavras
- Traga exemplos, dados ou explicações claras, evitando frases genéricas ou poéticas

Formato esperado:
[Imagem: descrição da cena]
Texto narrado (2 a 3 frases)
(linha em branco para separar cada cena)
"""

# Chave da API via variável de ambiente
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Envia para o modelo
response = client.chat.completions.create(
    model="gpt-4o",
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