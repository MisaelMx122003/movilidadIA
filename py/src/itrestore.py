
from src.itbot import Itbot
import subprocess
import os
from src.global_sql import global_sql

class Itrestore:
    def __init__(self, mensaje=""):
        self.mensaje = mensaje
        self.itbot = Itbot()
        self.itsql = global_sql  # Usar la instancia global

    # El resto del código igual...

    def execute(self):
        """Ejecuta el comando de restauración según el mensaje recibido."""
        try:
            if self.mensaje.startswith('/restore list'):
                return self._list_backups()
            elif self.mensaje.startswith('/restore database'):
                return self._restore_database()
            elif self.mensaje == '/restore':
                return self._show_help()
            else:
                return "❌ Comando no reconocido. Use /restore para ayuda."
        except Exception as e:
            return f"❌ Error en restore: {str(e)}"

    def select(self):
        return self.execute()


    def _list_backups(self):
        backup_dir = "/home/misael/py/respaldos"

        if not os.path.exists(backup_dir):
            return "❌ Directorio de respaldos no encontrado"

        backups = []
        for file in os.listdir(backup_dir):
            if file.endswith(('.sql', '.sql.gz')):
                file_path = os.path.join(backup_dir, file)
                size = os.path.getsize(file_path)
                backups.append(f"📁 {file} ({self._format_size(size)})")

        if not backups:
            return "📭 No se encontraron archivos de respaldo"
        else:
            message = "📋 **Respaldos disponibles:**\n\n" + "\n".join(backups)
            return message


    def _restore_database(self):
        parts = self.mensaje.split()
        if len(parts) < 4:
            return "❌ Uso: /restore database <nombre_db> <archivo_respaldo>\nEjemplo: /restore database admindb admindb_2025_11_04_165554.sql.gz"

        db_name = parts[2]
        backup_file = parts[3]
        backup_path = f"/home/misael/py/respaldos/{backup_file}"

        if not os.path.exists(backup_path):
            return f"❌ Archivo de respaldo no encontrado: {backup_file}"

        try:
            # Detectar si es comprimido o no
            if backup_file.endswith('.gz'):
                cmd = f"gunzip -c '{backup_path}' | mysql -u web -p123456789 {db_name}"
            elif backup_file.endswith('.sql'):
                cmd = f"mysql -u web -p123456789 {db_name} < '{backup_path}'"
            else:
                return "❌ Formato no soportado. Solo se aceptan .sql o .sql.gz"

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)

            if result.returncode == 0:
                return f"✅ Base de datos '{db_name}' restaurada exitosamente desde {backup_file}"
            else:
                error_msg = result.stderr.strip() or "Error desconocido durante la restauración"
                return f"❌ Error en restauración:\n{error_msg}"

        except subprocess.TimeoutExpired:
            return "❌ Timeout: La restauración tardó demasiado tiempo"
        except Exception as e:
            return f"❌ Error ejecutando restauración: {str(e)}"

    # En itrestore.py, modifica el método _show_help:
    def _show_help(self):
        # Obtener la base de datos actual
        from src.itsql import Itsql
        itsql = Itsql()
        current_db = itsql.get_current_database()

        help_text = f"""
    🔧 **Comandos de Restauración y Respaldo:**

    📋 Listar respaldos:
    `/restore list`

    🔄 Restaurar base de datos:
    `/restore database <nombre_db> <archivo>`

    📝 **Base de datos actual:** `{current_db}`

    🎯 Ejemplos:
    `/restore list`
    `/restore database {current_db} {current_db}_2025_11_04_165554.sql`
    `/restore database {current_db} {current_db}_2025_11_04_165554.sql.gz`
        """
        return help_text
