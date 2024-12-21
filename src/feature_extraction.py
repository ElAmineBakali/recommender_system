import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Configuración de rutas
PROCESSED_DATA_PATH = os.path.join('data', 'processed', 'processed_movies.csv')
TFIDF_MATRIX_PATH = os.path.join('data', 'features', 'tfidf_matrix.pkl')

# Clase para extracción de características
class FeatureExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english'
        )
    
    def fit_transform(self, texts):
        """
        Aplica TF-IDF al conjunto de textos y devuelve la matriz de características.
        """
        # Asegúrate de que todos los textos sean cadenas válidas
        texts = texts.fillna("").astype(str)
        return self.vectorizer.fit_transform(texts)

# Ejecución
if __name__ == "__main__":
    try:
        # Verifica si el archivo procesado existe
        if not os.path.exists(PROCESSED_DATA_PATH):
            raise FileNotFoundError(f"El archivo {PROCESSED_DATA_PATH} no existe.")

        # Carga el dataset preprocesado
        df = pd.read_csv(PROCESSED_DATA_PATH)

        # Verifica si la columna 'processed_synopsis' existe
        if 'processed_synopsis' not in df.columns:
            raise KeyError("La columna 'processed_synopsis' no existe en el dataset procesado.")
        
        # Extrae las características utilizando TF-IDF
        extractor = FeatureExtractor()
        tfidf_matrix = extractor.fit_transform(df['processed_synopsis'])

        # Guarda la matriz TF-IDF en un archivo para uso posterior
        os.makedirs(os.path.dirname(TFIDF_MATRIX_PATH), exist_ok=True)
        pd.DataFrame.sparse.from_spmatrix(tfidf_matrix).to_pickle(TFIDF_MATRIX_PATH)
        print(f"Matriz TF-IDF guardada en: {TFIDF_MATRIX_PATH}")
    
    except Exception as e:
        print(f"Error al extraer características: {e}")
