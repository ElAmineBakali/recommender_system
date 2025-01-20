import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from src.recommendations import MovieRecommender
from src.user_ratings import UserRatings

# Cargar los datos de películas y resetear los índices
movies_df = pd.read_csv('data/processed/processed_movies.csv')
movies_df = movies_df.drop_duplicates(subset='title').reset_index(drop=True)

# Inicializar las valoraciones del usuario
user_ratings = UserRatings()

# Crear la ventana principal
root = tk.Tk()
root.title("🎬 Movie Recommender App")
root.geometry("600x600")
root.configure(bg="#2C3E50")

# Estilos personalizados estilo oscuro
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#2C3E50", foreground="#ECF0F1", font=("Helvetica", 12))
style.configure("TButton", background="#E74C3C", foreground="#FFFFFF", font=("Helvetica", 12), padding=5)
style.configure("TCombobox", background="#34495E", foreground="#FFFFFF", font=("Helvetica", 12))

# Función para mostrar los detalles de la película seleccionada
def show_movie_details():
    selected_index = movie_combobox.current()
    if selected_index == -1:
        messagebox.showerror("Error", "Por favor selecciona una película.")
        return

    movie = movies_df.iloc[selected_index]
    details = f"Título: {movie['title']}\n\nSinopsis: {movie['synopsis']}"
    movie_details_label.config(text=details)

    # Cargar la valoración si existe
    if str(selected_index) in user_ratings.get_ratings():
        current_rating = user_ratings.get_ratings()[str(selected_index)]
        rating_scale.set(current_rating)
        current_rating_label.config(text=f"Nota actual: {current_rating} estrellas")
    else:
        rating_scale.set(1)  # Valoración predeterminada
        current_rating_label.config(text="Nota actual: 1 estrella")

# Función para actualizar la nota seleccionada en tiempo real
def update_rating_label(value):
    current_rating_label.config(text=f"Nota seleccionada: {int(float(value))} estrellas")

# Función para guardar la valoración de una película
def rate_movie():
    selected_index = movie_combobox.current()
    if selected_index == -1:
        messagebox.showerror("Error", "Por favor selecciona una película.")
        return

    # Obtener el valor de la escala
    rating = int(rating_scale.get())
    try:
        user_ratings.rate_movie(str(selected_index), rating)
        messagebox.showinfo("Éxito", f"Valoración guardada: {rating} estrellas")
        current_rating_label.config(text=f"Nota actual: {rating} estrellas")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Función para generar recomendaciones
def get_recommendations():
    selected_index = movie_combobox.current()
    if selected_index == -1:
        messagebox.showerror("Error", "Por favor selecciona una película.")
        return

    recommender = MovieRecommender()
    recommendations = recommender.recommend(selected_index, top_n=5)

    # Validar si los índices están dentro del rango del DataFrame
    valid_indices = [idx for idx in recommendations if idx < len(movies_df)]

    # Eliminar la película base de las recomendaciones (si está presente)
    filtered_indices = [idx for idx in valid_indices if idx != selected_index]

    # Convertir índices a títulos
    recommended_titles = [movies_df.iloc[i]['title'] for i in filtered_indices]
    if recommended_titles:
        recommendations_label.config(text="\n".join(recommended_titles))
    else:
        recommendations_label.config(text="No se encontraron recomendaciones válidas.")

# Crear widgets
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True)

movie_combobox = ttk.Combobox(main_frame, values=movies_df['title'].tolist(), width=50)
movie_combobox.grid(row=0, column=0, columnspan=2, pady=10)

select_button = ttk.Button(main_frame, text="Mostrar Detalles", command=show_movie_details)
select_button.grid(row=1, column=0, padx=5, pady=10)

recommend_button = ttk.Button(main_frame, text="Obtener Recomendaciones", command=get_recommendations)
recommend_button.grid(row=1, column=1, padx=5, pady=10)

movie_details_label = ttk.Label(main_frame, text="", wraplength=500, justify="left")
movie_details_label.grid(row=2, column=0, columnspan=2, pady=10)

rating_label = ttk.Label(main_frame, text="Valorar película (1-5):")
rating_label.grid(row=3, column=0, pady=5)

rating_scale = ttk.Scale(main_frame, from_=1, to=5, orient="horizontal", length=200, command=update_rating_label)
rating_scale.grid(row=3, column=1, pady=5)

current_rating_label = ttk.Label(main_frame, text="Nota seleccionada: 1 estrella")
current_rating_label.grid(row=4, column=0, columnspan=2, pady=5)

rate_button = ttk.Button(main_frame, text="Guardar valoración", command=rate_movie)
rate_button.grid(row=5, column=0, columnspan=2, pady=10)

recommendations_label = ttk.Label(main_frame, text="", wraplength=500, justify="left")
recommendations_label.grid(row=6, column=0, columnspan=2, pady=10)

# Ejecutar la aplicación
root.mainloop()
