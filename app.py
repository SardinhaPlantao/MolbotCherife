import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="CherifeBot AI - Painel de Controle",
    page_icon="🤖",
    layout="wide"
)

# Configuração
TOKEN = "8342975161:AAE3FZ_NZBEfM7BSBOGT7HVOmhBUC1WB1Is"
YOUR_ID = "704297959"

st.title("🤖 CherifeBot AI - Painel de Controle")
st.markdown("---")

# 1. TESTE DE CONEXÃO
st.header("🔗 Teste de Conexão")

if st.button("Testar Conexão com Bot Telegram"):
    with st.spinner("Conectando..."):
        url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                st.success("✅ **BOT CONECTADO!**")
                bot_data = response.json()["result"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Nome", bot_data.get("first_name"))
                with col2:
                    st.metric("Usuário", f"@{bot_data.get('username')}")
                with col3:
                    st.metric("Status", "🟢 Online")
                    
            else:
                st.error(f"❌ Erro: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Erro: {e}")

st.markdown("---")

# 2. ENVIAR MENSAGENS
st.header("📨 Enviar Mensagem")

message = st.text_area("Digite sua mensagem:")
if st.button("Enviar para Telegram", type="primary"):
    if message:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": YOUR_ID,
            "text": f"📨 *Mensagem do Painel:*\n\n{message}\n\n_Enviado: {datetime.now().strftime('%H:%M:%S')}_",
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                st.success("✅ Mensagem enviada!")
                st.balloons()
            else:
                st.error(f"❌ Erro: {response.text}")
        except Exception as e:
            st.error(f"❌ Erro: {e}")
    else:
        st.warning("Digite uma mensagem!")

st.markdown("---")

# 3. STATUS DO SISTEMA
st.header("📊 Status do Sistema")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Painel Web", "🟢 Online", "Streamlit")
with col2:
    st.metric("Bot Telegram", "🟢 Online", "@CherifeBot")
with col3:
    st.metric("Servidor AWS", "⚙️ Configurar", "Próximo passo")

st.markdown("---")

# 4. PRÓXIMOS PASSOS
st.header("🚀 Próximos Passos")

st.info("""
**Para completar o sistema MoltBot:**

1. ✅ **Painel Web (Streamlit)** - Este aqui!
2. ⚙️ **Bot 24/7 (AWS)** - Precisamos configurar
3. 🤖 **AI Integration** - Adicionar depois

**Instruções AWS:**
1. Acesse seu servidor AWS
2. Execute os comandos que vou fornecer
3. O bot ficará online 24/7
""")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🤖 <strong>CherifeBot AI Assistant</strong> | 🎯 <a href='https://t.me/CherifeBot' target='_blank'>@CherifeBot</a></p>
    <p><em>Sistema em construção - Versão 1.0</em></p>
</div>
""", unsafe_allow_html=True)
