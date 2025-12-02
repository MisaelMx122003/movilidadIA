from src.itbot import Itbot

class Ithelp:
    def __init__(self, mensaje):
        self.mensaje = mensaje

    def help(self):
        if self.mensaje.strip() == "/help":
            itbot = Itbot()

            help_text = """
🤖 **BOT DE ADMINISTRACIÓN - COMANDOS DISPONIBLES**

🔹 **BÁSICOS**
`/start` - Iniciar bot
`/help` - Esta ayuda
`/about` - Mi información

💾 **RESPALDOS**
`/backup` - Respaldo normal
`/backup gzip` - Respaldo comprimido
`/restore list` - Listar respaldos
`/restore database <bd> <archivo>` - Restaurar

👥 **USUARIOS MYSQL**
`/user create <user> <pass>` - Crear usuario
`/user delete <user>` - Eliminar
`/user grant <user>` - Dar permisos
`/user revoke <user>` - Quitar permisos
`/user list` - Listar usuarios

🔧 **ADMIN BOT**
`/list_userbot` - Ver usuarios del bot
`/block_user <id>` - Bloquear usuario
`/unblock_user <id>` - Desbloquear

🗄️ **BASE DE DATOS**
`/select <sql>` - Consultas SELECT
`/insert <sql>` - Insertar datos
`/sql <consulta>` - SQL general
`/database use <bd>` - Cambiar BD

🛠️ **OTROS**
`/cmd <comando>` - Comandos sistema
`/couch` - CouchDB
`/log` - Registros
`/config` - Configuración

📝 **Ejemplos:**
`/user create maria 123456`
`/backup gzip`
`/select * FROM tabla`
            """

            itbot.send_message(help_text)
        else:
            itbot = Itbot()
            itbot.send_message(self.mensaje)