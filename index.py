import os
import subprocess
import whisper
import google.generativeai as genai

def configurar_api_gemini():
    """Configura a API do Gemini a partir de uma variável de ambiente."""
    try:
        api_key = "GEMINI_API_KEY"
        if not api_key:
            print("Erro: A variável de ambiente 'GEMINI_API_KEY' não foi definida.")
            print("Por favor, configure sua chave de API antes de executar o script.")
            return None
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        print(f"Erro ao configurar a API do Gemini: {e}")
        return None

def chamar_gemini(transcricao, contexto_usuario, model):
    """
    Envia a transcrição e o contexto para a API Gemini e retorna o resultado.
    """
    if not model:
        return "Erro: Modelo do Gemini não foi inicializado."

    # Se não houver contexto, cria uma instrução padrão.
    if not contexto_usuario:
        instrucao = "Com base na transcrição a seguir, crie um resumo conciso e bem estruturado em formato Markdown."
    else:
        instrucao = contexto_usuario

    prompt = f"""
    **Instrução do Usuário:**
    {instrucao}

    ---

    **Texto da Transcrição para Análise:**
    {transcricao}
    """

    print("\n🤖 Enviando para a IA do Gemini...")
    try:
        response = model.generate_content(prompt)
        print("✅ Resposta da IA recebida!")
        return response.text
    except Exception as e:
        print(f"❌ Erro ao chamar a API do Gemini: {e}")
        return f"Erro ao processar com a IA: {e}"


def extrair_audio_e_salvar_unico(caminho_video, pasta_destino_base):
    if not os.path.exists(caminho_video):
        print(f"Erro: O arquivo '{caminho_video}' não foi encontrado.")
        return None

    nome_arquivo_video = os.path.basename(caminho_video)
    nome_base_video = os.path.splitext(nome_arquivo_video)[0]

    pasta_saida_audio = os.path.join(pasta_destino_base, "Conversao", nome_base_video)
    os.makedirs(pasta_saida_audio, exist_ok=True)

    caminho_mp3 = os.path.join(pasta_saida_audio, f"{nome_base_video}.mp3")

    print(f"\nExtraindo áudio de: '{nome_arquivo_video}'")
    print(f"Salvando MP3 em: '{caminho_mp3}'")

    try:
        comando_ffmpeg = [
            "ffmpeg",
            "-i", caminho_video,
            "-vn",
            "-ab", "320k",
            "-map_chapters", "-1",
            "-y", # Sobrescreve o arquivo de saída se ele existir
            caminho_mp3
        ]
        subprocess.run(comando_ffmpeg, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Áudio extraído com sucesso: '{caminho_mp3}'")
        return caminho_mp3

    except subprocess.CalledProcessError as e:
        print(f"Erro ao processar '{nome_arquivo_video}': {e}")
    except FileNotFoundError:
        print("Erro: FFmpeg não encontrado. Verifique se ele está instalado e no PATH do sistema.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return None

def transcrever_e_processar(file_path, pasta_destino_processamento, gemini_model):
    try:
        model = whisper.load_model("small")
        print(f"\n🎙️  Transcrevendo arquivo: {os.path.basename(file_path)}")

        result = model.transcribe(file_path)
        texto_transcrito = result.get("text", "").strip()

        if not texto_transcrito:
            print("⚠️ A transcrição resultou em um texto vazio. Pulando para o próximo.")
            return

        print("-----------------------------------")
        print("\n📝 Transcrição concluída:")
        print("-----------------------------------")
        # print(texto_transcrito)
        

        # === >>> NOVO TRECHO: SALVA TRANSCRIÇÃO EM .TXT NA PASTA "Transcricao"
        nome_base = os.path.splitext(os.path.basename(file_path))[0]
        pasta_transcricao = os.path.join(pasta_destino_processamento, "Transcricao")
        os.makedirs(pasta_transcricao, exist_ok=True)

        caminho_txt = os.path.join(pasta_transcricao, f"{nome_base}.txt")
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write(texto_transcrito)

        print(f"💾 Transcrição salva em: {caminho_txt}")
        # === <<< FIM DO NOVO TRECHO

        # <<< INTERAÇÃO COM O USUÁRIO
        contexto_usuario = ""
        while True:
            resposta = input("\nDeseja adicionar um contexto/instrução para a IA? (s/n): ").lower().strip()
            if resposta in ['s', 'sim']:
                contexto_usuario = input("Digite sua instrução: ")
                break
            elif resposta in ['n', 'nao', 'não']:
                print("✅ Encerrando o programa conforme solicitado pelo usuário.")
                exit()
            else:
                print("Resposta inválida. Por favor, digite 's' ou 'n'.")

        resultado_final = chamar_gemini(texto_transcrito, contexto_usuario, gemini_model)

        # Salva o resultado final em um arquivo .md
        pasta_saida = os.path.join(pasta_destino_processamento, nome_base)
        os.makedirs(pasta_saida, exist_ok=True)

        caminho_saida = os.path.join(pasta_saida, f"{nome_base}_resultado_IA.md")

        with open(caminho_saida, "w", encoding="utf-8") as f:
            f.write(resultado_final)

        print(f"💾 Resultado final salvo em: {caminho_saida}")

    except Exception as e:
        print(f"❌ Erro ao transcrever e processar '{file_path}': {e}")



def processar_videos(caminho_pasta_videos, gemini_model):
    if not os.path.isdir(caminho_pasta_videos):
        print(f"Erro: O caminho '{caminho_pasta_videos}' não é uma pasta válida.")
        return

    print(f"Iniciando processamento de vídeos em: '{caminho_pasta_videos}'")

    pasta_destino_base = os.path.dirname(caminho_pasta_videos) or os.getcwd()
    # Pasta para salvar os resultados .md
    pasta_resultados_ia = os.path.join(pasta_destino_base, "Resultados_IA")

    extensoes_video = (".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".mpeg", ".mpg")

    arquivos_videos = sorted([
        os.path.join(caminho_pasta_videos, arquivo)
        for arquivo in os.listdir(caminho_pasta_videos)
        if arquivo.lower().endswith(extensoes_video)
    ])

    if not arquivos_videos:
        print("Nenhum vídeo encontrado.")
        return

    for video in arquivos_videos:
        caminho_mp3 = extrair_audio_e_salvar_unico(video, pasta_destino_base)
        if caminho_mp3:
            transcrever_e_processar(caminho_mp3, pasta_resultados_ia, gemini_model)

    print("\n🎉 Processamento completo de todos os vídeos!")


if __name__ == "__main__":
    # Configura a API do Gemini no início
    modelo_gemini = configurar_api_gemini()
    
    if modelo_gemini:
        pasta_videos = input("Digite o caminho completo para a pasta com os vídeos: ").strip()
        processar_videos(pasta_videos, modelo_gemini)