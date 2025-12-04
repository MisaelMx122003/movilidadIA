import re
import spacy
import unicodedata

class Itpreprocesamiento:
    def __init__(self):
        # Cargar modelo en español de spaCy
        try:
            self.nlp = spacy.load("es_core_news_sm")
        except:
            # Si no está instalado, descargarlo
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])
            self.nlp = spacy.load("es_core_news_sm")
        
        # Stopwords en español personalizadas
        self.stopwords = set([
            'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 
            'del', 'se', 'las', 'por', 'un', 'para', 'con', 
            'no', 'una', 'su', 'al', 'lo', 'como', 'más', 
            'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 
            'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 
            'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 
            'quien', 'desde', 'todo', 'nos', 'durante', 'todos', 
            'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 
            'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 
            'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 
            'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 
            'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 
            'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 
            'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 
            'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 
            'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 
            'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 
            'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 
            'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 
            'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás', 
            'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 
            'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 
            'estabas', 'estábamos', 'estabais', 'estaban', 'estuve', 
            'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 
            'estuviera', 'estuvieras', 'estuviéramos', 'estuvierais', 
            'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos', 
            'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 
            'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 
            'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 
            'hayan', 'habré', 'habrás', 'habrá', 'habremos', 'habréis', 
            'habrán', 'habría', 'habrías', 'habríamos', 'habríais', 
            'habrían', 'había', 'habías', 'habíamos', 'habíais', 'habían', 
            'hube', 'hubiste', 'hubo', 'hubimos', 'hubisteis', 'hubieron', 
            'hubiera', 'hubieras', 'hubiéramos', 'hubierais', 'hubieran', 
            'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 
            'habiendo', 'habido', 'habida', 'habidos', 'habidas'
        ])
    
    def limpiar_texto(self, texto):
        """Limpia y normaliza el texto para procesamiento"""
        if not texto or not isinstance(texto, str):
            return ""
        
        # 1. Convertir a minúsculas
        texto = texto.lower()
        
        # 2. Eliminar acentos y caracteres especiales
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
        
        # 3. Eliminar URLs
        texto = re.sub(r'http\S+|www\S+|https\S+', '', texto, flags=re.MULTILINE)
        
        # 4. Eliminar menciones (@) y hashtags (#)
        texto = re.sub(r'@\w+|#\w+', '', texto)
        
        # 5. Eliminar números
        texto = re.sub(r'\d+', '', texto)
        
        # 6. Eliminar emojis y símbolos especiales
        texto = re.sub(r'[^\w\s]', ' ', texto)
        
        # 7. Tokenización y lematización con spaCy
        doc = self.nlp(texto)
        tokens_lematizados = []
        
        for token in doc:
            # Lematizar y filtrar stopwords
            if token.text not in self.stopwords and len(token.text) > 2:
                tokens_lematizados.append(token.lemma_)
        
        # 8. Unir tokens
        texto_limpio = ' '.join(tokens_lematizados)
        
        # 9. Eliminar espacios múltiples
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
        
        return texto_limpio
    
    def procesar_lista(self, textos):
        """Procesa una lista de textos"""
        return [self.limpiar_texto(texto) for texto in textos]
