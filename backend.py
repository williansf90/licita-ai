from fastapi import FastAPI, UploadFile, File
import uvicorn
import pdfplumber
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Carrega a chave do arquivo .env protegido
load_dotenv()

app = FastAPI(title="LicitaAI API", description="API com IA real conectada")

CHAVE_API = os.getenv("GEMINI_API_KEY")
if not CHAVE_API:
    raise ValueError("Chave da API do Gemini não encontrada no arquivo .env")

# Configura a biblioteca do Google com a sua chave liberada
genai.configure(api_key=CHAVE_API)

@app.get("/")
def read_root():
    return {"status": "A API da LicitaAI está online com IA real ativa!"}

@app.post("/analisar-edital/")
async def analisar_edital(file: UploadFile = File(...)):
    try:
        # 1. Extração do texto do PDF enviado pelo Streamlit
        texto_edital = ""
        with pdfplumber.open(file.file) as pdf:
            # Lendo as 5 primeiras páginas para extrair dados profundos do edital
            for page in pdf.pages[:5]: 
                texto_edital += page.extract_text() + "\n"

        # 2. Inicializando o modelo que está liberado na sua conta
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # 3. Engenharia de Prompt para garantir o retorno em JSON estruturado
        prompt = f"""
        Você é um assistente especialista em licitações públicas chamado LicitaAI.
        Leia o trecho do edital abaixo e extraia as seguintes informações estritamente em formato JSON.
        Não adicione nenhuma introdução, nenhuma conclusão e nenhum bloco de código markdown (como ```json).
        Retorne APENAS o objeto JSON.
        
        Formato esperado:
        {{
            "objeto": "Texto resumido explicando claramente o que a prefeitura/órgão está contratando ou adquirindo",
            "valor_estimado": "Valor monetário total estimado no edital, formatado em R$. Se não houver, escreva 'Não informado'",
            "prazos_criticos": ["Data limite para propostas: DD/MM/AAAA", "Data da sessão pública: DD/MM/AAAA"],
            "documentacao_exigida": ["Documento essencial 1", "Documento essencial 2", "Certidão importante"]
        }}

        Edital:
        {texto_edital}
        """

        # 4. Chamada real para a API do Google
        response = model.generate_content(prompt)
        
        # Limpeza de segurança caso a IA insira formatações de markdown na resposta
        texto_resposta = response.text.strip()
        if texto_resposta.startswith("```json"):
            texto_resposta = texto_resposta.replace("```json", "", 1)
        if texto_resposta.endswith("```"):
            texto_resposta = texto_resposta[:-3]
        texto_resposta = texto_resposta.strip()
        
        # 5. Converte a resposta em dicionário Python
        dados_ia = json.loads(texto_resposta)

        return {
            "nome_arquivo": file.filename,
            "analise_ia": dados_ia
        }

    except Exception as e:
        # Se algo falhar na extração ou na IA, o frontend exibirá o motivo real em vermelho
        return {"erro": f"Erro no processamento da IA: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)