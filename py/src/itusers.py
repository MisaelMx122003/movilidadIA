from src.global_sql import global_sql

class Itusers:
    def __init__(self, mensaje=None):
        self.mensaje = mensaje
        self.itsql = global_sql  # Usar la instancia global

    def get_current_database(self):
        """Obtiene la base de datos actual desde la instancia global"""
        return self.itsql.get_current_database()

    def create(self, username, password):
        try:
            sql = f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';"
            self.itsql.execute(sql)
            self.itsql.commit()
            return f"🎉 *Usuario Creado Exitosamente*\n\n👤 Usuario: `{username}`\n🔐 Contraseña: `{password}`\n🏠 Host: `localhost`"
        except Exception as e:
            return f"❌ *Error al Crear Usuario*\n\n👤 Usuario: `{username}`\n📝 Error: `{e}`"

    def delete(self, username):
        try:
            sql = f"DROP USER IF EXISTS '{username}'@'localhost';"
            self.itsql.execute(sql)
            self.itsql.commit()
            return f"🗑️ *Usuario Eliminado*\n\n👤 Usuario: `{username}`\n✅ Eliminado completamente del sistema"
        except Exception as e:
            return f"❌ *Error al Eliminar Usuario*\n\n👤 Usuario: `{username}`\n📝 Error: `{e}`"

    def allow(self, username):
        try:
            current_db = self.get_current_database()  # Obtener BD actual
            grant_sql = f"""
            GRANT EXECUTE, SELECT, SHOW VIEW, ALTER, ALTER ROUTINE, CREATE, CREATE ROUTINE,
            CREATE TEMPORARY TABLES, CREATE VIEW, DELETE, DROP, EVENT, INDEX, INSERT, REFERENCES,
            TRIGGER, UPDATE, LOCK TABLES ON `{current_db}`.* TO '{username}'@'localhost' WITH GRANT OPTION;
            FLUSH PRIVILEGES;
            """
            for stmt in grant_sql.strip().split(";"):
                if stmt.strip():
                    self.itsql.execute(stmt.strip())
            self.itsql.commit()

            privileges = [
                "✅ EXECUTE", "✅ SELECT", "✅ SHOW VIEW", "✅ ALTER",
                "✅ CREATE", "✅ DELETE", "✅ DROP", "✅ INSERT",
                "✅ UPDATE", "✅ INDEX", "✅ TRIGGER", "✅ REFERENCES",
                "🎯 WITH GRANT OPTION"
            ]

            return f"🔓 *Privilegios Otorgados*\n\n👤 Usuario: `{username}`\n🗄️ Base de datos: `{current_db}`\n\n📋 *Permisos Concedidos:*\n" + "\n".join(privileges)
        except Exception as e:
            return f"❌ *Error al Otorgar Privilegios*\n\n👤 Usuario: `{username}`\n📝 Error: `{e}`"

    def block(self, username):
        try:
            revoke_sql = f"""
            REVOKE ALL PRIVILEGES, GRANT OPTION FROM '{username}'@'localhost';
            FLUSH PRIVILEGES;
            """
            for stmt in revoke_sql.strip().split(";"):
                if stmt.strip():
                    self.itsql.execute(stmt.strip())
            self.itsql.commit()
            return f"🔒 *Privilegios Revocados*\n\n👤 Usuario: `{username}`\n🚫 Todos los permisos han sido removidos\n🔄 Privilegios actualizados en el sistema"
        except Exception as e:
            return f"❌ *Error al Revocar Privilegios*\n\n👤 Usuario: `{username}`\n📝 Error: `{e}`"

    def list(self):
        try:
            sql = "SELECT user, host, authentication_string AS password FROM mysql.user WHERE user NOT IN ('mysql.sys', 'mysql.session', 'mysql.infoschema', 'root');"
            self.itsql.cursor.execute(sql)
            users = self.itsql.cursor.fetchall()

            if not users:
                return "📭 *No Hay Usuarios Registrados*\n\nNo se encontraron usuarios personalizados en la base de datos."

            result = "👥 *Usuarios del Sistema MySQL*\n\n"
            for u in users:
                user = u['user']
                host = u['host']
                has_password = "🔐" if u['password'] else "🔓"
                result += f"{has_password} `{user}`@{host}\n"

            result += f"\n📊 Total: {len(users)} usuario(s)"
            return result
        except Exception as e:
            return f"❌ *Error al Listar Usuarios*\n\n📝 Error: `{e}`"