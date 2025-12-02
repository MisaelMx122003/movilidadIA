from src.itbot import Itbot

class Itconfig:
    def __init__(self, mensaje):
        self.mensaje = mensaje

    def get(self):
        itbot = Itbot()
        itbot.send_message(self.mensaje)