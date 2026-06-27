import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="LicitaAI - Plataforma", page_icon="📄", layout="centered")

st.title("📄 LicitaAI")
st.subheader("Automação Inteligente de Processos Licitatórios")
st.write("Faça o upload do edital e deixe nossa IA extrair os requisitos e prazos críticos.")

# Área de Upload
arquivo_pdf = st.file_uploader("Selecione o Edital (PDF)", type=["pdf"])

if st.button("Analisar Edital com IA"):
    if arquivo_pdf is not None:
        with st.spinner("Nossa IA está lendo o documento..."):
            
            # Preparando o arquivo para enviar ao Backend
            files = {"file": (arquivo_pdf.name, arquivo_pdf.getvalue(), "application/pdf")}
            
            try:
                # Fazendo a requisição para a nossa API FastAPI
                resposta = requests.post("http://localhost:8000/analisar-edital/", files=files)
                
                if resposta.status_code == 200:
                    dados = resposta.json()["analise_ia"]
                    
                    st.success("Análise concluída com sucesso!")
                    
                    # Exibindo os resultados de forma estruturada e amigável
                    st.markdown("### 📌 Resumo do Edital")
                    st.write(f"**Objeto:** {dados['objeto']}")
                    st.write(f"**Valor Estimado:** {dados['valor_estimado']}")
                    
                    st.markdown("### ⏳ Prazos Críticos")
                    for prazo in dados['prazos_criticos']:
                        st.warning(prazo)
                        
                    st.markdown("### 📁 Documentação Exigida")
                    for doc in dados['documentacao_exigida']:
                        st.info(f"- {doc}")
                else:
                    st.error("Erro na comunicação com o servidor.")
            
            except requests.exceptions.ConnectionError:
                st.error("Servidor Backend não encontrado. Certifique-se de que o FastAPI está rodando.")
    else:
        st.warning("Por favor, faça o upload de um arquivo PDF antes de analisar.")