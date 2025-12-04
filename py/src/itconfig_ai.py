import json
import os

class Itconfig_ai:
    def __init__(self, config_path="config/ai_config.json"):
        self.config_path = config_path
        self.config = self._cargar_config()
    
    def _cargar_config(self):
        """Carga la configuración desde archivo"""
        config_default = {
            "modelos": {
                "sentimiento": {
                    "path": "modelos/sentiment_model.pkl",
                    "vectorizer": "modelos/sentiment_vectorizer.pkl",
                    "activo": True
                },
                "denuncias": {
                    "path": "modelos/denuncias_model.pkl",
                    "vectorizer": "modelos/denuncias_vectorizer.pkl",
                    "activo": True
                }
            },
            "datasets": {
                "sentimiento": "data/quejas.csv",
                "denuncias": "data/denuncias.csv",
                "chatbot": "data/rutas_respuestas.json"
            },
            "umbrales": {
                "similitud_chatbot": 0.4,
                "confianza_minima": 0.6
            },
            "ciudad": "San Juan del Río, Querétaro",
            "rutas_activas": ["ruta_8", "ruta_10", "ruta_15"]
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_usuario = json.load(f)
                    # Fusionar con defaults
                    self._fusionar_dicts(config_default, config_usuario)
            except:
                print("⚠️  Error cargando config, usando valores por defecto")
        
        return config_default
    
    def _fusionar_dicts(self, destino, fuente):
        """Fusiona diccionarios recursivamente"""
        for key, value in fuente.items():
            if key in destino and isinstance(destino[key], dict) and isinstance(value, dict):
                self._fusionar_dicts(destino[key], value)
            else:
                destino[key] = value
    
    def guardar(self):
        """Guarda la configuración"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"💾 Configuración guardada en {self.config_path}")
    
    def get(self, clave, valor_default=None):
        """Obtiene un valor de configuración"""
        keys = clave.split('.')
        valor = self.config
        
        for key in keys:
            if isinstance(valor, dict) and key in valor:
                valor = valor[key]
            else:
                return valor_default
        
        return valor
    
    def set(self, clave, valor):
        """Establece un valor de configuración"""
        keys = clave.split('.')
        config_ref = self.config
        
        for i, key in enumerate(keys[:-1]):
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]
        
        config_ref[keys[-1]] = valor
        self.guardar()
