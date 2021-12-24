class Movie:
    """Classe décrivant un film"""

    def __init__(self, title, genres, script):
        # TODO : Ajouter les attributs dont on a besoin au fur et à mesure
        self.title = title
        self.genres = genres
        self.script = script

    def __str__(self):
        return self.title