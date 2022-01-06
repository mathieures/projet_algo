import imsdb_api
import tmdb_api
from Interface import Interface
import Movie
import Script

import concurrent.futures
import os


SAVE_FILE_NAME = "movies_by_genre.pkl"
GRAPH_DICT = {}


def main():
    global GRAPH_DICT

    # Récupération des données sur le site de scénarios
    data = imsdb_api.getName()
    # Associe les noms de film à l'url de leur page IMSDB.

    try:
        for movie_title in data:
            print(f"Film : {movie_title}")
            # TODO : voir si on garde l'API ou pas, vu qu'on n'a besoin que du script
            """
            # On fait appel à l'API TMDB pour avoir les autres informations
            movie = tmdb_api.search_movie(movie_title)
            """

            print("Téléchargement du script")
            # On télécharge le script
            script = Script.Script(data[movie_title])
            script.download() # Facultatif


            print("Traitement du script")
            # On le traite et on met le résultat dans le dictionnaire principal
            script.parse() # Facultatif
            for word in script.parsed_script:
                copy_without_word = script.parsed_script.copy()
                copy_without_word.pop(word)
                # Si le mot de base n'est pas présent dans le dictionnaire,
                # Alors il n'y a pas encore d'occurrences
                if word not in GRAPH_DICT:
                    GRAPH_DICT[word] = copy_without_word
                    # print("new graph dict :", GRAPH_DICT)
                # S'il l'est, il faut additionner les occurrences
                else:
                    # Pour chaque autre mot lié à ce mot
                    for other_word in copy_without_word:
                        if other_word not in GRAPH_DICT[word]:
                            GRAPH_DICT[word][other_word] = 0
                        # On additionne
                        GRAPH_DICT[word][other_word] += copy_without_word[other_word]

            # A SUPPRIMER
            print("Fin du traitement du script")
            break

                # GRAPH_DICT.update(script.parsed_script)
    # Pour pouvoir arrêter le processus si on est pressé
    except KeyboardInterrupt:
        pass

    # print("final :", GRAPH_DICT)

    nb_panels = 1
    interface = Interface(nb_panels, GRAPH_DICT)  # bloquant


if __name__ == '__main__':
    main()
