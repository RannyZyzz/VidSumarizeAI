## 📜 Descrição do Projeto

**VidSummarizeAI** é uma ferramenta automatizada que transforma vídeos em resumos estruturados em Markdown. O sistema realiza três etapas principais:

1. **Extração de áudio dos vídeos (via FFmpeg)**
2. **Transcrição do áudio com o modelo Whisper da OpenAI**
3. **Geração de resumos inteligentes com a API Gemini do Google**

Você pode personalizar o comportamento da IA fornecendo instruções adicionais ou deixar que o sistema use um prompt padrão para gerar resumos concisos.

Ideal para jornalistas, criadores de conteúdo, pesquisadores ou qualquer pessoa que deseje extrair informações rápidas e organizadas de vídeos gravados.

---

## 📂 Estrutura Geral

```
📁 seu_projeto/
├── seu_script.py
├── 📁 Resultados_IA/
│   └── nome_do_video_resultado_IA.md
├── 📁 Conversao/
│   └── nome_do_video/
│       └── nome_do_video.mp3
```

---

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8+
- Instalar dependências via `pip`:

```bash
pip install -r requirements.txt
```

### Executando

1. Certifique-se de ter a chave da API Gemini (Google AI Studio).
2. Atualize a chave diretamente no script ou use uma variável de ambiente.
3. Execute o script:

```bash
python index.py
```

4. Quando solicitado, forneça o caminho da pasta contendo os vídeos.
5. Para cada vídeo, o sistema irá:
   - Extrair o áudio
   - Transcrever o conteúdo com Whisper
   - Perguntar se você deseja adicionar uma instrução personalizada para a IA
   - Enviar para o Gemini e salvar o resultado em `.md`

---

## 🧠 Funcionalidades

- ✅ Suporte a múltiplos formatos de vídeo (.mp4, .mkv, .avi, etc.)
- ✅ Transcrição automática com Whisper
- ✅ Geração de conteúdo com instruções personalizadas (via Gemini)
- ✅ Salvamento automático dos resumos em formato Markdown
- ✅ Interface interativa via terminal

---

## ⚙️ Tecnologias Usadas

- Python 3
- [Whisper (OpenAI)](https://github.com/openai/whisper)
- [Google Gemini API](https://ai.google.dev)
- FFmpeg

---

## 🔒 Observações de Segurança

A chave da API Gemini está atualmente hardcoded no script. Para produção, recomenda-se fortemente o uso de variáveis de ambiente para manter a segurança.

```python
api_key = os.getenv("GEMINI_API_KEY")
```

---

## 🛠️ Melhorias Futuras

- Interface gráfica (GUI)
- Suporte a múltiplas línguas na transcrição
- Geração de slides/resumos visuais
- Upload direto de arquivos no Google Drive ou Notion

---

## 🧑‍💻 Autor

- Desenvolvido por [Ranniêr Reis]
- Contribuições são bem-vindas!

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
