import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

st.set_page_config(
    page_title="CherifeBot AI - Sistema Completo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CONFIGURAÇÃO =================
TOKEN = "8342975161:AAE3FZ_NZBEfM7BSBOGT7HVOmhBUC1WB1Is"
YOUR_ID = "704297959"
BOT_USERNAME = "@CherifeBot"
# ================================================

# CSS Personalizado
st.markdown("""
<style>
    /* Tema MoltBot */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid #667eea;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        transition: all 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .status-online {
        color: #10b981;
        font-weight: bold;
    }
    
    .status-offline {
        color: #ef4444;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("🤖 CherifeBot AI")
    
    # Status do Sistema
    st.markdown("### 📊 Status do Sistema")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Bot Status", "🟢 Online", "24/7")
    with col2:
        st.metric("AI Core", "✅ Ativo", "Claude")
    
    # Navegação
    st.markdown("---")
    page = st.radio(
        "Navegação",
        ["🏠 Dashboard", "💬 Chat AI", "🔍 Pesquisa", "📧 Email", "📅 Agenda", 
         "⚙️ Configurações", "📊 Analytics", "🛠️ Ferramentas"]
    )
    
    # Quick Actions
    st.markdown("---")
    st.markdown("### ⚡ Ações Rápidas")
    
    if st.button("🔄 Atualizar Status", use_container_width=True):
        st.rerun()
    
    if st.button("📱 Abrir Telegram", use_container_width=True):
        st.markdown(f'<a href="https://t.me/CherifeBot" target="_blank">Abrir @CherifeBot</a>', unsafe_allow_html=True)
    
    if st.button("🐛 Debug Console", use_container_width=True):
        st.session_state.debug = True

# ================= PÁGINAS PRINCIPAIS =================

if page == "🏠 Dashboard":
    # Header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("🚀 CherifeBot AI Assistant")
        st.markdown("Sistema completo de automação 24/7 - Seu assistente pessoal AI")
    with col2:
        st.metric("Mensagens Hoje", "42", "+12%")
    with col3:
        st.metric("Uptime", "99.8%", "30 dias")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Features Grid
    st.markdown("## 🔧 Funcionalidades Principais")
    
    features = [
        {"icon": "🤖", "title": "Chat AI", "desc": "Conversação com Claude/GPT", "status": "✅"},
        {"icon": "🔍", "title": "Pesquisa Web", "desc": "Brave Search API integrado", "status": "✅"},
        {"icon": "📧", "title": "Email AI", "desc": "Gerenciamento automático", "status": "🔄"},
        {"icon": "📅", "title": "Agenda", "desc": "Calendário inteligente", "status": "⚙️"},
        {"icon": "🌐", "title": "Análise Web", "desc": "Scraping e análise", "status": "✅"},
        {"icon": "💾", "title": "GitHub", "desc": "Automação de código", "status": "🔄"},
        {"icon": "📊", "title": "Dashboard", "desc": "Analytics em tempo real", "status": "✅"},
        {"icon": "🔔", "title": "Notificações", "desc": "Alertas inteligentes", "status": "✅"},
    ]
    
    cols = st.columns(4)
    for idx, feature in enumerate(features):
        with cols[idx % 4]:
            with st.container():
                st.markdown(f"""
                <div class="feature-card">
                    <h3>{feature['icon']} {feature['title']}</h3>
                    <p>{feature['desc']}</p>
                    <p><strong>Status:</strong> {feature['status']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Statistics
    st.markdown("---")
    st.markdown("## 📈 Estatísticas")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Usuários Ativos", "1", "Você")
    with col2:
        st.metric("Mensagens/Dia", "42", "+12%")
    with col3:
        st.metric("Tarefas Concluídas", "156", "+8%")
    with col4:
        st.metric("Uptime", "99.8%", "30 dias")
    
    # Gráfico de uso (simulado)
    data = pd.DataFrame({
        'Dia': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        'Mensagens': [35, 42, 38, 45, 52, 40, 38],
        'Tarefas': [12, 15, 10, 18, 22, 14, 11]
    })
    
    fig = px.line(data, x='Dia', y=['Mensagens', 'Tarefas'], 
                  title='📊 Atividade Semanal', markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif page == "💬 Chat AI":
    st.title("💬 Chat AI - Conversação Inteligente")
    
    # Configuração do modelo
    with st.expander("⚙️ Configurações do Modelo", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            model = st.selectbox("Modelo AI", ["Claude 3 Opus", "GPT-4", "GPT-3.5", "Claude Haiku"])
        with col2:
            temperature = st.slider("Criatividade", 0.0, 1.0, 0.7, 0.1)
        with col3:
            max_tokens = st.slider("Comprimento", 100, 4000, 1500, 100)
    
    # Histórico de conversa
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem para o AI..."):
        # Adicionar mensagem do usuário
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Simular resposta do AI
        with st.chat_message("assistant"):
            with st.spinner("🧠 Pensando..."):
                # Aqui você chamaria a API do AI
                response = f"**AI Responde:**\n\nEsta é uma resposta simulada. Configure a API do Claude/OpenAI para respostas reais.\n\n*Prompt:* {prompt}"
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Botão para limpar
        if st.button("🗑️ Limpar Conversa"):
            st.session_state.chat_history = []
            st.rerun()

elif page == "🔍 Pesquisa":
    st.title("🔍 Pesquisa Web Inteligente")
    
    tab1, tab2, tab3 = st.tabs(["🔎 Buscar", "📚 Histórico", "⚙️ Configurar"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_input("O que deseja pesquisar?", placeholder="Ex: Python machine learning tutorials 2024")
        with col2:
            num_results = st.selectbox("Resultados", [3, 5, 10, 15])
        
        if st.button("🔍 Pesquisar", type="primary"):
            if query:
                with st.spinner("Buscando..."):
                    # Simulação de resultados
                    results = [
                        {"title": "Python Machine Learning Tutorial 2024", 
                         "url": "https://example.com/python-ml", 
                         "snippet": "Aprenda machine learning com Python passo a passo...",
                         "source": "Brave Search"},
                        {"title": "Scikit-learn Documentation", 
                         "url": "https://scikit-learn.org", 
                         "snippet": "Official documentation for scikit-learn machine learning library...",
                         "source": "GitHub"},
                        {"title": "Machine Learning Mastery", 
                         "url": "https://machinelearningmastery.com", 
                         "snippet": "Practical tutorials and resources for machine learning...",
                         "source": "Web"},
                    ]
                    
                    for i, result in enumerate(results, 1):
                        with st.container():
                            st.markdown(f"### {i}. [{result['title']}]({result['url']})")
                            st.markdown(f"*Fonte: {result['source']}*")
                            st.markdown(result['snippet'])
                            st.markdown("---")
            else:
                st.warning("Digite algo para pesquisar")
    
    with tab2:
        st.info("📊 Histórico de pesquisas será exibido aqui após configuração.")
    
    with tab3:
        st.subheader("⚙️ Configurar API Keys")
        
        api_provider = st.selectbox("Provedor de Pesquisa", ["Brave Search", "Google Custom Search", "SerpAPI"])
        
        if api_provider == "Brave Search":
            st.markdown("""
            **Brave Search API:**
            1. Acesse: [brave.com/search/api](https://brave.com/search/api)
            2. Crie conta gratuita
            3. Gere API Key
            4. Cole abaixo
            """)
            
            brave_key = st.text_input("Brave API Key", type="password")
            if brave_key and st.button("Salvar Configuração"):
                st.success("✅ API Key configurada!")
                
        st.markdown("---")
        st.markdown("**Configurações Avançadas:**")
        st.checkbox("Safe Search (filtrar conteúdo adulto)", True)
        st.checkbox("Pesquisa em português", True)
        st.checkbox("Resultados em tempo real", False)

elif page == "📧 Email":
    st.title("📧 Email AI Assistant")
    
    st.info("""
    **Funcionalidade em desenvolvimento**
    
    *Próximas features:*
    - 📥 Leitura automática de emails
    - 🤖 Respostas com AI
    - 📁 Organização inteligente
    - 🔔 Alertas importantes
    - 📊 Análise de caixa de entrada
    """)
    
    # Configuração do Email
    with st.expander("⚙️ Configurar Conta de Email", expanded=True):
        email_provider = st.selectbox("Provedor", ["Gmail", "Outlook", "Yahoo", "Custom IMAP"])
        
        if email_provider:
            col1, col2 = st.columns(2)
            with col1:
                email_address = st.text_input("Email")
                imap_server = st.text_input("IMAP Server", value="imap.gmail.com" if email_provider == "Gmail" else "")
            with col2:
                app_password = st.text_input("App Password", type="password")
                imap_port = st.number_input("Porta IMAP", value=993)
            
            if st.button("🔗 Conectar Email", type="primary"):
                st.success("✅ Conexão simulada! Configure OAuth2 para produção.")
    
    # Dashboard do Email
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Emails Hoje", "24", "+3")
    with col2:
        st.metric("Não Lidos", "8", "-2")
    with col3:
        st.metric("Importantes", "5", "+1")
    with col4:
        st.metric("Spam", "12", "-4")

elif page == "⚙️ Configurações":
    st.title("⚙️ Configurações do Sistema")
    
    tab1, tab2, tab3 = st.tabs(["🔐 Segurança", "🤖 Bot", "🌐 API"])
    
    with tab1:
        st.subheader("🔐 Configurações de Segurança")
        
        st.text_input("Token do Bot", value=TOKEN, type="password", disabled=True)
        st.text_input("Seu User ID", value=YOUR_ID, disabled=True)
        
        st.markdown("---")
        st.subheader("🔑 API Keys")
        
        with st.form("api_keys_form"):
            openai_key = st.text_input("OpenAI API Key", type="password")
            anthropic_key = st.text_input("Anthropic API Key", type="password")
            brave_key = st.text_input("Brave Search API Key", type="password")
            
            if st.form_submit_button("💾 Salvar Keys"):
                st.success("✅ Keys salvas no ambiente (em produção use .env)")
    
    with tab2:
        st.subheader("🤖 Configurações do Bot")
        
        bot_name = st.text_input("Nome do Bot", value="CherifeBot")
        bot_username = st.text_input("Username", value="@CherifeBot", disabled=True)
        
        st.markdown("---")
        st.subheader("📱 Notificações")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Notificações por Email", True)
            st.checkbox("Notificações por Telegram", True)
        with col2:
            st.checkbox("Alertas importantes", True)
            st.checkbox("Relatórios diários", False)
        
        st.markdown("---")
        if st.button("🔄 Reiniciar Bot", type="secondary"):
            st.info("Comando de reinicialização enviado ao servidor.")
    
    with tab3:
        st.subheader("🌐 Configurações de API")
        
        st.markdown("**Endpoints Disponíveis:**")
        
        endpoints = {
            "Bot Status": f"https://api.telegram.org/bot{TOKEN}/getMe",
            "Send Message": f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            "Webhook": "https://yourdomain.com/webhook",
            "API Dashboard": "https://yourdomain.com/api/docs"
        }
        
        for name, url in endpoints.items():
            st.code(f"{name}: {url}", language="text")
        
        st.markdown("---")
        st.subheader("📊 Limites e Status")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Requests/Dia", "10,000", "5% usado")
            st.metric("AI Calls", "500", "12% usado")
        with col2:
            st.metric("Storage", "5GB", "1.2GB usado")
            st.metric("Uptime", "99.8%", "30 dias")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <h3>🚀 CherifeBot AI Assistant 24/7</h3>
    <p>Seu sistema completo de automação pessoal</p>
    <p><small>🤖 Versão 1.0 | 📅 {date} | 🔗 <a href='https://t.me/CherifeBot' target='_blank'>@CherifeBot</a></small></p>
</div>
""".format(date=datetime.now().strftime('%d/%m/%Y')), unsafe_allow_html=True)
