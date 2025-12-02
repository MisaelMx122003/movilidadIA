from src.itbot import Itbot

class Itlog:
    def __init__(self, mensaje):
        self.mensaje = mensaje

    def register(self):
        itbot = Itbot()
        itbot.send_message(self.mensaje)