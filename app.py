import streamlit as st
import requests
import json
import time
from datetime import datetime
import pytz

st.set_page_config(
    page_title="CherifeBot - Seu Assistente AI",
    page_icon="🤖",
    layout="wide"
)

# ================= CONFIGURAÇÃO =================
# CORREÇÃO: Token com 'F' maiúsculo (erro anterior: NZBEfM7BSBOG)
TOKEN = "8342975161:AAE3FZ_NZBEFM7BSBOGT7HVOmhBUCIbWBI1s"
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
    if st.button("🔗 Testar Conexão com Telegram", use_container_width=True, key="test_connection"):
        with st.spinner("Conectando..."):
            url = f"https://api.telegram.org/bot{TOKEN}/getMe"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ **CONECTADO COM SUCESSO!**")
                    
                    # Mostrar informações do bot
                    bot_info = data["result"]
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Nome do Bot", bot_info.get('first_name', 'N/A'))
                        st.metric("ID do Bot", bot_info.get('id', 'N/A'))
                    
                    with col_b:
                        st.metric("Usuário", f"@{bot_info.get('username', 'N/A')}")
                        st.metric("Status", "🟢 ONLINE")
                    
                    st.info(f"""
                    **Informações do Bot:**
                    - **Nome:** {bot_info.get('first_name', 'N/A')}
                    - **Usuário:** @{bot_info.get('username', 'N/A')}
                    - **ID:** {bot_info.get('id', 'N/A')}
                    - **Link:** [t.me/{bot_info.get('username', '')}](https://t.me/{bot_info.get('username', '')})
                    - **É Bot:** {bot_info.get('is_bot', 'N/A')}
                    """)
                    
                    # Teste adicional - verificar se pode enviar mensagem
                    st.subheader("🚀 Teste de Envio")
                    test_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    test_data = {
                        "chat_id": YOUR_ID,
                        "text": "✅ *Teste de conexão bem-sucedido!*\n\nSeu painel de controle está funcionando perfeitamente!",
                        "parse_mode": "Markdown"
                    }
                    
                    test_response = requests.post(test_url, json=test_data)
                    if test_response.status_code == 200:
                        st.success("✅ Teste de envio: **OK**")
                    else:
                        st.warning(f"⚠️ Teste de envio falhou: {test_response.text}")
                        
                else:
                    st.error(f"❌ Erro {response.status_code}: {response.text}")
                    st.info("""
                    **Possíveis soluções:**
                    1. Token pode estar expirado - gere novo no @BotFather
                    2. Token digitado incorretamente
                    3. Problema de rede temporário
                    """)
            except Exception as e:
                st.error(f"❌ Erro de conexão: {e}")
                st.info("Verifique sua conexão com a internet")

with col2:
    st.header("👤 Suas Credenciais")
    
    # Credenciais em formato mais seguro
    with st.expander("🔐 Ver Credenciais", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Token", value=TOKEN, type="password", disabled=True, key="token_display")
            st.text_input("Bot Username", value=BOT_USERNAME, disabled=True)
        with col_b:
            st.text_input("User ID", value=YOUR_ID, disabled=True)
            st.text_input("Status", value="🟢 Ativo", disabled=True)
    
    st.warning("""
    ⚠️ **Mantenha essas informações em segurança!**
    - O token permite controlar seu bot completamente
    - O User ID garante que só você use o bot
    - Não compartilhe essas informações
    """)
    
    # Botões de ação rápida
    st.subheader("⚡ Ações Rápidas")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Atualizar Token", use_container_width=True):
            st.info("Vá no Telegram -> @BotFather -> /mybots -> Selecione seu bot -> API Token -> Revoke & Generate New")
    with col_b:
        if st.button("📱 Abrir Telegram", use_container_width=True):
            st.markdown(f'<a href="https://t.me/{BOT_USERNAME[1:]}" target="_blank"><button style="width:100%">Abrir @CherifeBot</button></a>', unsafe_allow_html=True)

st.markdown("---")

# Seção de controle do bot
st.header("🎮 Controle do Bot")

tab1, tab2, tab3, tab4 = st.tabs(["📨 Enviar Mensagem", "📊 Estatísticas", "⚙️ Configurações", "🐛 Debug"])

with tab1:
    st.subheader("Enviar mensagem através do bot")
    
    # Opções de formatação
    col_format, col_type = st.columns(2)
    with col_format:
        parse_mode = st.selectbox("Formato da mensagem", ["Markdown", "HTML", "Texto simples"])
    with col_type:
        message_type = st.selectbox("Tipo de mensagem", ["Texto", "Aviso", "Urgente", "Informação"])
    
    # Ícone baseado no tipo
    icons = {
        "Texto": "📝",
        "Aviso": "⚠️",
        "Urgente": "🚨",
        "Informação": "ℹ️"
    }
    
    # Para enviar mensagem para você mesmo
    message = st.text_area(
        f"Digite sua mensagem:",
        height=150,
        placeholder=f"Digite aqui a mensagem que deseja enviar para você mesmo através do {BOT_USERNAME}..."
    )
    
    col_send, col_clear = st.columns([3, 1])
    with col_send:
        if st.button(f"{icons[message_type]} Enviar Mensagem", type="primary", use_container_width=True):
            if message:
                with st.spinner("Enviando..."):
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    
                    # Formatar mensagem baseada no tipo
                    if message_type == "Aviso":
                        formatted_message = f"⚠️ *AVISO*\n\n{message}"
                    elif message_type == "Urgente":
                        formatted_message = f"🚨 *URGENTE*\n\n{message}"
                    elif message_type == "Informação":
                        formatted_message = f"ℹ️ *INFORMAÇÃO*\n\n{message}"
                    else:
                        formatted_message = message
                    
                    # Adicionar timestamp
                    tz = pytz.timezone('America/Sao_Paulo')
                    timestamp = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
                    formatted_message += f"\n\n_Enviado: {timestamp}_"
                    
                    data = {
                        "chat_id": YOUR_ID,
                        "text": formatted_message,
                        "parse_mode": "Markdown" if parse_mode == "Markdown" else "HTML" if parse_mode == "HTML" else None
                    }
                    
                    try:
                        response = requests.post(url, json=data, timeout=10)
                        if response.status_code == 200:
                            st.success("✅ Mensagem enviada com sucesso!")
                            st.balloons()
                            
                            # Mostrar preview
                            with st.expander("📋 Ver mensagem enviada"):
                                st.markdown("**Pré-visualização:**")
                                st.info(formatted_message)
                                st.json(response.json())
                        else:
                            error_msg = response.json().get('description', response.text)
                            st.error(f"❌ Erro ao enviar: {error_msg}")
                            
                            # Sugestões de correção
                            if "Unauthorized" in error_msg:
                                st.info("""
                                **Token inválido! Soluções:**
                                1. Verifique se o token está correto
                                2. Gere novo token no @BotFather
                                3. Confirme se há espaços extras no token
                                """)
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
            else:
                st.warning("Digite uma mensagem primeiro!")
    
    with col_clear:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.rerun()

with tab2:
    st.subheader("Estatísticas do Bot")
    
    if st.button("📈 Obter Estatísticas Detalhadas", use_container_width=True):
        with st.spinner("Buscando dados..."):
            # Pegar informações do bot
            url = f"https://api.telegram.org/bot{TOKEN}/getMe"
            response = requests.get(url)
            
            if response.status_code == 200:
                st.metric("Status do Bot", "🟢 ONLINE", delta="Conectado", delta_color="normal")
                bot_data = response.json()["result"]
                
                # Mostrar informações em métricas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Nome", bot_data.get("first_name", "N/A"))
                with col2:
                    st.metric("Usuário", f"@{bot_data.get('username', 'N/A')}")
                with col3:
                    st.metric("ID", bot_data.get("id", "N/A"))
                with col4:
                    st.metric("Tipo", "🤖 Bot" if bot_data.get("is_bot") else "👤 Usuário")
                
                # Informações adicionais
                st.subheader("📋 Detalhes Técnicos")
                st.json(bot_data)
                
                # Timestamp
                tz = pytz.timezone('America/Sao_Paulo')
                last_check = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
                st.success(f"✅ Última verificação: {last_check} (BRT)")
            else:
                st.error("❌ Não foi possível conectar ao bot")
                st.info("Verifique o token e tente novamente")

with tab3:
    st.subheader("Configurações Avançadas")
    
    # Configurações em abas
    config_tab1, config_tab2, config_tab3 = st.tabs(["🛠️ Configurações", "🚀 Hospedagem", "📦 Download"])
    
    with config_tab1:
        st.info("""
        ### 🔧 Configurações do Bot
        
        1. **Token do Bot** - Mantenha sempre seguro
        2. **User ID** - Apenas seu ID pode usar o bot
        3. **Parse Mode** - Markdown ou HTML para formatação
        4. **Timezone** - Ajustado para Brasil (BRT)
        """)
        
        # Editor de configuração (simulado)
        config_json = {
            "bot_token": TOKEN[:10] + "..." + TOKEN[-5:],
            "user_id": YOUR_ID,
            "bot_username": BOT_USERNAME,
            "timezone": "America/Sao_Paulo",
            "parse_mode": "Markdown",
            "security": {
                "only_owner": True,
                "webhook_enabled": False,
                "rate_limit": "60/hour"
            }
        }
        
        st.json(config_json)
    
    with config_tab2:
        st.info("""
        ### 🌐 Hospedagem 24/7
        
        **Opções Recomendadas:**
        
        **A) PythonAnywhere (Gratuito)**
        - Hospedagem Python gratuita
        - Roda 24/7 (com algumas limitações)
        - Fácil configuração
        
        **B) Seu servidor AWS** (Já configurado!)
        - Já temos o servidor
        - Precisamos apenas rodar o código Python
        
        **C) Render/Heroku** (Alternativas)
        - Hospedagem gratuita para bots
        
        **D) Railway.app** (Recomendado)
        - Fácil deploy com GitHub
        - Generoso free tier
        """)
        
        # Comando para deploy
        st.code("""
        # Para rodar no seu servidor:
        pip install python-telegram-bot
        python cherifebot.py
        """, language="bash")
    
    with config_tab3:
        st.subheader("💾 Download Códigos")
        
        # Bot Python completo
        bot_code = '''import telebot
import time
import logging
from datetime import datetime

# ================= CONFIGURAÇÃO =================
TOKEN = "8342975161:AAE3FZ_NZBEFM7BSBOGT7HVOmhBUCIbWBI1s"
YOUR_ID = "704297959"
# ================================================

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Responde ao comando /start"""
    user_id = str(message.from_user.id)
    if user_id == YOUR_ID:
        welcome_text = """
🤖 *Olá! Sou o CherifeBot!*

*Comandos disponíveis:*
/start - Mostra esta mensagem
/status - Verifica status do bot
/time - Mostra data e hora atual

*Desenvolvido com ❤️ para você!*
        """
        bot.reply_to(message, welcome_text, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ *Acesso não autorizado.*", parse_mode="Markdown")

@bot.message_handler(commands=['status'])
def send_status(message):
    """Responde ao comando /status"""
    user_id = str(message.from_user.id)
    if user_id == YOUR_ID:
        status_text = f"""
✅ *Status do CherifeBot*

*Informações:*
• Usuário: @{message.from_user.username or 'N/A'}
• ID: {user_id}
• Data: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
• Bot: Online 🟢

*Tudo funcionando perfeitamente!*
        """
        bot.reply_to(message, status_text, parse_mode="Markdown")

@bot.message_handler(commands=['time'])
def send_time(message):
    """Responde ao comando /time"""
    user_id = str(message.from_user.id)
    if user_id == YOUR_ID:
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        bot.reply_to(message, f"🕐 *Data e Hora:* {current_time}", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Responde a todas as outras mensagens"""
    user_id = str(message.from_user.id)
    if user_id == YOUR_ID:
        # Echo com timestamp
        current_time = datetime.now().strftime("%H:%M:%S")
        response = f"📨 *Mensagem recebida* ({current_time}):\n\n{message.text}"
        bot.reply_to(message, response, parse_mode="Markdown")
        logger.info(f"Mensagem recebida de {user_id}: {message.text[:50]}...")
    else:
        bot.reply_to(message, "🚫 *Bot privado* - Apenas o proprietário pode usar.", parse_mode="Markdown")
        logger.warning(f"Tentativa de acesso não autorizado: {user_id}")

if __name__ == "__main__":
    logger.info("🤖 Iniciando CherifeBot...")
    print("=" * 50)
    print("🤖 CHERIFEBOT - ASSISTENTE AI 24/7")
    print("=" * 50)
    print(f"👤 Proprietário: {YOUR_ID}")
    print(f"🔗 Bot: @CherifeBot")
    print(f"🕐 Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 50)
    print("✅ Bot está rodando! Pressione Ctrl+C para parar")
    
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logger.error(f"Erro no bot: {e}")
        print(f"❌ Erro: {e}")
        time.sleep(5)'''

        st.download_button(
            label="📥 Download bot.py (Completo)",
            data=bot_code,
            file_name="cherifebot_completo.py",
            mime="text/python",
            use_container_width=True
        )
        
        # Requirements.txt
        req_code = '''python-telegram-bot==20.7
requests==2.31.0
python-dotenv==1.0.0
pytz==2023.3
'''
        
        st.download_button(
            label="📦 Download requirements.txt",
            data=req_code,
            file_name="requirements.txt",
            mime="text/plain",
            use_container_width=True
        )

with tab4:
    st.subheader("🐛 Debug & Logs")
    
    # Teste de API
    if st.button("🔍 Testar APIs", use_container_width=True):
        with st.spinner("Testando todas as APIs..."):
            tests = [
                ("getMe", f"https://api.telegram.org/bot{TOKEN}/getMe"),
                ("sendMessage", f"https://api.telegram.org/bot{TOKEN}/sendMessage"),
            ]
            
            results = []
            for test_name, test_url in tests:
                try:
                    if test_name == "sendMessage":
                        data = {"chat_id": YOUR_ID, "text": "🔧 Teste de debug"}
                        response = requests.post(test_url, json=data)
                    else:
                        response = requests.get(test_url)
                    
                    results.append({
                        "API": test_name,
                        "Status": response.status_code,
                        "Sucesso": response.status_code == 200,
                        "Resposta": response.json() if response.status_code == 200 else response.text
                    })
                except Exception as e:
                    results.append({
                        "API": test_name,
                        "Status": "ERRO",
                        "Sucesso": False,
                        "Resposta": str(e)
                    })
            
            # Mostrar resultados
            for result in results:
                col1, col2, col3 = st.columns([2, 1, 3])
                with col1:
                    st.text(result["API"])
                with col2:
                    if result["Sucesso"]:
                        st.success("✅")
                    else:
                        st.error("❌")
                with col3:
                    st.text(f"Status: {result['Status']}")
    
    # Logs simulados
    st.subheader("📋 Logs Recentes")
    tz = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.now(tz).strftime('%H:%M:%S')
    
    logs = [
        {"time": current_time, "level": "INFO", "message": "Aplicação Streamlit iniciada"},
        {"time": current_time, "level": "INFO", "message": f"Token configurado: {TOKEN[:10]}..."},
        {"time": current_time, "level": "INFO", "message": f"User ID: {YOUR_ID}"},
        {"time": current_time, "level": "SUCCESS", "message": "Painel de controle carregado"},
    ]
    
    for log in logs:
        if log["level"] == "INFO":
            st.info(f"{log['time']} - {log['message']}")
        elif log["level"] == "SUCCESS":
            st.success(f"{log['time']} - {log['message']}")
        else:
            st.warning(f"{log['time']} - {log['message']}")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <h3 style='color: #4CAF50;'>🎯 Seu Bot está Pronto para Uso!</h3>
    <p>Abra o Telegram e converse com <a href='https://t.me/CherifeBot' target='_blank' style='font-weight: bold;'>@CherifeBot</a></p>
    <p><em>🤖 Desenvolvido com ❤️ - Seu Assistente AI Pessoal 24/7</em></p>
    <p style='font-size: 0.8em; color: #666;'>Última atualização: {}</p>
</div>
""".format(datetime.now().strftime('%d/%m/%Y %H:%M:%S')), unsafe_allow_html=True)

# CSS personalizado
st.markdown("""
<style>
    /* Botões principais */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Sucesso */
    .stSuccess {
        border-radius: 10px;
        padding: 1rem;
        border-left: 5px solid #4CAF50;
    }
    
    /* Erro */
    .stError {
        border-radius: 10px;
        padding: 1rem;
        border-left: 5px solid #f44336;
    }
    
    /* Info */
    .stInfo {
        border-radius: 10px;
        padding: 1rem;
        border-left: 5px solid #2196F3;
    }
    
    /* Warning */
    .stWarning {
        border-radius: 10px;
        padding: 1rem;
        border-left: 5px solid #ff9800;
    }
    
    /* Métricas */
    [data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 10px 10px 0px 0px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: bold;
        background-color: #f8f9fa;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript para melhorias
st.markdown("""
<script>
// Adicionar animações suaves
document.addEventListener('DOMContentLoaded', function() {
    // Animar métricas
    const metrics = document.querySelectorAll('[data-testid="stMetric"]');
    metrics.forEach((metric, index) => {
        metric.style.opacity = '0';
        metric.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            metric.style.transition = 'all 0.5s ease';
            metric.style.opacity = '1';
            metric.style.transform = 'translateY(0)';
        }, index * 100);
    });
});
</script>
""", unsafe_allow_html=True)
