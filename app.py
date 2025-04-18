import openai
import datetime
import os

api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Prompt que será enviado ao modelo
prompt = """
Você é um criador de conteúdo especializado em educação infantil e desenvolvimento pedagógico. Analise os tópicos em alta hoje no Brasil relacionados a:

- Educação
- Autismo
- Alfabetização
- Pedagogia
- Desenvolvimento infantil

Com base nisso, me sugira 1 ideia de vídeos curtos para TikTok com no minimo 1 minuto. A ideia deve conter:

1. Título envolvente
2. Objetivo do vídeo (o que ensinar ou conscientizar)
3. Uma frase de impacto inicial (gancho)
4. Uma explicação curta em tom acessível (15 segundos no máximo)

Responda em formato de lista e de forma direta, como um roteiro inicial para criador de vídeos.
"""

# Chamada correta usando openai >= 1.0.0
response = client.chat.completions.create(
    model="gpt-4.1-mini-2025-04-14",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=800
)

# Extrair o conteúdo da resposta
content = response.choices[0].message.content

# Cria o arquivo com as ideias
today = datetime.date.today().isoformat()
filename = f"ideias_tiktok_{today}.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Ideias salvas em {filename}")