import requests

class Itbot:
    def __init__(self, chat_id=None):
        self.chat_id = chat_id or "7316511307"  # Usa el proporcionado o el default
        self.token = "8268216056:AAH9qfeyv9CSV0zNt9GYU4xH9I8z7Y2WgYA"
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    def send_message(self, text):
        """Envía un mensaje de texto"""
        url = self.base_url + "sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, params=params)
        return response

    def send_photo(self, photo_path, caption=""):
        """Envía una foto"""
        url = self.base_url + "sendPhoto"

        with open(photo_path, 'rb') as photo_file:
            files = {'photo': photo_file}
            params = {
                'chat_id': self.chat_id,
                'caption': caption,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, files=files, data=params)
            return response