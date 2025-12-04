import json
import os
import re
from difflib import SequenceMatcher

class Itchatbot_movilidad:
    def __init__(self, ruta_dataset="data/rutas_respuestas.json"):
        self.ruta_dataset = ruta_dataset
        self.intenciones = self._cargar_intenciones()
        self.rutas_base = {
            "ruta_8": {
                "horario": "6:00 AM - 10:00 PM",
                "frecuencia": "Cada 15-20 minutos",
                "recorrido": "Centro → Banthi → V. de Guadalupe → Centro"
            },
            "ruta_10": {
                "horario": "5:30 AM - 9:30 PM",
                "frecuencia": "Cada 25 minutos",
                "recorrido": "Centro → Av. México → Carr. 57 → Centro"
            },
            "ruta_15": {
                "horario": "6:30 AM - 11:00 PM",
                "frecuencia": "Cada 30 minutos",
                "recorrido": "Terminal → Blvd. Hidalgo → Plaza San Juan → Terminal"
            }
        }
    
    def _cargar_intenciones(self):
        """Carga las intenciones desde JSON"""
        if os.path.exists(self.ruta_dataset):
            try:
                with open(self.ruta_dataset, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Intenciones por defecto
        return {
            "saludo": {
                "patrones": ["hola", "buenos días", "buenas tardes", "buenas noches"],
                "respuesta": "¡Hola! 👋 Soy tu asistente de movilidad. ¿En qué puedo ayudarte?"
            },
            "despedida": {
                "patrones": ["adiós", "hasta luego", "gracias", "chao"],
                "respuesta": "¡Hasta luego! 🚌 Que tengas un buen viaje."
            },
            "horario_ruta": {
                "patrones": ["horario", "a qué hora pasa", "cuándo pasa", "horarios de"],
                "respuesta": "Los horarios varían por ruta. ¿De qué ruta necesitas información?"
            },
            "ruta_destino": {
                "patrones": ["qué ruta va a", "cómo llego a", "ruta para", "transporte a"],
                "respuesta": "¿Desde dónde quieres partir y a qué destino?"
            },
            "trafico": {
                "patrones": ["hay tráfico", "tráfico en", "congestión", "embotellamiento"],
                "respuesta": "Actualmente hay tráfico moderado en Blvd. Hidalgo y Av. México."
            }
        }
    
    def _coincidencia_similaridad(self, texto_usuario, patrones):
        """Calcula la similitud entre el texto y los patrones"""
        mejor_similitud = 0
        mejor_patron = ""
        
        for patron in patrones:
            similitud = SequenceMatcher(None, texto_usuario.lower(), patron.lower()).ratio()
            if similitud > mejor_similitud:
                mejor_similitud = similitud
                mejor_patron = patron
        
        return mejor_similitud, mejor_patron
    
    def extraer_ruta(self, texto):
        """Extrae el número de ruta del texto"""
        numeros = re.findall(r'\b\d+\b', texto)
        if numeros:
            return f"ruta_{numeros[0]}"
        return None
    
    def procesar_mensaje(self, texto):
        """Procesa el mensaje del usuario y genera respuesta"""
        texto = texto.lower().strip()
        
        # 1. Extraer número de ruta si existe
        ruta_num = self.extract_ruta_number(texto)
        
        # 2. Identificar intención
        mejor_intencion = None
        mejor_similitud = 0
        
        for nombre_intencion, datos in self.intenciones.items():
            similitud, _ = self._coincidencia_similaridad(texto, datos["patrones"])
            if similitud > mejor_similitud and similitud > 0.4:  # Umbral
                mejor_similitud = similitud
                mejor_intencion = nombre_intencion
        
        # 3. Generar respuesta
        if mejor_intencion:
            respuesta_base = self.intenciones[mejor_intencion]["respuesta"]
            
            # Información específica de ruta
            if ruta_num and ruta_num in self.rutas_base:
                info_ruta = self.rutas_base[ruta_num]
                respuesta = f"{respuesta_base}\n\n📌 **Información de {ruta_num.replace('_', ' ')}:**\n"
                respuesta += f"⏰ Horario: {info_ruta['horario']}\n"
                respuesta += f"🔄 Frecuencia: {info_ruta['frecuencia']}\n"
                respuesta += f"📍 Recorrido: {info_ruta['recorrido']}"
                return respuesta
            
            return respuesta_base
        
        # Respuesta por defecto si no entiende
        return "No estoy seguro de entenderte. ¿Podrías reformular tu pregunta? Por ejemplo:\n• ¿A qué hora pasa la ruta 8?\n• ¿Cómo llego al centro?\n• ¿Hay tráfico en Av. México?"
    
    def extract_ruta_number(self, texto):
        """Extrae números de ruta del texto"""
        import re
        match = re.search(r'ruta\s*(\d+)|camión\s*(\d+)|\b(\d+)\b', texto.lower())
        if match:
            for group in match.groups():
                if group:
                    return f"ruta_{group}"
        return None
