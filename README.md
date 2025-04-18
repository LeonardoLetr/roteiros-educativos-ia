# ✨ Projeto: Automação de Conteúdo Educativo para TikTok

Este repositório automatiza a criação de ideias, roteiros e envio de materiais para vídeos educativos narrados por IA com imagens ilustrativas.

---

## 🚀 Funcionalidade principal

O GitHub Actions executa diariamente (ou manualmente) o seguinte fluxo:

1. **Gera uma ideia de vídeo** sobre temas como educação infantil, autismo, alfabetização etc.
2. **Cria um roteiro técnico e didático**, narrado por IA, com marcações [Imagem: ...]
3. **Extrai as marcações de imagem** e cria um arquivo separado
4. **Envia por e-mail** o roteiro completo e o arquivo com as marcações para facilitar uso no ChatGPT

---

## 📁 Estrutura de arquivos

- `tikedutor.py` – Gera a ideia
- `roteirizador.py` – Cria o roteiro com estilo definido (professora, tom técnico, com gancho)
- `send_email.py` – Envia os arquivos por e-mail como anexos

---

## 📦 Workflow ativo

Apenas o seguinte workflow deve permanecer ativo:

- `.github/workflows/gerador_completo_com_email.yml`

---

## 📬 Secrets necessários

Configure os seguintes *GitHub Secrets* para o envio de e-mail:

- `OPENAI_API_KEY` – sua chave da OpenAI
- `EMAIL_SENDER` – e-mail que vai enviar (ex: seuemail@gmail.com)
- `EMAIL_PASSWORD` – senha de app (gerada via [Google App Passwords](https://myaccount.google.com/apppasswords))
- `EMAIL_RECIPIENT` – e-mail que vai receber os arquivos

---

## 🧠 Etapas manuais (por enquanto)

As imagens ainda estão sendo geradas manualmente via ChatGPT, a partir das marcações `[Imagem: ...]` extraídas automaticamente.

---

## ✅ Próximas melhorias sugeridas

- Narração automatizada com IA (voz sintética)
- Montagem de vídeo via CapCut ou Whisper API
- Publicação e agendamento automático no TikTok