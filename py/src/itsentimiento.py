import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import joblib
import os
from .itpreprocesamiento import Itpreprocesamiento

class Itsentimiento:
    def __init__(self, modelo_path="modelos/sentiment_model.pkl"):
        self.modelo_path = modelo_path
        self.vectorizer_path = "modelos/sentiment_vectorizer.pkl"
        self.preprocesador = Itpreprocesamiento()
        self.modelo = None
        self.vectorizer = None
        self.cargar_modelo()
    
    def cargar_modelo(self):
        """Carga el modelo si existe"""
        if os.path.exists(self.modelo_path) and os.path.exists(self.vectorizer_path):
            try:
                self.modelo = joblib.load(self.modelo_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                print("✅ Modelo de sentimiento cargado")
            except:
                print("⚠️  Error cargando modelo, se entrenará uno nuevo")
                self.modelo = None
    
    def entrenar(self, ruta_dataset="data/quejas.csv"):
        """Entrena un nuevo modelo de análisis de sentimiento"""
        if not os.path.exists(ruta_dataset):
            print("❌ Dataset no encontrado")
            return False
        
        # Cargar datos
        df = pd.read_csv(ruta_dataset)
        
        # Verificar columnas necesarias
        if 'texto_queja' not in df.columns or 'sentimiento' not in df.columns:
            print("❌ Columnas incorrectas en el dataset")
            return False
        
        # Preprocesar texto
        print("🔄 Preprocesando texto...")
        df['texto_limpio'] = df['texto_queja'].apply(self.preprocesador.limpiar_texto)
        
        # Vectorizar
        print("🔢 Vectorizando texto...")
        self.vectorizer = TfidfVectorizer(max_features=5000)
        X = self.vectorizer.fit_transform(df['texto_limpio'])
        y = df['sentimiento']
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Entrenar modelo
        print("🧠 Entrenando modelo...")
        self.modelo = MultinomialNB()
        self.modelo.fit(X_train, y_train)
        
        # Evaluar
        y_pred = self.modelo.predict(X_test)
        print("\n📊 **Resultados del modelo:**")
        print(classification_report(y_test, y_pred))
        
        # Guardar modelo
        self.guardar_modelo()
        
        return True
    
    def predecir(self, texto):
        """Predice el sentimiento de un texto"""
        if self.modelo is None:
            return {"error": "Modelo no entrenado", "sentimiento": "neutro"}
        
        # Preprocesar texto
        texto_limpio = self.preprocesador.limpiar_texto(texto)
        
        # Vectorizar
        X = self.vectorizer.transform([texto_limpio])
        
        # Predecir
        sentimiento = self.modelo.predict(X)[0]
        probabilidades = self.modelo.predict_proba(X)[0]
        
        return {
            "texto": texto,
            "sentimiento": sentimiento,
            "probabilidades": {
                "positivo": round(float(probabilidades[0] if sentimiento == "positivo" else probabilidades[1]), 3),
                "negativo": round(float(probabilidades[1] if sentimiento == "negativo" else probabilidades[0]), 3),
                "neutro": round(float(probabilidades[2] if len(probabilidades) > 2 else 0), 3)
            }
        }
    
    def guardar_modelo(self):
        """Guarda el modelo entrenado"""
        if self.modelo and self.vectorizer:
            os.makedirs("modelos", exist_ok=True)
            joblib.dump(self.modelo, self.modelo_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            print(f"💾 Modelo guardado en {self.modelo_path}")
    
    def analizar_batch(self, textos):
        """Analiza múltiples textos"""
        resultados = []
        for texto in textos:
            resultados.append(self.predecir(texto))
        return resultados
