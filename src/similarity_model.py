from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import numpy as np
import pandas as pd

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
        
        # Calcular similitudes para todas las películas
        similarities = cosine_similarity(movie_vector, self.tfidf_matrix).flatten()
        
        # Crear una lista de tuplas (índice, similitud) y ordenarlas por similitud
        similar_movies = [(i, sim) for i, sim in enumerate(similarities) if i != movie_index]
        similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
        
        # Retornar solo los índices de las películas más similares
        return [movie[0] for movie in similar_movies[:top_n]]

# Bloque de prueba
if __name__ == "__main__":
    model = SimilarityModel()
    movie_index = 0  # Cambia este índice para probar con diferentes películas
    similar_movies = model.find_similar(movie_index, top_n=5)
    print(f"Películas similares al índice {movie_index}: {similar_movies}")
