import os
import whisper
import streamlit as st
import google.generativeai as genai
from imageio_ffmpeg import get_ffmpeg_exe
import subprocess

# ============================ CONFIG GERAL =============================

def configurar_api_gemini():
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("Chave da API do Gemini não configurada.")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

modelo_gemini = configurar_api_gemini()

def chamar_gemini(transcricao, contexto_usuario, model):
    if not transcricao.strip():
        return "Erro: transcrição vazia."
    
    instrucao = contexto_usuario or "Com base na transcrição a seguir, crie um resumo conciso em Markdown."
    prompt = f"""
    **Instrução do Usuário:**  
    {instrucao}

    ---

    **Texto da Transcrição para Análise:**  
    {transcricao}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao chamar a IA: {e}"

# ============================ AUDIO & TRANSCRIÇÃO =============================

def extrair_audio(video_path, destino_base):
    nome_base = os.path.splitext(os.path.basename(video_path))[0]
    pasta_saida = os.path.join(destino_base, "Conversao", nome_base)
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_mp3 = os.path.join(pasta_saida, f"{nome_base}.mp3")

    try:
        ffmpeg_path = get_ffmpeg_exe()
        comando = [
            ffmpeg_path,
            "-i", video_path,
            "-vn", "-ab", "320k",
            "-map_chapters", "-1",
            "-y", caminho_mp3
        ]
        subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return caminho_mp3
    except Exception as e:
        st.error(f"Erro ao extrair áudio: {e}")
        return None

def transcrever_audio(mp3_path):
    try:
        model = whisper.load_model("small")
        result = model.transcribe(mp3_path)
        return result.get("text", "").strip()
    except Exception as e:
        st.error(f"Erro ao transcrever áudio: {e}")
        return ""

# ============================ SALVAMENTO LOCAL =============================

def salvar_transcricao(transcricao, nome_base):
    os.makedirs("transcricao", exist_ok=True)
    caminho = os.path.join("transcricao", f"{nome_base}.txt")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(transcricao)

def salvar_resposta_ia(resposta, nome_base):
    os.makedirs("Resposta_IA", exist_ok=True)
    caminho = os.path.join("Resposta_IA", f"{nome_base}.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(resposta)

# ============================ CONTROLE DE ESTADO =============================

if "processando" not in st.session_state:
    st.session_state.processando = False
if "confirmacao_iniciar" not in st.session_state:
    st.session_state.confirmacao_iniciar = False
if "confirmacao_cancelar" not in st.session_state:
    st.session_state.confirmacao_cancelar = False

def solicitar_confirmacao_inicio():
    st.session_state.confirmacao_iniciar = True

def confirmar_inicio():
    st.session_state.processando = True
    st.session_state.confirmacao_iniciar = False

def cancelar_confirmacao_inicio():
    st.session_state.confirmacao_iniciar = False

def solicitar_confirmacao_cancelamento():
    st.session_state.confirmacao_cancelar = True

def confirmar_cancelamento():
    st.session_state.processando = False
    st.session_state.confirmacao_cancelar = False

def cancelar_confirmacao_cancelamento():
    st.session_state.confirmacao_cancelar = False

def mostrar_controles_de_processo():
    if not st.session_state.processando:
        if st.session_state.confirmacao_iniciar:
            col1, col2 = st.columns(2)
            with col1:
                st.button("✅ Confirmar Início", on_click=confirmar_inicio)
            with col2:
                st.button("❌ Cancelar", on_click=cancelar_confirmacao_inicio)
        else:
            st.button("▶️ Iniciar Processamento", on_click=solicitar_confirmacao_inicio)
    else:
        if st.session_state.confirmacao_cancelar:
            col1, col2 = st.columns(2)
            with col1:
                st.button("✅ Confirmar Cancelamento", on_click=confirmar_cancelamento)
            with col2:
                st.button("❌ Manter Processando", on_click=cancelar_confirmacao_cancelamento)
        else:
            st.button("⛔ Cancelar Processamento", on_click=solicitar_confirmacao_cancelamento)

    return st.session_state.processando

# ============================ UI STREAMLIT =============================

st.set_page_config(page_title="Processador de Vídeo com IA", layout="centered")
st.title("🎧 VidSummarizeAI - Processamento de Vídeo e Áudio com IA Gemini")
st.markdown("Escolha um dos modos abaixo para começar.")

modo = st.selectbox("Selecione o modo de operação:", [
    "📽️ Processar vídeo do início ao fim",
    "🎵 Importar apenas MP3",
    "📝 Importar apenas transcrição"
])

contexto = st.text_area("📌 Contexto/Instrução para a IA (opcional)", height=100)

# ============================ MODOS DE OPERAÇÃO =============================

if modo == "📽️ Processar vídeo do início ao fim":
    video_file = st.file_uploader("📁 Envie o arquivo de vídeo", type=["mp4", "mkv", "avi", "mov"])
    if video_file and modelo_gemini:
        nome_base = os.path.splitext(video_file.name)[0]

        st.markdown("## 🚦 Controle de Processamento")
        if mostrar_controles_de_processo():
            status = st.status("Iniciando processamento...", expanded=True)
            status.write("🎞️ Salvando vídeo temporário...")
            temp_video_path = f"temp_{video_file.name}"
            with open(temp_video_path, "wb") as f:
                f.write(video_file.read())

            status.write("🔊 Extraindo áudio com ffmpeg...")
            mp3_path = extrair_audio(temp_video_path, "output")
            os.remove(temp_video_path)

            if mp3_path:
                status.write("🧠 Transcrevendo com Whisper...")
                transcricao = transcrever_audio(mp3_path)
                st.markdown("### 📝 Transcrição")
                st.code(transcricao, language="text")  # ✅ Copiar habilitado
                salvar_transcricao(transcricao, nome_base)

                if transcricao:
                    status.write("🤖 Enviando transcrição para Gemini...")
                    resposta = chamar_gemini(transcricao, contexto, modelo_gemini)
                    st.markdown("### 🤖 Resultado da IA")
                    st.code(resposta, language="markdown")  # ✅ Copiar habilitado
                    salvar_resposta_ia(resposta, nome_base)

            status.update(label="✅ Processamento concluído!", state="complete", expanded=False)
            st.session_state.processando = False

elif modo == "🎵 Importar apenas MP3":
    mp3_file = st.file_uploader("🎵 Envie o arquivo MP3", type=["mp3"])
    if mp3_file and modelo_gemini:
        nome_base = os.path.splitext(mp3_file.name)[0]
        st.markdown("## 🚦 Controle de Processamento")
        if mostrar_controles_de_processo():
            status = st.status("Iniciando transcrição...", expanded=True)
            temp_mp3_path = f"temp_{mp3_file.name}"
            with open(temp_mp3_path, "wb") as f:
                f.write(mp3_file.read())

            status.write("🧠 Transcrevendo com Whisper...")
            transcricao = transcrever_audio(temp_mp3_path)
            st.markdown("### 📝 Transcrição")
            st.code(transcricao, language="text")  # ✅ Copiar habilitado
            salvar_transcricao(transcricao, nome_base)

            if transcricao:
                status.write("🤖 Enviando transcrição para Gemini...")
                resposta = chamar_gemini(transcricao, contexto, modelo_gemini)
                st.markdown("### 🤖 Resultado da IA")
                st.code(resposta, language="markdown")  # ✅ Copiar habilitado
                salvar_resposta_ia(resposta, nome_base)

            os.remove(temp_mp3_path)
            status.update(label="✅ Processamento concluído!", state="complete", expanded=False)
            st.session_state.processando = False

elif modo == "📝 Importar apenas transcrição":
    txt_file = st.file_uploader("📝 Envie o arquivo de transcrição (.txt)", type=["txt"])
    if txt_file and modelo_gemini:
        nome_base = os.path.splitext(txt_file.name)[0]
        transcricao = txt_file.read().decode("utf-8")
        st.markdown("### 📝 Transcrição")
        st.code(transcricao, language="text")  # ✅ Copiar habilitado
        salvar_transcricao(transcricao, nome_base)

        st.markdown("## 🚦 Controle de Processamento")
        if mostrar_controles_de_processo():
            status = st.status("Enviando para IA Gemini...", expanded=True)
            resposta = chamar_gemini(transcricao, contexto, modelo_gemini)
            st.markdown("### 🤖 Resultado da IA")
            st.code(resposta, language="markdown")  # ✅ Copiar habilitado
            salvar_resposta_ia(resposta, nome_base)

            status.update(label="✅ Processamento concluído!", state="complete", expanded=False)
            st.session_state.processando = False
