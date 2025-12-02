from src.global_sql import admin_sql


class Ituserbot:
    def __init__(self):
        """Inicializa la conexión SQL usando la instancia global"""
        self.db = admin_sql

    def es_administrador(self, telegram_user_id):
        """
        Verifica si el usuario es administrador.
        Define aquí tu ID de Telegram como administrador.
        """
        administradores = [7316511307]
        return telegram_user_id in administradores

    def registrar(self, telegram_user_id, username, name_real):
        print(f"📥 Registrando usuario {telegram_user_id} ({username})...")

        try:
            # Buscar usuario existente
            query_check = "SELECT * FROM telegram_users WHERE telegram_user_id = %s"
            result = self.db.fetchone(query_check, (telegram_user_id,))
            print(f"Resultado SELECT: {result}")

            if result is None:
                print("🆕 Nuevo usuario, insertando registro.")
                query_insert = """
                    INSERT INTO telegram_users (telegram_user_id, username, name_real, is_allowed, last_interaction_at, created_at)
                    VALUES (%s, %s, %s, 1, NOW(), NOW())
                """
                self.db.execute(query_insert, (telegram_user_id, username, name_real))
            else:
                print("🟡 Ya existe, actualizando interacción.")
                query_update = """
                    UPDATE telegram_users
                    SET last_interaction_at = NOW()
                    WHERE telegram_user_id = %s
                """
                self.db.execute(query_update, (telegram_user_id,))

        except Exception as e:
            print(f"❌ Error en registrar: {e}")
            raise e

    def existe(self, telegram_user_id):
        """Verifica si el usuario existe."""
        try:
            query = "SELECT id FROM telegram_users WHERE telegram_user_id = %s"
            result = self.db.fetchone(query, (telegram_user_id,))
            return bool(result)
        except Exception as e:
            print(f"❌ Error en existe: {e}")
            return False

    def bloqueado(self, telegram_user_id):
        """Verifica si el usuario está bloqueado."""
        try:
            query = "SELECT is_allowed FROM telegram_users WHERE telegram_user_id = %s"
            result = self.db.fetchone(query, (telegram_user_id,))

            if not result:
                return False  # si no existe, lo dejamos pasar por ahora

            return (result["is_allowed"] == 0)
        except Exception as e:
            print(f"❌ Error en bloqueado: {e}")
            return False

    def block(self, telegram_user_id):
        """Bloquea a un usuario (is_allowed = 0)"""
        try:
            query = "UPDATE telegram_users SET is_allowed = 0 WHERE telegram_user_id = %s"
            self.db.execute(query, (telegram_user_id,))
            return True
        except Exception as e:
            print(f"❌ Error en block: {e}")
            return False

    def allow(self, telegram_user_id):
        """Permite nuevamente a un usuario (is_allowed = 1)"""
        try:
            query = "UPDATE telegram_users SET is_allowed = 1 WHERE telegram_user_id = %s"
            self.db.execute(query, (telegram_user_id,))
            return True
        except Exception as e:
            print(f"❌ Error en allow: {e}")
            return False

    def listar(self):
        """Devuelve una lista con todos los usuarios y su estado."""
        try:
            query = """
                SELECT telegram_user_id, 
                       username, 
                       name_real,
                       CASE WHEN is_allowed = 1 THEN '✅ Permitido' ELSE '⛔ Bloqueado' END AS estado,
                       DATE_FORMAT(last_interaction_at, '%Y-%m-%d %H:%i:%s') AS ultima_interaccion
                FROM telegram_users
                ORDER BY created_at DESC
            """
            return self.db.fetchall(query)
        except Exception as e:
            print(f"❌ Error en listar: {e}")
            return []

    def log_registrar(self, telegram_user_id, message_id, chat_id, message_type, message_text):
        """Registra un log de actividad."""
        try:
            query = """
                INSERT INTO telegram_logs (telegram_user_id, message_id, chat_id, message_type, message_text, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            params = (telegram_user_id, message_id, chat_id, message_type, message_text)
            self.db.execute(query, params)
            print(f"🧾 Log registrado: {telegram_user_id} -> {message_text[:40]}...")
        except Exception as e:
            print(f"❌ Error en log_registrar: {e}")

    def log_listar(self, telegram_user_id=None, limite=50):
        """Devuelve los últimos logs registrados (por usuario o globales)."""
        try:
            if telegram_user_id:
                query = """
                    SELECT id, telegram_user_id, message_type, message_text, created_at
                    FROM telegram_logs
                    WHERE telegram_user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                """
                return self.db.fetchall(query, (telegram_user_id, limite))
            else:
                query = """
                    SELECT id, telegram_user_id, message_type, message_text, created_at
                    FROM telegram_logs
                    ORDER BY created_at DESC
                    LIMIT %s
                """
                return self.db.fetchall(query, (limite,))
        except Exception as e:
            print(f"❌ Error en log_listar: {e}")
            return []