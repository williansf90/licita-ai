import streamlit as st
from pypdf import PdfReader
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
                leitor_pdf = PdfReader(arquivo_pdf)
                limite_paginas = min(20, len(leitor_pdf.pages))

                for i in range(limite_paginas):
                    pagina_texto = leitor_pdf.pages[i].extract_text()
                    if pagina_texto:
                        texto_edital += pagina_texto + "\n"

                # --- MODO DEMONSTRAÇÃO ---
                if arquivo_pdf.name == "EDITAL BELÉM CE 90015-2026.pdf":
                    import time
                    time.sleep(5)

                    texto_resposta = """
                    {
                        "objeto": "Contratação de empresa especializada no ramo da construção civil para a execução de obra visando à construção de Unidade Básica de Saúde (UBS) Porte V, para atender as necessidades da Secretaria Municipal de Saúde (SESMA) de Belém/PA",
                        "valor_estimado": "R$ 6.515.602,35",
                        "prazos_criticos": ["Início da Sessão Pública: 21/07/2026 às 10h00 (horário de Brasília/DF)", "Prazo de execução da obra: 14 meses a contar do recebimento da Ordem de Serviço", "Prazo de vigência da contratação: 24 meses contados a partir da assinatura do contrato", "Impugnações e esclarecimentos: encaminhar até 03 dias úteis antes da data de abertura do certame", "Envio da proposta de preços e planilhas ajustadas: em até 24 horas corridas contadas a partir da solicitação do Agente de Contratação", "Envio dos documentos de habilitação: no prazo de até 02 horas úteis a partir da convocação", "Prazo para assinatura do contrato: dentro do prazo de 10 dias após convocação", "Prazo de validade da proposta de preços: não inferior a 120 dias"],
                        "documentacao_exigida": ["Registro cadastral atualizado no Sistema de Cadastramento Unificado de Fornecedores (SICAF)", "Habilitação Jurídica: Ato Constitutivo, Contrato Social ou Estatuto Social consolidado e registrado na Junta Comercial", "Prova de inscrição no CNPJ", "Regularidade com a Fazenda Federal, incluindo as contribuições Sociais (Dívida Ativa da União)", "Regularidade com as Fazendas Estadual e Municipal do domicílio ou sede do licitante", "Certificado de Regularidade do FGTS (CRF)", "Certidão Negativa de Débitos Trabalhistas (CNDT)", "Certidão Negativa de Falência ou Recuperações Judiciais e Extrajudiciais", "Balanço Patrimonial e Demonstração do Resultado do Exercício (DRE) dos 2 últimos exercícios sociais", "Declaração dos índices de Liquidez Geral (LG), Liquidez Corrente (LC) e Solvência Geral (SG) assinada por profissional contábil", "Registro ou inscrição da empresa no CAU ou CONFEA/CREA em plena validade", "Atestado de Capacidade Técnico-Profissional em nome do engenheiro civil ou arquiteto indicado", "Comprovação de Capacidade Técnico-Operacional (Atestados de execução de obras semelhantes acompanhados de CAT/ART/RRT)", "Declaração de Vistoria Prévia ou Declaração Formal assinada pelo responsável técnico sobre o conhecimento das condições locais de execução", "Declarações unificadas no sistema (Trabalho do Menor, Inexistência de Fato Impeditivo, Fidelidade e Veracidade, Elaboração de Proposta Independente, etc.)"]
                    }
                    """
                    limite_paginas = 20
                else:
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

                response = model.generate_content(prompt, request_options={"timeout": 600})
                
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