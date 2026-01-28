import streamlit as st
import requests
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="CherifeBot - Seu Assistente AI",
    page_icon="🤖",
    layout="wide"
)

# ================= CONFIGURAÇÃO =================
TOKEN = "8342975161:AAE3FZ_NZBEfM7BSBOGT7HVOmhBUCIbWBI1s"
YOUR_ID = "704297959"
BOT_USERNAME = "@CherifeBot"
# ================================================

# Título principal
st.title("🤖 CherifeBot - Seu Assistente AI 24/7")
st.markdown("---")

# Colunas para layout
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Status do Bot")
    
    # Testar conexão
    if st.button("🔗 Testar Conexão com Telegram", use_container_width=True):
        with st.spinner("Conectando..."):
            url = f"https://api.telegram.org/bot{TOKEN}/getMe"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ **CONECTADO COM SUCESSO!**")
                    st.json(data["result"])
                    
                    # Mostrar informações do bot
                    bot_info = data["result"]
                    st.info(f"""
                    **Informações do Bot:**
                    - Nome: {bot_info.get('first_name', 'N/A')}
                    - Usuário: @{bot_info.get('username', 'N/A')}
                    - ID: {bot_info.get('id', 'N/A')}
                    - Link: [t.me/{bot_info.get('username', '')}](https://t.me/{bot_info.get('username', '')})
                    """)
                else:
                    st.error(f"❌ Erro {response.status_code}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {e}")

with col2:
    st.header("👤 Suas Credenciais")
    
    st.code(f"""
Token: {TOKEN}
User ID: {YOUR_ID}
Bot: {BOT_USERNAME}
    """, language="text")
    
    st.warning("""
    ⚠️ **Mantenha essas informações em segurança!**
    - O token permite controlar seu bot
    - O User ID garante que só você use
    """)

st.markdown("---")

# Seção de controle do bot
st.header("🎮 Controle do Bot")

tab1, tab2, tab3 = st.tabs(["📨 Enviar Mensagem", "📊 Estatísticas", "⚙️ Configurações"])

with tab1:
    st.subheader("Enviar mensagem através do bot")
    
    # Para enviar mensagem para você mesmo
    message = st.text_area("Digite uma mensagem para enviar para você mesmo:")
    
    if st.button("📤 Enviar Mensagem", type="primary"):
        if message:
            with st.spinner("Enviando..."):
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                data = {
                    "chat_id": YOUR_ID,
                    "text": f"📨 *Mensagem do Painel de Controle:*\n\n{message}",
                    "parse_mode": "Markdown"
                }
                
                try:
                    response = requests.post(url, json=data)
                    if response.status_code == 200:
                        st.success("✅ Mensagem enviada com sucesso!")
                        st.balloons()
                    else:
                        st.error(f"❌ Erro ao enviar: {response.text}")
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
        else:
            st.warning("Digite uma mensagem primeiro!")

with tab2:
    st.subheader("Estatísticas do Bot")
    
    if st.button("📈 Obter Estatísticas"):
        with st.spinner("Buscando dados..."):
            # Pegar informações do bot
            url = f"https://api.telegram.org/bot{TOKEN}/getMe"
            response = requests.get(url)
            
            if response.status_code == 200:
                st.metric("Status do Bot", "🟢 ONLINE", "Conectado")
                bot_data = response.json()["result"]
                
                # Mostrar informações
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Nome do Bot", bot_data.get("first_name", "N/A"))
                with col2:
                    st.metric("Usuário", f"@{bot_data.get('username', 'N/A')}")
                with col3:
                    st.metric("ID do Bot", bot_data.get("id", "N/A"))
                
                st.success(f"Última verificação: {datetime.now().strftime('%H:%M:%S')}")
            else:
                st.error("❌ Não foi possível conectar ao bot")

with tab3:
    st.subheader("Configurações Avançadas")
    
    st.info("""
    ### 🔧 Próximos Passos para Bot Completo:
    
    1. **Servidor 24/7** (AWS já temos)
    2. **Código Python rodando continuamente**
    3. **Integração com APIs de AI**
    
    ### 🚀 Soluções Recomendadas:
    
    **A) PythonAnywhere (Gratuito)**
    - Hospedagem Python gratuita
    - Roda 24/7 (com algumas limitações)
    - Fácil configuração
    
    **B) Seu servidor AWS** (Já configurado!)
    - Já temos o servidor
    - Precisamos apenas rodar o código Python
    
    **C) Render/Heroku** (Alternativas)
    - Hospedagem gratuita para bots
    """)
    
    if st.button("💾 Baixar Código do Bot Python"):
        bot_code = """
import telebot
import time

TOKEN = "8342975161:AAE3FZ_NZBEfM7BSBOGT7HVOmhBUCIbWBI1s"
YOUR_ID = "704297959"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Olá! Sou o CherifeBot! 🤖")

@bot.message_handler(func=lambda m: True)
def echo(message):
    if str(message.from_user.id) == YOUR_ID:
        bot.reply_to(message, f"Você disse: {message.text}")

print("Bot iniciado!")
bot.polling()
        """
        
        st.download_button(
            label="📥 Download bot.py",
            data=bot_code,
            file_name="cherifebot.py",
            mime="text/python"
        )

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <h3>🎯 Seu Bot está Pronto!</h3>
    <p>Abra o Telegram e converse com <a href='https://t.me/CherifeBot' target='_blank'>@CherifeBot</a></p>
    <p><em>Desenvolvido com ❤️ - Seu Assistente AI Pessoal</em></p>
</div>
""", unsafe_allow_html=True)

# CSS personalizado
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
    }
    .stSuccess {
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)
