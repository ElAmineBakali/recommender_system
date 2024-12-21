import pandas as pd

# Cargar los datos procesados
movies_df = pd.read_csv('data/processed/movies_dataset.csv')

class UserRatings:
    def __init__(self):
        self.ratings = {}

    def rate_movie(self, movie_index, rating):
        """Asigna una valoración (1-5) a una película."""
        if movie_index in self.ratings:
            self.ratings[movie_index].append(rating)
        else:
            self.ratings[movie_index] = [rating]

    def get_ratings(self):
        """Devuelve todas las valoraciones del usuario."""
        return self.ratings

    def update_user_profile(self):
        """Ajusta el perfil del usuario en función de las valoraciones."""
        # Puedes agregar lógica aquí para actualizar el perfil según géneros, actores, etc.
        pass
