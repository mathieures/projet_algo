import imsdb_api
import tmdb_api
from interface import Interface
from Movie import Movie

import pickle
import os
import threading


SAVE_FILE_NAME = "movies_by_genre.pkl"
UNKNOWN_GENRE = "(Unknown)"
NB_PARSED_MOVIES = 0
NB_MOVIES = 0
MOVIES_BY_GENRE = {} # Associe un genre (str) à une liste d'objets Movie


# TODO : voir ce qu'il faut modif ici, je pense qu'il y a bcp de trucs vu que
# j'ai modif Movie. Voir ce qu'on remplace par des PartialMovie, bien vérif
# les résultats, et aussi quand est-ce qu'on peut utiliser un Movie
# (après appel des deux APIs très sûrement)



def parse_movie_in_thread(title, movie_url, index=0):
    global NB_PARSED_MOVIES
    global MOVIES_BY_GENRE

    # print(f"Traitement du film {title} ({index}/{NB_MOVIES})")

    if temp_movie.script is None:
        print(f"[Avertissement] Le film '{title}' n'a pas de script")
    else:
        # TODO : Trouver pourquoi ça fonctionne pas toujours le cast (erreur du côté de bs4)
        try:
            # TODO : enlever le str() une fois le module modifié pour ne renvoyer que le texte
            temp_movie.script = str(temp_movie.script)
        except RecursionError as e:
            print(f"[Erreur] {e}")
        # S'il n'y a pas eu d'erreur
        else:
            # Récupération des genres grâce à l'API
            movie = None
            result = tmdb_api.search_movie(title)
            # Si le film a été trouvé sur le site
            if result is not None:
                movie = Movie.merge_into_Movie(temp_movie, result)

                # On ajoute les genres de ce film à l'index
                for genre in result.genres:
                    if genre not in MOVIES_BY_GENRE:
                        MOVIES_BY_GENRE[genre] = []
                    MOVIES_BY_GENRE[genre].append(movie)
            # Sinon, on ne connaît pas ses genres
            # TODO : voir si on prend les genres présents sur le site de script
            else:
                movie = Movie(title=title, genres=[], script=script)
                if UNKNOWN_GENRE not in MOVIES_BY_GENRE:
                    MOVIES_BY_GENRE[UNKNOWN_GENRE] = []
                MOVIES_BY_GENRE[UNKNOWN_GENRE].append(movie)

    # Dans tous les cas
    NB_PARSED_MOVIES += 1 # je crois que ça va pas jusqu'au bout
    print(f"-- Traitement de '{title}' terminé "
          f"(reste : {NB_MOVIES - NB_PARSED_MOVIES}) --")
    # print(movie)


def main():
    global NB_MOVIES
    global MOVIES_BY_GENRE

    if not os.path.exists(SAVE_FILE_NAME):
        # Récupération des données sur le site de scénarios
        # Dictionnaire associant un nom de film à un url et des genres
        data = imsdb_api.getName()
        NB_MOVIES = len(data)

        # Conversion en objets Movie

        # On lance et on attend que tout se finisse

        """
        threads = [
            threading.Thread(
                target=parse_movie_in_thread,
                args=(title, data[title], i)
            ) for i, title in enumerate(data, start=1)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        """
            
        # with open(SAVE_FILE_NAME, "wb") as f:
        #     pickle.dump(MOVIES_BY_GENRE, f)
    else:
        with open(SAVE_FILE_NAME, "rb") as f:
            MOVIES_BY_GENRE = pickle.load(f)

    nb_panels = 2
    interface = Interface(nb_panels, MOVIES_BY_GENRE)  # bloquant


if __name__ == '__main__':
    main()
