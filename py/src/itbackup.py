import subprocess
import datetime
import os
from src.global_sql import user_sql

class Itbackup:
    def __init__(self):
        self.user = "web"
        self.password = "123456789"
        self.ruta_respaldo = "/home/misael/py/respaldos"
        self.itsql = user_sql  # Usar la conexión del usuario

    # El resto del código igual...

    def get_current_database(self):
        """Obtiene la base de datos actualmente seleccionada desde Itsql"""
        return self.itsql.get_current_database()

    def execute(self, tipo="normal"):
        """
        Ejecuta el respaldo según el tipo:
        - normal : respaldo SQL sin comprimir
        - gzip   : respaldo SQL comprimido
        - all    : respaldo completo de todas las BD
        """
        # Obtener la base de datos actual desde Itsql
        current_db = self.get_current_database()
        print(f"📦 Creando respaldo de la base de datos: {current_db}")

        if tipo == "gzip":
            return self._backup_gzip(current_db)
        elif tipo == "all":
            return self._backup_all()
        else:
            return self._backup_normal(current_db)

    def _backup_normal(self, database_name):
        print(f"🧩 Ejecutando respaldo normal de '{database_name}' (.sql)...")
        fecha = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        archivo_sql = f"{self.ruta_respaldo}/{database_name}_{fecha}.sql"

        comando = (
            f"mysqldump --add-drop-table -u {self.user} -p{self.password} "
            f"{database_name} > {archivo_sql}"
        )
        print(comando)
        try:
            subprocess.run(comando, shell=True, check=True)
            print(f"✅ Respaldo creado: {archivo_sql}")
            return archivo_sql
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al crear respaldo: {e}")
            return None

    def _backup_gzip(self, database_name):
        print(f"🗜️ Ejecutando respaldo comprimido de '{database_name}' (.gz)...")
        fecha = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        archivo_gz = f"{self.ruta_respaldo}/{database_name}_{fecha}.sql.gz"

        comando = (
            f"mysqldump --add-drop-table -u {self.user} -p{self.password} "
            f"{database_name} | gzip > {archivo_gz}"
        )
        print(comando)
        try:
            subprocess.run(comando, shell=True, check=True)
            print(f"✅ Respaldo comprimido creado: {archivo_gz}")
            return archivo_gz
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al crear respaldo comprimido: {e}")
            return None

    def _backup_all(self):
        """Respaldo de todas las bases de datos"""
        print("🗃️ Ejecutando respaldo de TODAS las bases de datos...")
        fecha = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        archivo_sql = f"{self.ruta_respaldo}/ALL_DATABASES_{fecha}.sql"

        comando = (
            f"mysqldump --add-drop-table -u {self.user} -p{self.password} "
            f"--all-databases > {archivo_sql}"
        )
        print(comando)
        try:
            subprocess.run(comando, shell=True, check=True)
            print(f"✅ Respaldo completo creado: {archivo_sql}")
            return archivo_sql
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al crear respaldo completo: {e}")
            return None