import imsdb_api
import tmdb_api
from interface import Interface
import Movie

import concurrent.futures
import os


SAVE_FILE_NAME = "movies_by_genre.pkl"
MOVIES_BY_GENRE = {} # Associe un genre (str) à une liste d'objets Movie


def main():
    global NB_MOVIES
    global MOVIES_BY_GENRE

    # Récupération des données sur le site de scénarios
    data = imsdb_api.getName()
    # Associe un genre à un dictionnaire { "nom_film_1": "url_film_1", … }

    # Conversion en objets PartialMovie
    for genre, movies in data.items():
        # Pour chaque film du genre actuel
        for title in movies:
            # S'il n'y avait pas ce genre dans le dictionnaire
            if genre not in MOVIES_BY_GENRE:
                MOVIES_BY_GENRE[genre] = []
            # Dans tous les cas on l'ajoute à la liste
            MOVIES_BY_GENRE[genre].append(
                Movie.PartialMovie(
                    title=title,
                    genres=genre,
                    movie_url=movies[title]
                )
            ) # Un PartialMovie permet de garder en mémoire son url

    print(MOVIES_BY_GENRE)

    nb_panels = 2
    interface = Interface(nb_panels, MOVIES_BY_GENRE)  # bloquant


if __name__ == '__main__':
    main()
