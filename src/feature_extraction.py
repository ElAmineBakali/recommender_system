from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
import os

PROCESSED_DATA_PATH = os.path.join('data', 'processed', 'processed_movies.csv')
TFIDF_VECTORS_PATH = os.path.join('data', 'processed', 'tfidf_vectors.pkl')

class FeatureExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
    
    def fit_transform(self, texts):
        """Aplica TF-IDF a una lista de textos."""
        return self.vectorizer.fit_transform(texts)
    
    def save_model(self, path):
        """Guarda el modelo vectorizador."""
        with open(path, 'wb') as file:
            pickle.dump(self.vectorizer, file)
        print(f"Modelo TF-IDF guardado en: {path}")

# Ejecución
if __name__ == "__main__":
    df = pd.read_csv(PROCESSED_DATA_PATH)
    extractor = FeatureExtractor()
    tfidf_matrix = extractor.fit_transform(df['processed_synopsis'])
    extractor.save_model(TFIDF_VECTORS_PATH)
    print("Vectorización TF-IDF completada.")
