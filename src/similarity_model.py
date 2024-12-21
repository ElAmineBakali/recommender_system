from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import numpy as np

TFIDF_VECTORS_PATH = os.path.join('data', 'features', 'tfidf_matrix.pkl')

class SimilarityModel:
    def __init__(self):
        with open(TFIDF_VECTORS_PATH, 'rb') as file:
            self.tfidf_matrix = pickle.load(file)
        # Convertimos el DataFrame a un array Numpy si es necesario
        if isinstance(self.tfidf_matrix, pd.DataFrame):
            self.tfidf_matrix = self.tfidf_matrix.to_numpy()

    def find_similar(self, movie_index, top_n=5):
        """Encuentra las películas más similares dado un índice."""
        # Asegúrate de que la fila seleccionada sea 2D para cosine_similarity
        movie_vector = self.tfidf_matrix[movie_index].reshape(1, -1)
        similarities = cosine_similarity(movie_vector, self.tfidf_matrix)
        similar_indices = similarities.argsort()[0, -top_n-1:-1][::-1]
        return similar_indices

# Ejecución de prueba
if __name__ == "__main__":
    import pandas as pd  # Import necesario solo si tfidf_matrix es un DataFrame
    model = SimilarityModel()
    print("Películas similares:", model.find_similar(0, top_n=5))
