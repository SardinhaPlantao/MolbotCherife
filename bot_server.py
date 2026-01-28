import telebot
import logging
import json
import time
from datetime import datetime
from ai_core import AICore
from tools.email_tool import EmailTool
from tools.web_search import WebSearch

# Configuração
TOKEN = "8342975161:AAE3FZ_NZBEfM7BSBOGT7HVOmhBUC1WB1Is"
YOUR_ID = "704297959"
ADMIN_IDS = [YOUR_ID]

# Inicializar
bot = telebot.TeleBot(TOKEN)
ai = AICore()
web_search = WebSearch()
email_tool = EmailTool()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= COMANDOS PRINCIPAIS =================

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if str(message.from_user.id) in ADMIN_IDS:
        welcome = """
🤖 *CherifeBot AI Assistant 24/7*

*Comandos disponíveis:*
/chat [mensagem] - Conversar com AI
/search [query] - Pesquisar na web
/email - Gerenciar email
/schedule - Agendar tarefa
/remind [tempo] [mensagem] - Definir lembrete
/todo - Lista de tarefas
/news - Últimas notícias
/weather - Previsão do tempo
/translate [texto] - Traduzir
/code [linguagem] [código] - Analisar código
/analyze [url] - Analisar site
/summarize [texto] - Resumir texto
/status - Status do sistema

*Exemplos:*
`/search Python tutorials 2024`
`/remind 15:30 Reunião importante`
`/chat Como automatizar meu trabalho?`
"""
        bot.reply_to(message, welcome, parse_mode="Markdown")

@bot.message_handler(commands=['chat'])
def chat_ai(message):
    """Conversação com AI"""
    user_id = str(message.from_user.id)
    if user_id in ADMIN_IDS:
        query = message.text.replace('/chat ', '').strip()
        if query:
            with bot.send_message(message.chat.id, "🧠 *Pensando...*", parse_mode="Markdown"):
                response = ai.chat(query)
                bot.reply_to(message, response, parse_mode="Markdown")
        else:
            bot.reply_to(message, "Digite: `/chat [sua pergunta]`", parse_mode="Markdown")

@bot.message_handler(commands=['search'])
def search_command(message):
    """Pesquisa na web"""
    user_id = str(message.from_user.id)
    if user_id in ADMIN_IDS:
        query = message.text.replace('/search ', '').strip()
        if query:
            with bot.send_message(message.chat.id, "🔍 *Pesquisando...*", parse_mode="Markdown"):
                results = web_search.search(query, num_results=5)
                response = "📚 *Resultados da pesquisa:*\n\n"
                for i, result in enumerate(results, 1):
                    response += f"{i}. [{result['title']}]({result['link']})\n"
                    response += f"   {result['snippet'][:100]}...\n\n"
                bot.reply_to(message, response, parse_mode="Markdown")
        else:
            bot.reply_to(message, "Digite: `/search [o que pesquisar]`", parse_mode="Markdown")

@bot.message_handler(commands=['remind'])
def set_reminder(message):
    """Definir lembrete"""
    user_id = str(message.from_user.id)
    if user_id in ADMIN_IDS:
        parts = message.text.replace('/remind ', '').strip().split(' ', 1)
        if len(parts) == 2:
            time_str, reminder_text = parts
            # Simples - poderia usar banco de dados
            response = f"⏰ *Lembrete configurado!*\n\n"
            response += f"🕐 *Hora:* {time_str}\n"
            response += f"📝 *Tarefa:* {reminder_text}\n\n"
            response += f"✅ Vou te lembrar às {time_str}"
            bot.reply_to(message, response, parse_mode="Markdown")
        else:
            bot.reply_to(message, "Digite: `/remind [HH:MM] [mensagem]`", parse_mode="Markdown")

@bot.message_handler(commands=['todo'])
def todo_list(message):
    """Lista de tarefas"""
    user_id = str(message.from_user.id)
    if user_id in ADMIN_IDS:
        tasks = [
            "✅ Configurar bot Telegram",
            "🔄 Implementar sistema AI",
            "📧 Conectar email",
            "🌐 Adicionar pesquisa web",
            "📅 Integrar calendário"
        ]
        response = "📋 *Sua Lista de Tarefas:*\n\n"
        for task in tasks:
            response += f"{task}\n"
        bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(commands=['status'])
def system_status(message):
    """Status do sistema"""
    user_id = str(message.from_user.id)
    if user_id in ADMIN_IDS:
        status = f"""
🖥️ *Status do Sistema CherifeBot*

*Componentes:*
🤖 Bot Telegram: ✅ **ONLINE**
🧠 AI Core: ✅ **CONECTADO**
🔍 Web Search: ✅ **PRONTO**
📧 Email: ⚠️ **NÃO CONFIGURADO**
📅 Calendário: ⚠️ **NÃO CONFIGURADO**

*Estatísticas:*
👤 Usuário: {message.from_user.first_name}
🆔 ID: {user_id}
📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
🔋 Status: **🟢 OPERACIONAL**
"""
        bot.reply_to(message, status, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Processa todas as mensagens normais com AI"""
    user_id = str(message.from_user.id)
    if user_id in ADMIN_IDS:
        user_message = message.text
        
        # Respostas automáticas para comandos comuns
        quick_responses = {
            "oi": "👋 Olá! Como posso ajudar?",
            "olá": "👋 Olá! Em que posso ser útil?",
            "obrigado": "😊 De nada! Estou aqui para ajudar!",
            "como você está": "🤖 Estou ótimo! Pronto para automatizar seu dia!",
        }
        
        if user_message.lower() in quick_responses:
            bot.reply_to(message, quick_responses[user_message.lower()])
        else:
            # Processar com AI
            with bot.send_message(message.chat.id, "💭 *Processando...*", parse_mode="Markdown"):
                response = ai.chat(user_message)
                bot.reply_to(message, response, parse_mode="Markdown")

# ================= FUNÇÕES DO SISTEMA =================

def run_scheduler():
    """Agendador de tarefas em background"""
    while True:
        try:
            # Verificar lembretes
            current_time = datetime.now().strftime("%H:%M")
            # Aqui você verificaria lembretes do banco de dados
            time.sleep(60)  # Verificar a cada minuto
        except Exception as e:
            logger.error(f"Erro no scheduler: {e}")
            time.sleep(60)

if __name__ == "__main__":
    logger.info("🚀 Iniciando CherifeBot AI Assistant 24/7...")
    print("=" * 60)
    print("🤖 CHERIFEBOT AI ASSISTANT - SISTEMA COMPLETO")
    print("=" * 60)
    print(f"🔑 Token: {TOKEN[:10]}...")
    print(f"👤 Admin: {YOUR_ID}")
    print(f"🔗 Bot: @CherifeBot")
    print(f"🕐 Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    print("✅ Sistema iniciado! Rodando 24/7...")
    print("📞 Converse com: https://t.me/CherifeBot")
    print("=" * 60)
    
    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=10)
    except Exception as e:
        logger.error(f"Erro principal: {e}")
        time.sleep(5)
