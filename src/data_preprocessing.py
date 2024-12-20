import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

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
        tokens = word_tokenize(text.lower())
        filtered_tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in self.stop_words]
        return " ".join(filtered_tokens)
    
    def preprocess_dataset(self, input_path, output_path):
        """Carga, limpia y guarda el dataset preprocesado."""
        df = pd.read_csv(input_path)
        df['processed_synopsis'] = df['synopsis'].apply(self.preprocess_text)
        df.to_csv(output_path, index=False)
        print(f"Dataset preprocesado guardado en: {output_path}")

# Ejecución
if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    preprocessor.preprocess_dataset(RAW_DATA_PATH, PROCESSED_DATA_PATH)
