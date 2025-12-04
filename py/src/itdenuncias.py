import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report
import joblib
import os
from .itpreprocesamiento import Itpreprocesamiento

class Itdenuncias:
    def __init__(self, modelo_path="modelos/denuncias_model.pkl"):
        self.modelo_path = modelo_path
        self.vectorizer_path = "modelos/denuncias_vectorizer.pkl"
        self.preprocesador = Itpreprocesamiento()
        self.modelo = None
        self.vectorizer = None
        
        # Categorías de denuncias
        self.categorias = [
            "choque", "bache", "semáforo", "bloqueo", 
            "tráfico", "transporte_detenido", "conducción_peligrosa"
        ]
        
        self.cargar_modelo()
    
    def cargar_modelo(self):
        """Carga el modelo si existe"""
        if os.path.exists(self.modelo_path) and os.path.exists(self.vectorizer_path):
            try:
                self.modelo = joblib.load(self.modelo_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                print("✅ Modelo de denuncias cargado")
            except:
                print("⚠️  Error cargando modelo, se entrenará uno nuevo")
                self.modelo = None
    
    def entrenar(self, ruta_dataset="data/denuncias.csv"):
        """Entrena un nuevo modelo de clasificación"""
        if not os.path.exists(ruta_dataset):
            print("❌ Dataset no encontrado")
            return False
        
        # Cargar datos
        df = pd.read_csv(ruta_dataset)
        
        # Verificar columnas necesarias
        if 'descripcion' not in df.columns or 'categoria' not in df.columns:
            print("❌ Columnas incorrectas en el dataset")
            return False
        
        # Filtrar categorías válidas
        df = df[df['categoria'].isin(self.categorias)]
        
        if df.empty:
            print("❌ No hay datos válidos para las categorías definidas")
            return False
        
        # Preprocesar texto
        print("🔄 Preprocesando texto...")
        df['texto_limpio'] = df['descripcion'].apply(self.preprocesador.limpiar_texto)
        
        # Vectorizar
        print("🔢 Vectorizando texto...")
        self.vectorizer = TfidfVectorizer(max_features=3000)
        X = self.vectorizer.fit_transform(df['texto_limpio'])
        y = df['categoria']
        
        # Entrenar modelo
        print("🧠 Entrenando modelo...")
        self.modelo = RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            n_jobs=-1
        )
        self.modelo.fit(X, y)
        
        # Evaluar (validación cruzada)
        from sklearn.model_selection import cross_val_predict
        y_pred = cross_val_predict(self.modelo, X, y, cv=5)
        
        print("\n📊 **Resultados del modelo (5-fold CV):**")
        print(classification_report(y, y_pred, target_names=self.categorias))
        
        # Guardar modelo
        self.guardar_modelo()
        
        return True
    
    def predecir(self, texto):
        """Clasifica una denuncia en categorías"""
        if self.modelo is None:
            return {"error": "Modelo no entrenado", "categoria": "desconocida"}
        
        # Preprocesar texto
        texto_limpio = self.preprocesador.limpiar_texto(texto)
        
        # Vectorizar
        X = self.vectorizer.transform([texto_limpio])
        
        # Predecir
        categoria = self.modelo.predict(X)[0]
        probabilidades = self.modelo.predict_proba(X)[0]
        
        # Crear diccionario de probabilidades por categoría
        prob_dict = {}
        for cat, prob in zip(self.modelo.classes_, probabilidades):
            prob_dict[cat] = round(float(prob), 3)
        
        return {
            "texto": texto,
            "categoria": categoria,
            "probabilidades": prob_dict,
            "categoria_detalle": self._obtener_descripcion_categoria(categoria)
        }
    
    def _obtener_descripcion_categoria(self, categoria):
        """Obtiene descripción detallada de la categoría"""
        descripciones = {
            "choque": "🚗 Accidente vehicular o colisión",
            "bache": "🕳️ Daño en el pavimento o bache",
            "semáforo": "🚦 Semáforo descompuesto o apagado",
            "bloqueo": "🚧 Obstrucción o bloqueo vial",
            "tráfico": "🚗 Congestión vehicular",
            "transporte_detenido": "🚌 Transporte público detenido",
            "conducción_peligrosa": "⚠️ Conducción temeraria o peligrosa"
        }
        return descripciones.get(categoria, "Categoría no especificada")
    
    def guardar_modelo(self):
        """Guarda el modelo entrenado"""
        if self.modelo and self.vectorizer:
            os.makedirs("modelos", exist_ok=True)
            joblib.dump(self.modelo, self.modelo_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            print(f"💾 Modelo de denuncias guardado en {self.modelo_path}")
