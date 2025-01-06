import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Configuración de rutas
RAW_DATA_PATH = os.path.join('data', 'raw', 'movies_dataset.csv')
PROCESSED_DATA_PATH = os.path.join('data', 'processed', 'processed_movies.csv')

# Clase para preprocesamiento de datos
class DataPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        """Preprocesa texto: tokenización, eliminación de stop words y lematización."""
        if not isinstance(text, str) or not text.strip():
            return ""  # Retorna una cadena vacía si el texto es nulo o inválido

        tokens = word_tokenize(text.lower())
        filtered_tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in self.stop_words]
        return " ".join(filtered_tokens)

    def preprocess_dataset(self, input_path, output_path):
        """Carga, limpia y guarda el dataset preprocesado."""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"El archivo {input_path} no existe.")

        # Carga el dataset original
        df = pd.read_csv(input_path)

        # Manejo de valores nulos en las columnas 'synopsis' y 'genres'
        df['synopsis'] = df['synopsis'].fillna("")
        df['genres'] = df['genres'].fillna("")

        # Aplica el preprocesamiento de texto a la sinopsis
        df['processed_synopsis'] = df['synopsis'].apply(self.preprocess_text)

        # Verifica si la columna procesada está vacía
        if df['processed_synopsis'].str.strip().eq("").all():
            raise ValueError("Todos los textos procesados están vacíos. Revisa los datos de entrada y el preprocesamiento.")

        # Guarda el dataset procesado
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Dataset preprocesado guardado en: {output_path}")

# Ejecución
if __name__ == "__main__":
    try:
        preprocessor = DataPreprocessor()
        preprocessor.preprocess_dataset(RAW_DATA_PATH, PROCESSED_DATA_PATH)
    except Exception as e:
        print(f"Error durante el preprocesamiento: {e}")
