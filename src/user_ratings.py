import json
import os

class UserRatings:
    def __init__(self, ratings_file='user_ratings.json'):
        self.ratings_file = ratings_file
        self.ratings = self.load_ratings()

    def load_ratings(self):
        """Carga las valoraciones desde un archivo JSON."""
        if os.path.exists(self.ratings_file):
            with open(self.ratings_file, 'r') as file:
                return json.load(file)
        return {}

    def save_ratings(self):
        """Guarda las valoraciones en un archivo JSON."""
        with open(self.ratings_file, 'w') as file:
            json.dump(self.ratings, file, indent=4)

    def rate_movie(self, movie_index, rating):
        """Asigna o actualiza una valoración (1-5) a una película."""
        if rating < 1 or rating > 5:
            raise ValueError("La valoración debe estar entre 1 y 5 estrellas.")
        self.ratings[movie_index] = rating
        self.save_ratings()

    def get_ratings(self):
        """Devuelve todas las valoraciones del usuario."""
        return self.ratings
