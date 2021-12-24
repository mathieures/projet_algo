from imsdb_api import getName as get_all_scripts_urls, getScript as get_script
import tmdb_api
from interface import Interface
from Movie import Movie

import pickle
import os


if not os.path.exists("movies_by_genre.pkl"):
    # Récupération des données sur le site de scénarios
    data = get_all_scripts_urls() # Dictionnaire associant un nom de film à un url de script

    # Conversion en objets Movie
    movies_by_genre = {} # Associe un genre (str) à une liste d'objets Movie
    for i, title in enumerate(data):
        print(f"Traitement du film {title}… ({i + 1}/{len(data)})")
        # Récupération du script sur la page html
        # TODO : enlever le str() une fois le module modifié pour ne renvoyer que le texte
        script = str(get_script(data[title]))

        # Récupération des genres grâce à l'API
        # TODO : plus tard, le faire en asynchrone pour être plus rapide

        result = tmdb_api.search_movie(title)
        movie = None
        # Si le film a été trouvé sur le site
        if result is not None:
            movie = Movie(title=result.title,
                          genres=result.genres,
                          script=script)

            # On ajoute les genres de ce film à l'index
            for genre in result.genres:
                if genre not in movies_by_genre:
                    movies_by_genre[genre] = []
                movies_by_genre[genre].append(movie)
        # Sinon, on ne connaît pas ses genres
        # TODO : voir si on prend les genres présents sur le site de script
        else:
            movie = Movie(title=title, genres=[], script=script)
            if UNKNOWN_GENRE not in movies_by_genre:
                movies_by_genre[UNKNOWN_GENRE] = []
            movies_by_genre[UNKNOWN_GENRE].append(movie)

        # print(movie)
        # all_movies.append(movie)

    pickle.dump(movies_by_genre, "movies_by_genre.pkl")
else:
    movies_by_genre = pickle.load("movies_by_genre.pkl")

nb_panels = 2
interface = Interface(nb_panels, movies_by_genre) # bloquant