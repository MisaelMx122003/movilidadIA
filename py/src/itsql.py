import mysql.connector
import threading

class Itsql:
    def __init__(self, database_name="admindb"):
        self.peticiones = 0
        self.host = "localhost"
        self.user = "web"
        self.password = "123456789"
        self.base_datos = database_name
        self._connection_lock = threading.Lock()
        self._connect()

    def _connect(self):
        """Establece la conexión a la base de datos con configuraciones optimizadas"""
        try:
            self.mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.base_datos,
                port=3306,
                auth_plugin='mysql_native_password',
                pool_size=5,  # ✅ Pool de conexiones
                pool_reset_session=True,
                connect_timeout=30,
                buffered=True  # ✅ Mejor rendimiento para consultas
            )
            self.cursor = self.mydb.cursor(dictionary=True)
            print(f"✅ Conectado a BD: {self.base_datos}")
        except Exception as e:
            print(f"❌ Error conectando a {self.base_datos}: {e}")
            raise e

    # ... (el resto de métodos igual)

    def use_database(self, database_name):
        """Cambia la base de datos actual"""
        try:
            # Cerrar cursor anterior
            if hasattr(self, 'cursor'):
                self.cursor.close()

            # Actualizar la base de datos
            self.base_datos = database_name

            # Reconectar con la nueva base de datos
            self._connect()

            print(f"✅ Base de datos cambiada a: {database_name}")
            return True
        except Exception as e:
            print(f"❌ Error al cambiar BD: {e}")
            # Intentar reconectar a la BD anterior
            try:
                self._connect()
            except:
                pass
            return False

    def get_current_database(self):
        """Obtiene la base de datos actualmente en uso"""
        try:
            result = self.fetchone("SELECT DATABASE() as current_db")
            return result['current_db'] if result else self.base_datos
        except Exception as e:
            print(f"Error obteniendo BD actual: {e}")
            return self.base_datos

    def execute(self, sql, params=None):
        try:
            # Cerrar cursor anterior si hay resultados sin leer
            if self.cursor:
                self.cursor.close()
            self.cursor = self.mydb.cursor(dictionary=True)

            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            self.mydb.commit()
            self.peticiones += 1
        except Exception as e:
            print(f"\n❌ ERROR ejecutando SQL:\n{sql}\nparams={params}\n")
            raise e

    def commit(self):
        self.mydb.commit()
        self.peticiones += 1

    def get_peticiones(self):
        return self.peticiones

    def select(self, sql, params=None):
        self.peticiones += 1
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchone(self, sql, params=None):
        # Cerrar cursor anterior si hay resultados sin leer
        if self.cursor:
            self.cursor.close()
        self.cursor = self.mydb.cursor(dictionary=True)

        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self, sql, params=None):
        # Cerrar cursor anterior si hay resultados sin leer
        if self.cursor:
            self.cursor.close()
        self.cursor = self.mydb.cursor(dictionary=True)

        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()