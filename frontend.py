import streamlit as st
import requests

# 1. Configuração da página (agora usando 'wide' para aproveitar melhor a tela)
st.set_page_config(page_title="LicitaAI - Plataforma", page_icon="📄", layout="wide")

# 2. Construção da Barra Lateral (Sidebar)
with st.sidebar:
    st.title("📄 LicitaAI")
    st.markdown("### Automação de Editais")
    st.write("Faça o upload do edital em PDF para iniciar a extração inteligente.")
    
    st.divider() # Linha divisória para organizar visualmente
    
    arquivo_pdf = st.file_uploader("Selecione o arquivo", type=["pdf"])
    
    # Botão de análise agora fica na barra lateral e ganha destaque (primary)
    analisar_btn = st.button("Analisar Edital", type="primary", use_container_width=True)

# 3. Construção da Área Principal (Dashboard)
if analisar_btn:
    if arquivo_pdf is not None:
        with st.spinner("A IA está lendo o documento e extraindo os dados críticos..."):
            
            files = {"file": (arquivo_pdf.name, arquivo_pdf.getvalue(), "application/pdf")}
            
            try:
                resposta = requests.post("http://localhost:8000/analisar-edital/", files=files)
                
                if resposta.status_code == 200:
                    resposta_json = resposta.json()
                    
                    if "erro" in resposta_json:
                        st.error(f"Erro no servidor: {resposta_json['erro']}")
                    else:
                        dados = resposta_json["analise_ia"]
                        paginas = resposta_json.get("paginas_lidas", "N/A")
                        
                        st.success(f"Análise concluída com sucesso! ({paginas} páginas processadas)")
                        
                        # --- INÍCIO DO DASHBOARD VISUAL ---
                        
                        # Linha superior: Objeto (maior) e Valor Estimado (menor)
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.subheader("📌 Objeto da Licitação")
                            st.info(dados.get('objeto', 'N/A'))
                            
                        with col2:
                            st.subheader("💰 Valor Estimado")
                            st.success(dados.get('valor_estimado', 'N/A'))
                            
                        st.divider()
                        
                        # Linha inferior: Prazos e Documentação lado a lado
                        col3, col4 = st.columns(2)
                        with col3:
                            st.subheader("⏳ Prazos Críticos")
                            for prazo in dados.get('prazos_criticos', []):
                                st.warning(f"• {prazo}")
                                
                        with col4:
                            st.subheader("📁 Documentação Exigida")
                            for doc in dados.get('documentacao_exigida', []):
                                st.markdown(f"- {doc}")
                                
                        # --- FIM DO DASHBOARD VISUAL ---
                        
                else:
                    st.error("Erro na comunicação com o servidor.")
            
            except requests.exceptions.ConnectionError:
                st.error("Servidor Backend não encontrado. Certifique-se de que o FastAPI está rodando.")
    else:
        st.warning("⚠️ Por favor, selecione um arquivo PDF na barra lateral primeiro.")
else:
    # Tela de boas-vindas exibida antes de qualquer análise
    st.markdown("## Bem-vindo à LicitaAI")
    st.write("👈 Utilize a barra lateral à esquerda para enviar um edital e testar a automação em tempo real.")
    st.info("A inteligência artificial fará a leitura estruturada do objeto, valor, documentação e prazos em poucos segundos.")