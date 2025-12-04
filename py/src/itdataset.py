import pandas as pd
import json
import os

class Itdataset:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def crear_dataset_sentimiento(self):
        """Crea dataset de ejemplo para análisis de sentimiento"""
        data = [
            {"texto_queja": "El tráfico está horrible en la 57", "sentimiento": "negativo"},
            {"texto_queja": "Hoy avanzó rápido, buen servicio", "sentimiento": "positivo"},
            {"texto_queja": "Llegué sin retrasos", "sentimiento": "neutro"},
            {"texto_queja": "El camión pasó a tiempo", "sentimiento": "positivo"},
            {"texto_queja": "Mucho tráfico y accidentes", "sentimiento": "negativo"},
            {"texto_queja": "Fluye rápido el tráfico hoy", "sentimiento": "positivo"},
            {"texto_queja": "Semáforo descompuesto en el centro", "sentimiento": "negativo"},
            {"texto_queja": "Servicio regular, sin novedad", "sentimiento": "neutro"},
            {"texto_queja": "Pésimo servicio de transporte", "sentimiento": "negativo"},
            {"texto_queja": "Excelente atención del conductor", "sentimiento": "positivo"}
        ]
        
        df = pd.DataFrame(data)
        ruta = os.path.join(self.data_dir, "quejas.csv")
        df.to_csv(ruta, index=False, encoding='utf-8')
        print(f"✅ Dataset de sentimiento creado: {ruta}")
        return ruta
    
    def crear_dataset_denuncias(self):
        """Crea dataset de ejemplo para clasificación de denuncias"""
        data = [
            {"descripcion": "Hay un bache enorme en el carril izquierdo", "categoria": "bache"},
            {"descripcion": "Chocaron dos autos en Blvd. Juárez", "categoria": "choque"},
            {"descripcion": "Semáforo apagado en el centro", "categoria": "semáforo"},
            {"descripcion": "Bloqueo total en Av. México", "categoria": "bloqueo"},
            {"descripcion": "Tráfico intenso en hora pico", "categoria": "tráfico"},
            {"descripcion": "Autobús descompuesto en la parada", "categoria": "transporte_detenido"},
            {"descripcion": "Conductor manejando a exceso de velocidad", "categoria": "conducción_peligrosa"},
            {"descripcion": "Bache profundo en curva peligrosa", "categoria": "bache"},
            {"descripcion": "Accidente con heridos en carretera 57", "categoria": "choque"},
            {"descripcion": "Semáforo intermitente causa confusión", "categoria": "semáforo"}
        ]
        
        df = pd.DataFrame(data)
        ruta = os.path.join(self.data_dir, "denuncias.csv")
        df.to_csv(ruta, index=False, encoding='utf-8')
        print(f"✅ Dataset de denuncias creado: {ruta}")
        return ruta
    
    def crear_dataset_chatbot(self):
        """Crea dataset de ejemplo para chatbot"""
        data = {
            "intenciones": [
                {
                    "tag": "horario_ruta",
                    "patrones": ["a qué hora pasa el camión 8", "horarios ruta 8", "pasa la ruta 8 hoy?"],
                    "respuesta": "La ruta 8 pasa cada 15 minutos por el centro entre 6am y 10pm."
                },
                {
                    "tag": "ruta_destino",
                    "patrones": ["qué ruta me lleva al centro", "cómo llego a Banthi", "transporte al centro comercial"],
                    "respuesta": "Para llegar al centro puedes tomar la ruta 8 o 10. ¿Desde dónde partes?"
                },
                {
                    "tag": "trafico",
                    "patrones": ["hay tráfico", "está congestionado", "embotellamiento en"],
                    "respuesta": "Reportes indican tráfico moderado en Blvd. Hidalgo. Evita Av. México si es posible."
                },
                {
                    "tag": "incidente",
                    "patrones": ["hubo accidente", "choque en", "incidente vial"],
                    "respuesta": "Según reportes, hay un incidente en Av. Juárez. Toma rutas alternas."
                }
            ]
        }
        
        ruta = os.path.join(self.data_dir, "rutas_respuestas.json")
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Dataset de chatbot creado: {ruta}")
        return ruta
    
    def crear_todos(self):
        """Crea todos los datasets de ejemplo"""
        print("📊 Creando todos los datasets de ejemplo...")
        return {
            "sentimiento": self.crear_dataset_sentimiento(),
            "denuncias": self.crear_dataset_denuncias(),
            "chatbot": self.crear_dataset_chatbot()
        }
