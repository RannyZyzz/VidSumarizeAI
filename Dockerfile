FROM python:3.10-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instala PyTorch (somente CPU) e whisper
RUN pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

# Copia os scripts
COPY index.py configurar_streamlit.py ./

# Instala dependências do Python
RUN pip install --no-cache-dir \
    streamlit \
    google-generativeai \
    openai-whisper \
    imageio-ffmpeg \
    toml

# Criação do diretório de configuração do streamlit
RUN mkdir -p /root/.streamlit

# Passa ARG da chave e define ENV
ARG GEMINI_API_KEY
ENV GEMINI_API_KEY=${GEMINI_API_KEY}

# Executa configuração (criação do secrets.toml e config.toml)
RUN python configurar_streamlit.py

EXPOSE 8501

CMD ["streamlit", "run", "index.py"]
