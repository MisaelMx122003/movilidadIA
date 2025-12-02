import requests
import os
from src.itbot import Itbot

class Itabout:
    def __init__(self, mensaje, chat_id=None):
        self.mensaje = mensaje
        self.chat_id = chat_id

    def me(self):
        if self.mensaje.strip() == "/about":
            # Crear instancia de Itbot con el chat_id específico
            itbot = Itbot(self.chat_id)

            about_info = """
🤖 **Información del Estudiante**

👤 **Nombre:** Misael Martinez Trejo
🔢 **No. Control:** 21590290
📚 **Materia:** Administración de Base de Datos
🎓 **Carrera:** Ingeniería en Sistemas Computacionales
            """

            photo_path = "/home/misael/py/imagenes/10.jpg"

            if os.path.exists(photo_path):
                self._send_photo(itbot, photo_path, about_info)
            else:
                itbot.send_message("📷 Foto no encontrada\n" + about_info)

    def _send_photo(self, itbot, photo_path, caption=""):
        """Envía una foto a través de la API de Telegram"""
        try:
            with open(photo_path, 'rb') as photo_file:
                files = {'photo': photo_file}
                url = f"https://api.telegram.org/bot{itbot.token}/sendPhoto"
                params = {
                    'chat_id': itbot.chat_id,
                    'caption': caption,
                    'parse_mode': 'Markdown'
                }
                response = requests.post(url, files=files, data=params)

                if response.status_code != 200:
                    itbot.send_message(caption)

        except Exception as e:
            print(f"Error enviando foto: {e}")
            itbot.send_message(caption)