from bs4 import BeautifulSoup
import requests
import json


class PartialMovie:
    """
    Classe décrivant un film dont nous n'avons
    pas encore récolté toutes les informations
    """

    @staticmethod
    def _get_genres_from_dict(dict_):
        """
        Retourne une liste des genres sous forme de str, car
        l'API ne nous les fournit pas sous une forme exploitable
        """
        # TODO : à supprimer une fois que les genres seront récupérés sur le site des scripts
        return [genre["name"] for genre in dict_["genres"]]

    @classmethod
    def from_dict(cls, dict_):
        """
        Construit un objet PartialMovie grâce à un dictionnaire
        (résultat json d'une requête de tmdb_api ou autre)
        """
        return cls(
            budget=dict_.get("budget"),
            date=dict_.get("release_date"),
            duration=dict_.get("runtime"),
            genres=cls._get_genres_from_dict(dict_), # TODO : à modif une fois _get_genres_from_dict supprimée
            id=dict_.get("id"),
            note=dict_.get("vote_average"),
            title=dict_.get("title"),
            script=dict_.get("script"),
            movie_url=dict_.get("movie_url")
        )

    # @property
    # def script(self):
    #     """
    #     Retourne le script s'il est défini, le
    #     télécharge si non et si un lien est défini
    #     """
    #     if self._script is None and self.movie_url is not None:
    #         self._script = imsdb_api.getScript(self.movie_url)
    #     return self._script

    # @property
    # def genres(self):
    #     """
    #     Retourne les genres du films s'ils sont définis, les récupère si non
    #     """
    #     return self._genres

    def __init__(self,
                 budget=None,
                 date=None,
                 duration=None,
                 genres=None,
                 id=None,
                 note=None,
                 title=None,
                 script=None,
                 movie_url=None):
        self.title = title
        self.genres = genres
        self.movie_url = movie_url
        self.script = script
        self.budget = budget
        self.id = id
        self.date = date
        self.duration = duration
        self.note = note

    def __str__(self):
        return f"{type(self).__name__}: {self.title}"


class Movie(PartialMovie):
    """
    Classe pour un résultat après l'appel aux APIs,
    qui contient toutes les informations utiles,
    prêt pour le traitement du script
    """

    @classmethod
    def from_PartialMovie(cls, pm):
        """Construit un objet Movie à partir d'un PartialMovie"""
        return cls(
            budget=pm.budget,
            date=pm.date,
            duration=pm.duration,
            genres=pm.genres,
            id=pm.id,
            note=pm.note,
            title=pm.title,
            # script=pm.script,
            movie_url=pm.movie_url
        )

    @classmethod
    def merge_into_Movie(cls, *partial_movies):
        """
        Fusionne plusieurs objets PartialMovie
        en un Movie s'ils sont suffisants
        """
        temp = PartialMovie()
        for pm in partial_movies:
            for key, val in pm.__dict__.items():
                if val is not None:
                    temp.__dict__[key] = val
        return cls.from_PartialMovie(temp)

    def __init__(self,
                 budget,
                 date,
                 duration,
                 genres,
                 id,
                 note,
                 title,
                 # script,
                 movie_url):
        super().__init__(
            budget=budget,
            date=date,
            duration=duration,
            genres=genres,
            id=id,
            note=note,
            title=title,
            # script=script,
            movie_url=movie_url)

    def __str__(self):
        """
        Transforme les attributs de la classe
        en une chaîne de caractères formatée
        """
        return f"""{super().__str__()}
               Budget : {self.budget}
               Date : {self.date}
               Duration : {self.duration}
               Genres : {self.genres}
               Note : {self.note}
               Script length: {len(self._script)} characters"""


def main():
    pass
    # TODO : écrire des tests


if __name__ == '__main__':
    main()
