from .itchatbot_movilidad import Itchatbot_movilidad
from .itsentimiento import Itsentimiento
from .itdenuncias import Itdenuncias

class Itai_movilidad:
    def __init__(self):
        """Inicializa todos los módulos de IA"""
        print("🚀 Inicializando sistema de IA para movilidad...")
        
        # Inicializar módulos
        self.chatbot = Itchatbot_movilidad()
        self.sentimiento = Itsentimiento()
        self.denuncias = Itdenuncias()
        
        print("✅ Sistema de IA listo")
    
    def procesar_mensaje(self, mensaje):
        """
        Procesa un mensaje y determina qué módulo usar
        Retorna: {"modulo": "chatbot|sentimiento|denuncia", "respuesta": str/dict}
        """
        mensaje = mensaje.lower().strip()
        
        # Palabras clave para cada módulo
        palabras_chatbot = ["horario", "ruta", "cómo llego", "transporte", "camión", "autobús"]
        palabras_sentimiento = ["queja", "malo", "pésimo", "excelente", "buen", "horrible"]
        palabras_denuncia = ["choque", "accidente", "bache", "semáforo", "bloqueo", "reportar"]
        
        # Determinar tipo de mensaje
        if any(palabra in mensaje for palabra in palabras_chatbot):
            respuesta = self.chatbot.procesar_mensaje(mensaje)
            return {"modulo": "chatbot", "respuesta": respuesta}
        
        elif any(palabra in mensaje for palabra in palabras_denuncia):
            resultado = self.denuncias.predecir(mensaje)
            respuesta = f"🚨 **Denuncia clasificada:** {resultado['categoria_detalle']}\n"
            respuesta += f"📊 **Confianza:** {resultado['probabilidades'].get(resultado['categoria'], 0)*100:.1f}%"
            return {"modulo": "denuncia", "respuesta": respuesta, "datos": resultado}
        
        elif any(palabra in mensaje for palabra in palabras_sentimiento):
            resultado = self.sentimiento.predecir(mensaje)
            emoji = "😊" if resultado['sentimiento'] == "positivo" else "😠" if resultado['sentimiento'] == "negativo" else "😐"
            respuesta = f"{emoji} **Sentimiento:** {resultado['sentimiento'].upper()}\n"
            respuesta += f"📈 **Probabilidades:** Positivo: {resultado['probabilidades']['positivo']*100:.1f}%, "
            respuesta += f"Negativo: {resultado['probabilidades']['negativo']*100:.1f}%"
            return {"modulo": "sentimiento", "respuesta": respuesta, "datos": resultado}
        
        else:
            # Por defecto, usar chatbot
            respuesta = self.chatbot.procesar_mensaje(mensaje)
            return {"modulo": "chatbot", "respuesta": respuesta}
    
    def entrenar_todos(self):
        """Entrena todos los modelos"""
        resultados = {}
        
        print("\n" + "="*50)
        print("🧠 ENTRENANDO TODOS LOS MODELOS DE IA")
        print("="*50)
        
        # Entrenar análisis de sentimiento
        print("\n📊 1. Entrenando análisis de sentimiento...")
        resultados['sentimiento'] = self.sentimiento.entrenar()
        
        # Entrenar clasificador de denuncias
        print("\n🚨 2. Entrenando clasificador de denuncias...")
        resultados['denuncias'] = self.denuncias.entrenar()
        
        print("\n" + "="*50)
        print("✅ ENTRENAMIENTO COMPLETADO")
        print("="*50)
        
        return resultados
    
    def obtener_estado(self):
        """Obtiene estado de todos los módulos"""
        return {
            "chatbot": "✅ Listo" if self.chatbot else "❌ No inicializado",
            "sentimiento": "✅ Modelo cargado" if self.sentimiento.modelo else "⚠️  Sin entrenar",
            "denuncias": "✅ Modelo cargado" if self.denuncias.modelo else "⚠️  Sin entrenar"
        }
