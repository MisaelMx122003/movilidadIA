import telebot
from src.itbackup import Itbackup
from src.itabout import Itabout
from src.itusers import Itusers
from src.itbot import Itbot
from src.itconfig import Itconfig
from src.itcouch import Itcouch
from src.itdatabase import Itdatabase
from src.ithelp import Ithelp
from src.itlog import Itlog
from src.itmaster import Itmaster
from src.itrestore import Itrestore
from src.itslave import Itslave
from src.itssh import Itssh
from src.ituserbot import Ituserbot
from src.global_sql import admin_sql, user_sql
from src.itsql import Itsql
import os
from src.ituserbot import Ituserbot
from src.itai_movilidad import Itai_movilidad
from src.itdataset import Itdataset

# Usar global_sql en lugar de crear nuevas instancias

# ✅ Instancia global - nombre diferente
userbot = Ituserbot()

# En bot.py, modifica la función verificar_usuario
def verificar_usuario(message):
    telegram_user_id = message.from_user.id
    username = message.from_user.username
    name_real = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()

    # Usar admin_sql para las tablas del bot (siempre en admindb)
    userbot = Ituserbot()  # Esto usará admin_sql internamente
    userbot.registrar(telegram_user_id, username, name_real)

    if userbot.bloqueado(telegram_user_id):
        bot.reply_to(message, "🚫 Lo siento, estás bloqueado para usar este bot.")
        return False

    # Registrar log usando admin_sql
    userbot.log_registrar(
        telegram_user_id=telegram_user_id,
        message_id=message.message_id,
        chat_id=message.chat.id,
        message_type='command' if message.text.startswith('/') else 'text',
        message_text=message.text
    )

    return True

# Agrega esta nueva función para verificar permisos de administrador
def verificar_administrador(message):
    """
    Verifica si el usuario que ejecuta el comando es administrador
    """
    telegram_user_id = message.from_user.id
    return userbot.es_administrador(telegram_user_id)

def escape_md(text: str) -> str:
    """
    Escapa caracteres especiales de MarkdownV2 para mensajes de Telegram.
    """
    if text is None:
        return ""
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    for ch in escape_chars:
        text = text.replace(ch, f"\\{ch}")
    return text

# ✅ AHORA CREAMOS LA INSTANCIA DEL BOT
bot = telebot.TeleBot("8268216056:AAH9qfeyv9CSV0zNt9GYU4xH9I8z7Y2WgYA", parse_mode=None)

# ✅ INSTANCIAS GLOBALES DE IA
ai_sistema = Itai_movilidad()
ai_dataset = Itdataset()

@bot.message_handler(commands=['start'])
def start(message):
    if not verificar_usuario(message):
        return
    from src.ituserbot import Ituserbot
    userbot = Ituserbot()

    telegram_user_id = message.from_user.id
    username = message.from_user.username
    name_real = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
    message_id = message.message_id
    chat_id = message.chat.id
    message_text = message.text

    # Registrar usuario si no existe
    userbot.registrar(telegram_user_id, username, name_real)

    # Registrar log - SIN el parámetro command
    userbot.log_registrar(
        telegram_user_id=telegram_user_id,
        message_id=message_id,
        chat_id=chat_id,
        message_type='command',
        message_text=message_text
    )

    # Verificar si está bloqueado
    if userbot.bloqueado(telegram_user_id):
        bot.reply_to(message, "🚫 Lo siento, estás bloqueado para usar este bot.")
        return

    # Responder al usuario
    bot.reply_to(message, f"👋 Hola {name_real or username}, bienvenido al bot.")

@bot.message_handler(commands=['respaldo', 'backup'])
def cmd_backup(message):
    if not verificar_usuario(message):
        return

    # ✅ CORREGIR: usar message.text en lugar de texto
    texto = message.text

    # ✅ CORREGIR: Itbackup no necesita parámetros
    itbackup = Itbackup()

    if "gzip" in texto:
        tipo = "gzip"
        msg = "🗜️ Creando respaldo comprimido (.gz)..."
    else:
        tipo = "normal"
        msg = "💾 Creando respaldo normal (.sql)..."

    bot.reply_to(message, msg)

    # Ejecutar respaldo según tipo
    archivo = itbackup.execute(tipo)

    # Enviar resultado
    if archivo and os.path.exists(archivo):
        bot.reply_to(message, f"✅ Respaldo completado:\n{archivo}")
        with open(archivo, 'rb') as doc:
            bot.send_document(message.chat.id, doc)
    else:
        bot.reply_to(message, "❌ Error al crear el respaldo.")

# ... (AQUÍ VAN TODOS TUS OTROS HANDLERS EXISTENTES - asegúrate de que estén todos indentados correctamente)

# ✅ AHORA AGREGAMOS LOS NUEVOS HANDLERS DE IA (después de crear el bot)

@bot.message_handler(commands=['ai_train'])
def ai_train(message):
    """Entrena todos los modelos de IA"""
    if not verificar_administrador(message):
        bot.reply_to(message, "❌ Solo administradores pueden entrenar modelos")
        return
    
    bot.reply_to(message, "🧠 Entrenando modelos de IA... Esto puede tardar unos minutos.")
    
    # Crear datasets de ejemplo si no existen
    if not os.path.exists("data/quejas.csv"):
        ai_dataset.crear_todos()
    
    # Entrenar modelos
    resultados = ai_sistema.entrenar_todos()
    
    bot.reply_to(message, "✅ Modelos de IA entrenados correctamente!")

@bot.message_handler(commands=['ai_status'])
def ai_status(message):
    """Muestra estado de los modelos de IA"""
    estado = ai_sistema.obtener_estado()
    
    respuesta = "🤖 **ESTADO DE MODELOS DE IA**\n\n"
    for modulo, status in estado.items():
        respuesta += f"• {modulo.upper()}: {status}\n"
    
    bot.reply_to(message, respuesta)

# MODIFICA el handler echo_all para incluir IA:
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if not verificar_usuario(message):
        return
    
    # Si es un comando, ya fue procesado por otros handlers
    if message.text.startswith('/'):
        bot.reply_to(message, message.text)
        return
    
    # Si no es comando, procesar con IA de movilidad
    resultado = ai_sistema.procesar_mensaje(message.text)
    
    respuesta = f"**[{resultado['modulo'].upper()}]**\n{resultado['respuesta']}"
    bot.reply_to(message, respuesta)

# ✅ FINALMENTE EL POLLING
bot.infinity_polling()
