import streamlit as st
from src.recommendations import MovieRecommender
from src.user_ratings import UserRatings
import pandas as pd

# Cargar datos de películas
movies_df = pd.read_csv('C:/Users/bakal/visualCode/recommender_system/data/processed/processed_movies.csv')

def show_movie_details(movie_index):
    movie = movies_df.iloc[movie_index]
    st.write(f"**{movie['title']}**")
    st.write(f"Sinopsis: {movie['synopsis']}")

def main():
    st.title("Sistema de Recomendación de Películas")

    recommender = MovieRecommender()

    # Mostrar las películas disponibles
    movie_titles = movies_df['title'].tolist()
    movie_index = st.selectbox("Selecciona una película", range(len(movie_titles)), format_func=lambda x: movie_titles[x])

    # Mostrar detalles de la película seleccionada
    show_movie_details(movie_index)

    # Valorar la película
    rating = st.slider("Valora esta película", 1, 5, 3)
    user_ratings = UserRatings()
    if st.button("Valorar"):
        user_ratings.rate_movie(movie_index, rating)
        st.write(f"Gracias por valorar la película con {rating} estrellas.")

    # Obtener recomendaciones basadas en la película seleccionada
    if st.button("Obtener recomendaciones"):
        similar_movies = recommender.recommend(movie_index)
        st.write("Películas similares recomendadas:")
        for idx in similar_movies:
            st.write(movies_df.iloc[idx]['title'])

if __name__ == "__main__":
    main()
