import imsdb_api
import tmdb_api
import script_parsing
from interface import Interface
import Movie

import concurrent.futures
import os


SAVE_FILE_NAME = "movies_by_genre.pkl"
MOVIES = [] # Temporairement, liste d'objets PartialMovie pour le test
# MOVIES = [] # Liste d'objets Movie, complètement traités


def main():
    global MOVIES

    # Récupération des données sur le site de scénarios
    data = imsdb_api.getName()
    # Associe les noms de film à l'url de leur page IMSDB.

    # Conversion en objets PartialMovie
    for movie_title in data:
        # TODO : voir si on garde l'API ou pas, vu qu'on n'a besoin que du script
        """
        # On fait appel à l'API TMDB pour avoir les autres informations
        movie = tmdb_api.search_movie(movie_title)
        """

        # On télécharge et traite le script
        movie = imsdb_api.getScript(data[movie_title])

        # Enfin on ajoute le film à la liste
        MOVIES.append(

        )

    print(MOVIES_BY_GENRE)

    nb_panels = 2
    interface = Interface(nb_panels, MOVIES_BY_GENRE)  # bloquant


if __name__ == '__main__':
    main()
