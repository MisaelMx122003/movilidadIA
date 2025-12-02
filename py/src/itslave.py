from src.itbot import Itbot

class Itslave:
    def __init__(self, mensaje):
        self.mensaje = mensaje

    def status(self):
        itbot = Itbot()
        itbot.send_message(self.mensaje)
    def conect_to(self):
        pass