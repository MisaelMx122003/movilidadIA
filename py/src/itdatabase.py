from src.itbot import Itbot


class Itdatabase:
    def __init__(self, mensaje="", sql_connection=None):
        self.mensaje = mensaje
        self.itsql = sql_connection  # Recibe la conexión como parámetro

    def get_current_database(self):
        """Obtiene la base de datos actual"""
        return self.itsql.get_current_database()

    def use(self):
        """Cambia la base de datos actual"""
        if self.mensaje.startswith('/database use'):
            try:
                parts = self.mensaje.split()
                if len(parts) >= 3:
                    db_name = parts[2]

                    # Verificar si la BD existe (usar conexión temporal)
                    check_db = self.itsql.fetchone(f"SHOW DATABASES LIKE '{db_name}'")
                    if not check_db:
                        return f"❌ La base de datos `{db_name}` no existe"

                    # Cambiar a la BD
                    success = self.itsql.use_database(db_name)

                    if success:
                        current_db = self.get_current_database()
                        return f"✅ Base de datos cambiada a: `{current_db}`"
                    else:
                        return f"❌ Error al cambiar a la base de datos `{db_name}`"

                else:
                    return "❌ Uso: /database use <nombre_base_datos>"
            except Exception as e:
                return f"❌ Error al cambiar BD: {str(e)}"
        else:
            current_db = self.get_current_database()
            return f"ℹ️ **Base de datos actual:** `{current_db}`\n\n📝 **Comando disponible:**\n`/database use <nombre_bd>` - Cambiar BD actual"

    def current(self):
        """Muestra la base de datos actual"""
        current_db = self.get_current_database()
        return f"🗃️ **Base de datos actual:** `{current_db}`"