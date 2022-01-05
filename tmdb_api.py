import requests
import json
from Movie import PartialMovie


_API_KEY = "dd6b80f1beb24a174bc0574dbfbd08fa"
SESSION = requests.Session() # Garde la même session pour les requêtes (+ rapide)


def _format_search_query(query):
    return query.replace(" ", "+")


def get_movie_by_id(id):
    r = SESSION.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={_API_KEY}")
    return PartialMovie.from_dict(r.json())


def search_movie(query):
    """Retourne le premier résultat, le plus pertinent, ou None s'il n'y a pas de résultat"""
    r = SESSION.get(f"https://api.themoviedb.org/3/search/movie?api_key={_API_KEY}&query={_format_search_query(query)}")
    results = r.json()["results"]

    if len(results):
        id = results[0]["id"]
        return get_movie_by_id(id)
    else:
        return None


def main():
    print("Exemple de lien d'API :")
    r = SESSION.get(
        f"https://api.themoviedb.org/3/movie/550?api_key={_API_KEY}")

    print(PartialMovie.from_dict(r.json()))
    print()

    print("Infos d'un film grâce à son id :")

    print(get_movie_by_id(75780))
    print()

    print("Infos d'un film qui existe grâce à une recherche :")

    print(search_movie("Collateral Damage"))


    print("Infos d'un film qui n'existe pas grâce à une recherche :")

    print(search_movie("Film qui n'existe pas"))


    print("Genres d'un film grâce à son id :")

    id = 9884
    movie1 = get_movie_by_id(id)

    print(f"Id {id} : genres : {movie1.genres}")

    print(movie1.__dict__)


if __name__ == '__main__':
    main()
