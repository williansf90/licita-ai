from fastapi import FastAPI, UploadFile, File
import uvicorn
import time

app = FastAPI(title="LicitaAI API", description="API para automação de editais")

@app.get("/")
def read_root():
    return {"status": "A API da LicitaAI está online!"}

@app.post("/analisar-edital/")
async def analisar_edital(file: UploadFile = File(...)):
    # Aqui entra a futura lógica de extração de texto do PDF (ex: pdfplumber)
    # e o envio desse texto para o modelo de IA (Gemini/OpenAI).
    
    # Simulando o tempo de processamento da IA
    time.sleep(2) 
    
    # Retorno estruturado (JSON) simulando a resposta inteligente
    return {
        "nome_arquivo": file.filename,
        "analise_ia": {
            "objeto": "Aquisição de equipamentos de TI e infraestrutura",
            "valor_estimado": "R$ 150.000,00",
            "prazos_criticos": [
                "15/07/2026 - Data limite para envio da proposta",
                "20/07/2026 - Sessão pública de lances"
            ],
            "documentacao_exigida": [
                "Certidão Negativa de Débitos Trabalhistas (CNDT)",
                "Balanço Patrimonial do último exercício",
                "Atestado de Capacidade Técnica"
            ]
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)