# 📄 LicitaAI - Plataforma Inteligente para Automação de Processos Licitatórios

## 🎯 Visão Geral
A LicitaAI é uma startup de base tecnológica desenvolvida para automatizar processos relacionados a licitações públicas por meio de Inteligência Artificial. O projeto busca solucionar problemas associados à análise manual de editais, organização documental e acompanhamento de prazos, reduzindo o tempo operacional e mitigando falhas humanas.

## 🚀 Prova de Conceito (PoC)
Este repositório contém o Produto Mínimo Viável (MVP) da plataforma, focando no processo crítico de análise preliminar de documentos. A aplicação permite que o usuário faça o upload de um edital em PDF e utiliza Inteligência Artificial Generativa (Google Gemini) para extrair automaticamente:
- Objeto da licitação
- Valor estimado
- Prazos críticos
- Documentação exigida

## 🛠️ Stack Tecnológico
- **Frontend:** Streamlit (Interface de usuário ágil e interativa)
- **Backend:** FastAPI (Servidor assíncrono para chamadas de rede e processamento de arquivos)
- **Processamento de PDF:** pdfplumber
- **Inteligência Artificial:** Google Generative AI (Modelo: gemini-flash-latest)