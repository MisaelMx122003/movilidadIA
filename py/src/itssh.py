
import paramiko
import os
import datetime
"""itssh = Itssh()
itssh.connect()
fecha = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
source = "/home/misael/Agente con interfaz.mkv"
target = f"/home/misael/respaldodb/Agente_con_interfaz_{fecha}.mkv"
itssh.upload(source, target)
itssh.close()"""
class Itssh:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostname = "10.10.7.71"
        self.port = 22
        self.username = "misael"
        self.password = "1463"

    def connect(self):
        self.ssh.connect(hostname=self.hostname,port=self.port,username=self.username,password=self.password)
        self.sftp = self.ssh.open_sftp()
    def upload(self, local_file_path, remote_file_path):
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"El archivo {local_file_path} no existe")

        self.sftp.put(local_file_path, remote_file_path)
        print(f"Archivo subido: {local_file_path} → {remote_file_path}")

    def download(self, remote_file_path, local_file_path):
        print("")

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()
        print(" Conexión cerrada")





