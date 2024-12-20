from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

TFIDF_VECTORS_PATH = os.path.join('data', 'processed', 'tfidf_vectors.pkl')

class SimilarityModel:
    def __init__(self):
        with open(TFIDF_VECTORS_PATH, 'rb') as file:
            self.tfidf_matrix = pickle.load(file)
    
    def find_similar(self, movie_index, top_n=5):
        """Encuentra las películas más similares dado un índice."""
        similarities = cosine_similarity(self.tfidf_matrix[movie_index], self.tfidf_matrix)
        similar_indices = similarities.argsort()[0, -top_n-1:-1][::-1]
        return similar_indices

# Ejecución de prueba
if __name__ == "__main__":
    model = SimilarityModel()
    print("Películas similares:", model.find_similar(0, top_n=5))
