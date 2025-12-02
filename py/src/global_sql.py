from src.itsql import Itsql
import threading

# ✅ Conexiones thread-safe para mejor rendimiento
_admin_sql_instance = None
_user_sql_instance = None
_connection_lock = threading.Lock()

def get_admin_sql():
    global _admin_sql_instance
    if _admin_sql_instance is None:
        with _connection_lock:
            if _admin_sql_instance is None:
                _admin_sql_instance = Itsql("admindb")
    return _admin_sql_instance

def get_user_sql():
    global _user_sql_instance
    if _user_sql_instance is None:
        with _connection_lock:
            if _user_sql_instance is None:
                _user_sql_instance = Itsql("admindb")
    return _user_sql_instance

# Instancias globales
admin_sql = get_admin_sql()
user_sql = get_user_sql()
global_sql = admin_sql