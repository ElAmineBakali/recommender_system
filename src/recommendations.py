from src.similarity_model import SimilarityModel
from src.user_ratings import UserRatings

class MovieRecommender:
    def __init__(self):
        self.similarity_model = SimilarityModel()
        self.user_ratings = UserRatings()

    def recommend(self, movie_index, top_n=5):
        """Genera recomendaciones basadas en similitudes y perfil del usuario."""
        # Obtener películas similares
        similar_movies = self.similarity_model.find_similar(movie_index, top_n)
        return similar_movies
