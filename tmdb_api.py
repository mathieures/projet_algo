import requests
import json


_API_KEY = "dd6b80f1beb24a174bc0574dbfbd08fa"

class TMDB_Movie:
    """
    Classe pour un résultat de l'API TMDB, qui
    n'a pas les mêmes informations qu'un Movie
    """

    @staticmethod
    def _get_genres_from_dict(dict_):
        """
        Retourne une liste des genres sous forme de str, car
        l'API ne nous les fournit pas sous une forme exploitable
        """
        return [genre["name"] for genre in dict_["genres"]]

    @classmethod
    def from_dict(cls, dict_):
        """
        Construit un objet TMDB_Movie grâce à un
        dictionnaire (résultat json d'une requête)
        """
        return cls(
            budget=dict_["budget"],
            genres=cls._get_genres_from_dict(dict_),
            id=dict_["id"],
            date=dict_["release_date"],
            duration=dict_["runtime"],
            title=dict_["title"],
            note=dict_["vote_average"]
        )

    def __init__(self, budget=None, genres=None, id=None, date=None, duration=None, title=None, note=None):
        """Ajouter les attributs dont on a besoin au fur et à mesure"""
        self.budget = budget
        self.genres = genres
        self.id = id
        self.date = date
        self.duration = duration
        self.title = title
        self.note = note

    def __str__(self):
        """Transforme les attributs de la classe en une chaîne de caractères formatée"""
        return json.dumps(self.__dict__, indent=4)


def _format_search_query(query):
    return "+".join(query.split(" "))


def get_movie_by_id(id):
    r = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={_API_KEY}")
    return TMDB_Movie.from_dict(r.json())


def search_movie(query):
    """Retourne le premier résultat, le plus pertinent, ou None s'il n'y a pas de résultat"""
    r = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={_API_KEY}&query={_format_search_query(query)}")
    results = r.json()["results"]

    if len(results):
        id = results[0]["id"]
        return get_movie_by_id(id)
    else:
        return None


def main():
    print("Exemple de lien d'API :")
    r = requests.get(
        f"https://api.themoviedb.org/3/movie/550?api_key={_API_KEY}")

    print(TMDB_Movie.from_dict(r.json()))
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


if __name__ == '__main__':
    main()
