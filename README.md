# 🎬 VidSummarizeAI

VidSummarizeAI é uma aplicação interativa desenvolvida com **Streamlit**, **Whisper** e **Gemini AI**, que permite processar vídeos e áudios para **extrair transcrições** e gerar **resumos inteligentes em Markdown**. Ideal para jornalistas, pesquisadores, criadores de conteúdo e qualquer pessoa que deseje transformar vídeos longos em informações resumidas de forma automática.

---

## 🚀 Funcionalidades

- 🎞️ Extração de áudio de vídeos (.mp4, .mkv, etc.)
- 🧠 Transcrição automática de áudio com [OpenAI Whisper](https://github.com/openai/whisper)
- 🤖 Resumo inteligente com a API Gemini (Google)
- 📝 Interface amigável via [Streamlit](https://streamlit.io/)
- 💾 Salva automaticamente a transcrição e o resultado da IA em arquivos locais

---

## 🧱 Estrutura do Projeto

```
VidSummarizeAI/
├── index.py                     # Aplicação principal em Streamlit
├── configurar_streamlit.py      # Script de configuração inicial (API + upload)
├── requirements.txt             # Dependências do projeto
├── transcricao/                 # Transcrições salvas automaticamente
├── Resposta_IA/                 # Resumos gerados pela IA
```

---

## ⚙️ Instalação

1. **Clone o repositório**:

```bash
git clone https://github.com/RannyZyzz/VidSumarizeAI.git
cd VidSummarizeAI
```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado)**:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

4. **Configure a chave da API Gemini e o tamanho de upload**:

```bash
python configurar_streamlit.py
```

Siga as instruções no terminal para colar sua chave `GEMINI_API_KEY`.  
Você pode gerar a chave aqui: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## ▶️ Como Usar

Após configurar a API, inicie o aplicativo:

```bash
streamlit run index.py
```

A interface web será aberta automaticamente no navegador.

---

## 🧪 Modos de Operação

Ao iniciar o app, você poderá escolher entre três modos:

1. **📽️ Processar vídeo do início ao fim**  
   - Envie um arquivo de vídeo.
   - O sistema extrai o áudio, transcreve e gera o resumo.

2. **🎵 Importar apenas MP3**  
   - Envie diretamente um arquivo `.mp3` para transcrição e resumo.

3. **📝 Importar apenas transcrição**  
   - Faça upload de um `.txt` com o texto para receber o resumo da IA.

---

## 🔐 Variáveis de Ambiente

A chave da API Gemini será salva automaticamente em:

```
~/.streamlit/secrets.toml

# Exemplo:
[GEMINI_API_KEY]
GEMINI_API_KEY = "sua_chave_aqui"
```

---

## 📂 Saída dos Arquivos

- **Transcrição**: salva em `transcricao/NOME_BASE.txt`
- **Resumo da IA**: salvo em `Resposta_IA/NOME_BASE.md`

---

## 🧠 Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Google Gemini API](https://aistudio.google.com/)
- [FFmpeg](https://ffmpeg.org/) (gerenciado automaticamente via `imageio-ffmpeg`)

---

## ❗ Observações

- O modelo Whisper utilizado é o `small` (ótimo custo-benefício entre velocidade e precisão).
- A API Gemini pode ter custos dependendo da sua conta Google Cloud.
- Para arquivos grandes, o limite padrão de upload do Streamlit foi ajustado para **1000MB**.

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 🤝 Contribuição

Contribuições são bem-vindas!  
Sinta-se à vontade para abrir *Issues* ou enviar *Pull Requests*.

---

## 📧 Contato

Em caso de dúvidas, sugestões ou colaborações:

- ✉️ Email: rannierreis@gmail.com
- 🧑 GitHub: [@RannyZyzz](https://github.com/RannyZyzz)

---
