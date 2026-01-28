import streamlit as st
import requests
import json

st.set_page_config(page_title="Configurador Bot AI", page_icon="🤖")

st.title("🤖 Configurador de Bot AI para Telegram")

st.markdown("""
### ✅ Seu bot foi criado com sucesso!
**Nome:** CherifeBot  
**Usuário:** @CherifeBot  
**Link:** [t.me/CherifeBot](https://t.me/CherifeBot)

---

### 🔑 Seu Token (GUARDE EM SEGURANÇA!)
8342975161:AaE3FZ_NZBEFM7BSBOGT7HVOmhBUCIWBIIS

---

### 📝 Próximos Passos:
""")

# Seção 1: Verificar bot
st.subheader("1. Verificar conexão do bot")
if st.button("Testar conexão com Telegram"):
    token = "8342975161:AaE3FZ_NZBEFM7BSBOGT7HVOmhBUCIWBIIS"
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Bot conectado com sucesso!")
            st.json(data["result"])
        else:
            st.error(f"❌ Erro {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"❌ Erro de conexão: {e}")

# Seção 2: Configurar webhook simples
st.subheader("2. Configurar resposta automática")

user_id = st.text_input("Seu User ID (do @userinfobot):")

if user_id and user_id.isdigit():
    st.success(f"✅ User ID: {user_id}")
    
    message = st.text_area("Mensagem que o bot responderá:")
    
    if st.button("Configurar resposta"):
        st.info("""
        ⚠️ Para um bot completo, você precisa:
        1. Um servidor 24/7 (como o AWS que configuramos)
        2. Código Python rodando continuamente
        3. Webhook configurado
        
        **Solução fácil:** Use [PythonAnywhere](https://www.pythonanywhere.com) gratuito!
        """)

st.markdown("---")
st.markdown("### 🚀 Tutorial completo:")
st.markdown("""
1. **PythonAnywhere** (gratuito):
   - Crie conta em [pythonanywhere.com](https://www.pythonanywhere.com)
   - Crie novo arquivo `bot.py`
   - Cole o código que vou te enviar
   - Configure para rodar 24/7

2. **Ou use Replit** (mais simples):
   - [replit.com](https://replit.com)
   - Novo projeto Python
   - Cole o código do bot

Quer que eu te envie o código completo para rodar o bot?
""")

if st.button("📋 Sim, me envie o código do bot!"):
    st.code("""
import telebot
import os

TOKEN = "8342975161:AaE3FZ_NZBEFM7BSBOGT7HVOmhBUCIWBIIS"
YOUR_ID = "SEU_USER_ID_AQUI"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Sou seu assistente AI. Como posso ajudar?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if str(message.from_user.id) == YOUR_ID:
        bot.reply_to(message, f"Você disse: {message.text}")
    else:
        bot.reply_to(message, "Acesso não autorizado.")

print("Bot iniciado...")
bot.polling()
""", language="python")

st.markdown("---")
st.markdown("Feito com ❤️ - Seu assistente AI 24/7")
