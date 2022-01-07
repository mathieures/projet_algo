import imsdb_api
import tmdb_api
from ConfigWindow import ConfigWindow
from Interface import Interface
from Movie import PartialMovie, Movie
from Script import Script

import concurrent.futures
import os
from random import choices as rand_choices


SAVE_FILE_NAME = "movies_by_genre.pkl"
GRAPH_DICT = {}
MOVIES_INFOS = []


def pick_movies(data, count):
    choices = rand_choices(list(data), k=count)
    if count == 1:
        choices = choices[0]
    return choices

def extract_genres(tmdb_result):
    """
    Extraie les genres d'un résultat de l'API TMDB,
    car ils ne sont pas exploitables directement.
    """
    return [genre["name"] for genre in tmdb_result["genres"]]


def main():
    global GRAPH_DICT
    global MOVIES_INFOS

    # Récupération des données sur le site de scénarios
    print(f"Récupération des titres de film…")
    data = imsdb_api.getName()
    # Associe les noms de film à l'url de leur page IMSDB.

    config = ConfigWindow() # bloquant
    movie_nb, word_nb = config.movie_nb, config.word_nb


    picked_movies = pick_movies(data, movie_nb)
    print(f"Films choisis : {picked_movies}")

    try:
        for movie_title in picked_movies:

            movie = PartialMovie(title=movie_title)

            print(f"Film : {movie_title}")

            print("Téléchargement du script")
            # On télécharge le script
            movie.script = Script(data[movie_title], max_words=word_nb)
            try:
                movie.script.download() # Facultatif
            except RecursionError as e:
                print(e)
                print(f"[Avertissement] Choix d'un autre film.")
                picked_movies.append(pick_movies(data, 1)) # On en récupère un autre
                continue

            print("Traitement du script")
            # On le traite et on met le résultat dans le dictionnaire principal
            movie.script.parse() # Facultatif
            for word in movie.script.parsed_script:
                copy_without_word = movie.script.parsed_script.copy()
                del copy_without_word[word]
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

            # On fait appel à l'API TMDB pour avoir les autres informations
            tmdb_result = tmdb_api.search_movie(movie_title)
            if tmdb_result is None:
                print(f"[Avertissement] Informations indisponibles.")
                # Pour prendre un autre film, décommenter les lignes ci-dessous.
                # picked_movies.append(pick_movies(data, 1))
                # continue
            else:
                temp = PartialMovie.from_dict(tmdb_result)
                temp.genres = extract_genres(tmdb_result)

                # On rassemble tout dans un seul objet
                movie = Movie.merge_into_Movie(temp, movie)
            print(movie)

            MOVIES_INFOS.append(movie)

    # Pour pouvoir arrêter le processus si on est pressé : Ctrl+C
    except KeyboardInterrupt:
        pass

    # print("final :", GRAPH_DICT)

    nb_panels = 1
    interface = Interface(nb_panels, MOVIES_INFOS, GRAPH_DICT)  # bloquant


if __name__ == '__main__':
    main()
