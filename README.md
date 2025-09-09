# 🎧 VidSummarizeAI

VidSummarizeAI é uma aplicação completa em Python + Streamlit que permite **extrair áudio de vídeos**, **transcrever com Whisper**, e **gerar resumos inteligentes usando a IA Gemini** da Google. Ideal para quem quer resumir conteúdos de vídeo de forma automatizada.

---

## ✨ Funcionalidades

- 🎞️ Processa vídeos inteiros (MP4, MKV, MOV, AVI).
- 🔊 Extrai e converte o áudio para MP3 via FFmpeg.
- 🧠 Transcreve o áudio com o modelo Whisper (da OpenAI).
- 🤖 Gera resumos em Markdown com o Gemini 1.5 Flash (API da Google).
- 📝 Salva transcrição e resumo localmente.
- 🖥️ Interface gráfica via Streamlit.
- ⚙️ Configurável via `.env` e Docker.

---

## 🖼️ Interface

<div align="center">
  <img src="https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/7ff5ce44-ca1e-4c39-97f8-219e41242206/Home_Page.png" alt="Preview da interface">
</div>

---

## 🚀 Como executar

### ✅ Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- Uma chave de API Gemini válida:  
  👉 Obtenha em: https://aistudio.google.com/app/apikey

---

### 📦 1. Clone o repositório

```bash
git clone https://github.com/RannyZyzz/VidSumarizeAI.git
cd vidsummarizeai
```

---

### 🧪 2. Configure a chave da API Gemini

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
GEMINI_API_KEY=sua_chave_real_aqui
```

---

### 🐳 3. Rode com Docker Compose

```bash
docker-compose up --build
```

Acesse em: [http://localhost:8501](http://localhost:8501)

---

## 🛠️ Modos de Operação

Você pode escolher entre 3 modos:

| Modo | Descrição |
|------|-----------|
| 📽️ Processar vídeo do início ao fim | Extrai áudio, transcreve e resume |
| 🎵 Importar apenas MP3 | Pula extração de áudio |
| 📝 Importar apenas transcrição | Usa um `.txt` para enviar ao Gemini |

---

## 🗂️ Estrutura de Pastas

| Pasta         | Função                              |
|---------------|--------------------------------------|
| `output/`     | Armazena áudios convertidos          |
| `transcricao/`| Transcrições salvas (`.txt`)         |
| `Resposta_IA/`| Resumos gerados pelo Gemini (`.md`)  |

---

## 🧱 Arquitetura

- `index.py`: Interface com Streamlit + lógica de processamento.
- `configurar_streamlit.py`: Configura o `secrets.toml` e `config.toml`.
- `Dockerfile`: Cria a imagem com todas dependências (Whisper, FFmpeg, Gemini).
- `docker-compose.yml`: Facilita a execução da aplicação.
- `.env`: Onde você define a variável `GEMINI_API_KEY`.

---

## 🧠 Tecnologias Utilizadas

- [Python 3.10](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Google Generative AI SDK](https://github.com/google/generative-ai-python)
- [FFmpeg](https://ffmpeg.org/)
- [Docker](https://www.docker.com/)

---

## ❓ FAQ

### 1. O Whisper usa GPU?
Neste projeto usamos a versão **CPU** (`torch` + `torchaudio` CPU). Para uso em GPU, você pode alterar o Dockerfile e instalar CUDA.

### 2. O upload máximo é limitado?
Sim. Por padrão é 200 MB no Streamlit. O script `configurar_streamlit.py` ajusta para 1000 MB automaticamente no container.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribuindo

Pull Requests são bem-vindos! Sinta-se à vontade para abrir issues, sugerir melhorias ou relatar bugs.

---

## ✉️ Contato

Entre em contato pelo GitHub ou via [LinkedIn](https://br.linkedin.com/in/ranni%C3%AAr-reis-6a2983a1).
