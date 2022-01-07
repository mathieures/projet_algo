from bs4 import BeautifulSoup
import requests
import json


class PartialMovie:
    """
    Classe décrivant un film dont nous n'avons
    pas encore récolté toutes les informations
    """

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
            genres=dict_.get("genres"),
            # genres=cls._get_genres_from_dict(dict_),
            id=dict_.get("id"),
            note=dict_.get("vote_average"),
            title=dict_.get("title"),
            script=dict_.get("script"),
            movie_url=dict_.get("movie_url")
        ) if dict_ is not None else None

    def __init__(self,
                 budget=None,
                 date=None,
                 duration=None,
                 genres=None,
                 id=None,
                 movie_url=None,
                 note=None,
                 title=None,
                 script=None):
        self.budget = budget
        self.date = date
        self.duration = duration
        self.genres = genres
        self.id = id
        self.movie_url = movie_url
        self.note = note
        self.title = title
        self.script = script # objet Script

    def __repr__(self):
        """Affiche les informations du film"""
        string = ", ".join(f"{key}: {self.__dict__[key]}" for key in self.__dict__)
        return f"<{type(self).__name__}: {string}>"

    def __str__(self):
        """
        Utilisé par tkinter pour l'affichage. On sait que cela n'arrive
        qu'à un seul moment, donc on peut lui donner un sens.
        """
        return "[Informations indisponibles]"


class Movie(PartialMovie):
    """
    Classe pour un résultat après l'appel aux API's,
    qui contient toutes les informations utiles après
    le traitement du script.
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
            movie_url=pm.movie_url,
            note=pm.note,
            title=pm.title,
            script=pm.script
        )

    @classmethod
    def merge_into_Movie(cls, *partial_movies):
        """
        Fusionne plusieurs objets PartialMovie
        en un Movie s'ils sont suffisants
        """
        temp = PartialMovie()
        for pm in partial_movies:
            if isinstance(pm, PartialMovie):
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
                 movie_url,
                 note,
                 title,
                 script):
        super().__init__(
            budget=budget,
            date=date,
            duration=duration,
            genres=genres,
            id=id,
            movie_url=movie_url,
            note=note,
            title=title,
            script=script) # objet Script

    def __str__(self):
        """
        Transforme les attributs de la classe
        en une chaîne de caractères formatée
        """
        return "\n".join([f"Budget : {self.budget}",
                          f"Date : {self.date}",
                          f"Duration : {self.duration}",
                          f"Genres : {', '.join(self.genres)}",
                          f"Note : {self.note}"])


def main():
    pass
    # TODO : écrire des tests


if __name__ == '__main__':
    main()
