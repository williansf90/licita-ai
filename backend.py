from fastapi import FastAPI, UploadFile, File
import uvicorn
import pdfplumber
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LicitaAI API", description="API com leitura estendida e segurança anti-travamento")

CHAVE_API = os.getenv("GEMINI_API_KEY")
if not CHAVE_API:
    raise ValueError("Chave da API do Gemini não encontrada no arquivo .env")

genai.configure(api_key=CHAVE_API)

@app.get("/")
def read_root():
    return {"status": "A API da LicitaAI está online!"}

@app.post("/analisar-edital/")
async def analisar_edital(file: UploadFile = File(...)):
    try:
        texto_edital = ""
        with pdfplumber.open(file.file) as pdf:
            limite_paginas = min(40, len(pdf.pages))
            
            for i in range(limite_paginas):
                pagina_texto = pdf.pages[i].extract_text()
                if pagina_texto:  # Evita erro caso uma página seja apenas imagem
                    texto_edital += pagina_texto + "\n"

        model = genai.GenerativeModel('gemini-flash-latest')
        
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

        # SEGURANÇA 2: Define um tempo máximo (timeout) de 60 segundos para a IA responder
        response = model.generate_content(
            prompt,
            request_options={"timeout": 60}
        )
        
        # Limpeza e formatação
        texto_resposta = response.text.strip()
        if texto_resposta.startswith("```json"):
            texto_resposta = texto_resposta.replace("```json", "", 1)
        if texto_resposta.endswith("```"):
            texto_resposta = texto_resposta[:-3]
        texto_resposta = texto_resposta.strip()
        
        dados_ia = json.loads(texto_resposta)

        return {
            "nome_arquivo": file.filename,
            "paginas_lidas": limite_paginas,
            "analise_ia": dados_ia
        }

    except Exception as e:
        return {"erro": f"Erro no processamento: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)