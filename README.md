# 📄 LicitaAI - Plataforma Inteligente para Automação de Processos Licitatórios

## 🌐 Acesso ao Sistema (Live Demo)
A Prova de Conceito (PoC) da LicitaAI está em produção e pode ser acessada de qualquer dispositivo através do link abaixo:
👉 **[Acessar a LicitaAI no Streamlit Cloud](https://licita-ai.streamlit.app/)**

---

## 🎯 Visão Geral
A LicitaAI é uma startup de base tecnológica desenvolvida para automatizar processos relacionados a licitações públicas por meio de Inteligência Artificial. O projeto busca solucionar problemas associados à análise manual de editais, organização documental e acompanhamento de prazos, reduzindo o tempo operacional e mitigando falhas humanas.

## 🚀 Prova de Conceito (MVP)
Este repositório contém o Produto Mínimo Viável da plataforma, focando no processo crítico de análise preliminar de documentos. A aplicação permite que o usuário faça o upload de um edital em PDF e utiliza Inteligência Artificial Generativa para extrair automaticamente:
- Objeto da licitação
- Valor estimado
- Prazos críticos
- Documentação exigida

## 🛠️ Stack Tecnológico
Para garantir alta performance e disponibilidade na nuvem, o projeto adota uma arquitetura ágil e unificada:
- **Interface e Servidor Web:** Streamlit e Streamlit Community Cloud
- **Processamento de PDF:** `pypdf` (Otimizado para extração rápida de texto)
- **Inteligência Artificial:** Google Generative AI (Modelo: `gemini-flash-latest`)

## ⚙️ Como rodar a aplicação localmente

### 1. Pré-requisitos
- Python 3.10 ou superior.
- Uma chave de API válida do Google AI Studio.

### 2. Instalação
Clone este repositório e instale as dependências listadas no `requirements.txt`:
```bash
git clone [https://github.com/SEU-USUARIO/licita-ai.git](https://github.com/williansf90/licita-ai.git)
cd licita-ai
pip install -r requirements.txt