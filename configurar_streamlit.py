import os
import toml

def criar_secrets_toml(api_key):
    home = os.path.expanduser("~")
    pasta_streamlit = os.path.join(home, ".streamlit")
    os.makedirs(pasta_streamlit, exist_ok=True)

    caminho_secrets = os.path.join(pasta_streamlit, "secrets.toml")

    dados = {}
    if os.path.exists(caminho_secrets):
        with open(caminho_secrets, "r", encoding="utf-8") as f:
            dados = toml.load(f)

    dados["GEMINI_API_KEY"] = api_key

    with open(caminho_secrets, "w", encoding="utf-8") as f:
        toml.dump(dados, f)

    print(f"✅ Chave adicionada com sucesso em {caminho_secrets}.")


def configurar_max_upload(tamanho_mb=1000):
    home = os.path.expanduser("~")
    pasta_streamlit = os.path.join(home, ".streamlit")
    os.makedirs(pasta_streamlit, exist_ok=True)

    config_path = os.path.join(pasta_streamlit, "config.toml")

    dados = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            dados = toml.load(f)

    if "server" not in dados:
        dados["server"] = {}

    dados["server"]["maxUploadSize"] = tamanho_mb

    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(dados, f)

    print(f"✅ Tamanho máximo de upload ajustado para {tamanho_mb}MB em {config_path}.")


# ===================== EXECUÇÃO =====================

if __name__ == "__main__":
    print("🔐 Configuração da API do Gemini")
    print("🌐 Caso ainda não tenha sua chave de API, gere uma em:")
    print("👉 https://aistudio.google.com/apikey\n")

    chave = input("Informe sua GEMINI_API_KEY: ").strip()
    if not chave:
        print("❌ Nenhuma chave foi fornecida. Abortando.")
    else:
        criar_secrets_toml(chave)
        configurar_max_upload()
        print("🎉 Configuração concluída com sucesso!")
