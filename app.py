import streamlit as st
import requests
import json

st.title("🤖 Configurador de Bot AI")

st.write("""
### Passo 1: Configure seu bot no Telegram
1. Abra Telegram no celular
2. Procure **@BotFather**
3. Envie **/newbot**
4. Siga as instruções
5. Cole o token abaixo
""")

# Input para token
token = st.text_input("Token do seu bot:", type="password")

if token:
    st.success("✅ Token recebido!")
    
    st.write("### Passo 2: Teste seu bot")
    user_message = st.text_input("Digite uma mensagem para testar:")
    
    if user_message:
        # Envia mensagem via API do Telegram
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            st.success("✅ Bot conectado com sucesso!")
            st.json(response.json())
        else:
            st.error("❌ Erro ao conectar. Verifique o token.")

st.write("---")
st.write("Feito com ❤️ - Seu assistente AI 24/7")
