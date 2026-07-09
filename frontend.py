import streamlit as st
import pdfplumber
import google.generativeai as genai
import json
import os

# 1. Configuração da página
st.set_page_config(page_title="LicitaAI - Plataforma", page_icon="📄", layout="wide")

# 2. Configuração Segura da Chave de API
CHAVE_API = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not CHAVE_API:
    st.error("⚠️ Chave de API não encontrada nas configurações do sistema.")
else:
    genai.configure(api_key=CHAVE_API)

# 3. Construção da Barra Lateral
with st.sidebar:
    st.title("📄 LicitaAI")
    st.markdown("### Automação de Editais")
    st.write("Faça o upload do edital em PDF para iniciar a extração inteligente.")
    
    st.divider() 
    
    arquivo_pdf = st.file_uploader("Selecione o arquivo", type=["pdf"])
    analisar_btn = st.button("Analisar Edital", type="primary", use_container_width=True)

# 4. Processamento Principal (Backend integrado)
if analisar_btn:
    if arquivo_pdf is not None:
        with st.spinner("A IA está lendo o documento e extraindo os dados críticos..."):
            try:
                # Extração de texto
                texto_edital = ""
                with pdfplumber.open(arquivo_pdf) as pdf:
                    limite_paginas = min(20, len(pdf.pages))
                    for i in range(limite_paginas):
                        pagina_texto = pdf.pages[i].extract_text()
                        if pagina_texto:
                            texto_edital += pagina_texto + "\n"

                # Chamada da IA
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"""
                Você é um assistente especialista em licitações públicas chamado LicitaAI.
                Leia o trecho do edital abaixo e extraia as seguintes informações estritamente em formato JSON.
                Não adicione nenhuma introdução, nenhuma conclusão e nenhum bloco de código markdown (como ```json).
                Retorne APENAS o objeto JSON.
                
                Formato esperado:
                {{
                    "objeto": "Texto resumido explicando claramente o que está sendo contratado",
                    "valor_estimado": "Valor monetário total estimado, formatado em R$. Se não houver, escreva 'Não informado'",
                    "prazos_criticos": ["Prazo 1", "Prazo 2"],
                    "documentacao_exigida": ["Doc 1", "Doc 2"]
                }}

                Edital:
                {texto_edital}
                """

                response = model.generate_content(prompt, request_options={"timeout": 60})
                
                # Limpeza da resposta
                texto_resposta = response.text.strip()
                if texto_resposta.startswith("```json"):
                    texto_resposta = texto_resposta.replace("```json", "", 1)
                if texto_resposta.endswith("```"):
                    texto_resposta = texto_resposta[:-3]
                texto_resposta = texto_resposta.strip()
                
                dados = json.loads(texto_resposta)

                # --- DASHBOARD VISUAL ---
                st.success(f"Análise concluída com sucesso! ({limite_paginas} páginas processadas)")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader("📌 Objeto da Licitação")
                    st.info(dados.get('objeto', 'N/A'))
                with col2:
                    st.subheader("💰 Valor Estimado")
                    st.success(dados.get('valor_estimado', 'N/A'))
                    
                st.divider()
                
                col3, col4 = st.columns(2)
                with col3:
                    st.subheader("⏳ Prazos Críticos")
                    for prazo in dados.get('prazos_criticos', []):
                        st.warning(f"• {prazo}")
                with col4:
                    st.subheader("📁 Documentação Exigida")
                    for doc in dados.get('documentacao_exigida', []):
                        st.markdown(f"- {doc}")

            except Exception as e:
                st.error(f"Erro no processamento: {str(e)}")
    else:
        st.warning("⚠️ Por favor, selecione um arquivo PDF na barra lateral primeiro.")
else:
    st.markdown("## Bem-vindo à LicitaAI")
    st.write("👈 Utilize a barra lateral à esquerda para enviar um edital e testar a automação em tempo real.")
    st.info("A inteligência artificial fará a leitura estruturada do objeto, valor, documentação e prazos em poucos segundos.")