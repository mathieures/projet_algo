import tkinter as tk
from tkinter import ttk
from Movie import Movie
import tmdb_api


UNKNOWN_GENRE = "Unknown" # Genre pour les films dont on ne connaît pas le genre


"""
TODO : mettre les récupérations etc dans leur propre script
"""

class Interface:
    """Interface complète à instancier"""
    def __init__(self, nb_panels, movies_by_genre):
        self._nb_panels = nb_panels
        self._movies_by_genre = movies_by_genre

        # Instanciation des éléments graphiques
        self._root = tk.Tk()

        # Crée une liste de taille `nb_panels` contenant des objets Panel
        self._panels = [Panel(
                            self._movies_by_genre, self._root,
                            bg="#bbb", width=200, height=150,
                            padx=10, bd=5
                        ) for _ in range(self._nb_panels)]

        for panel in self._panels:
            # Faire ici les trucs à faire pour chaque panneau
            panel.pack()

        self._root.mainloop() # Bloquant


class Panel(tk.Frame):
    """
    Classe décrivant un "panneau", élément de l'interface qui contient :
        - Deux listes déroulantes (ttk.Combobox), une pour le genre de film et une pour le titre du film
        - Deux labels (tk.Label), un par liste déroulante pour décrire ce que l'utilisateur doit faire
        - Un bouton (tk.Button) pour valider la sélection
    """
    def __init__(self, movies_by_genre, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._movies_by_genre = movies_by_genre

        # Genre
        self._genre_label = tk.Label(self, text="Pick a genre :")
        self._genre_label.pack(side=tk.TOP)

        self._cbb_genre = ttk.Combobox(self, values=list(self._movies_by_genre))
        self._cbb_genre.current(0) # L'élément par défaut sera le 1er
        self._cbb_genre.pack(side=tk.TOP)

        # Action associée à la sélection d'un genre
        self._cbb_genre.bind("<<ComboboxSelected>>", self._update_cbb_movies)


        # Film
        self._movie_label = tk.Label(self, text="Pick a movie :")
        self._movie_label.pack(side=tk.TOP)

        self._cbb_movie = ttk.Combobox(self)
        self._update_cbb_movies()
        self._cbb_movie.current(0) # L'élément par défaut sera le 1er
        self._cbb_movie.pack(side=tk.TOP)


        # Bouton pour valider
        self._ok_button = tk.Button(self, text="Ok", command=self._ok_button_action)
        self._ok_button.pack(side=tk.TOP)

    def pack(self):
        """Écrase la méthode `pack()` des tk.Frame"""
        super().pack(side=tk.LEFT) # Les panneaux seront pack de gauche à droite
        # pack les autres éléments aussi je pense

    def _update_cbb_movies(self, evt=None):
        """
        Le bind fournit un paramètre `evt`
        (évènement), dont nous n'avons pas besoin.
        """
        # print(f"Sélectionné : {self._cbb_genre.get()}")
        self._cbb_movie["values"] = self._movies_by_genre[self._cbb_genre.get()]
        self._cbb_movie.current(0) # L'élément par défaut sera le 1er

    def _ok_button_action(self):
        """Action sur pression du bouton Ok"""
        """
        TODO : Ici seront faites les choses avec les graphes, donc après avoir enlevé les listes déroulantes etc.
        et avoir affiché un Canvas j'imagine, afficher l'image du graphe pour ce film à l'intérieur
        """
        print("Il vient de se passer quelque chose d'incroyable !!")


def main():
    """
    Simulation de ce qu'un script regroupant la
    récupération des données et l'affichage ferait
    """
    # Récupération des données sur le site de scénarios

    # ...

    ### pour le test ###
    data = {
        "John Carter": "http://example.com",
        "Collateral Damage": "http://example.com",
        "Tarzan": "http://example.com"
    }

    # all_movies = [] # Liste de tous les objets Movie
    movies_by_genre = {} # Associe un genre (str) à une liste d'objets Movie

    # Conversion en objets Movie
    for title in data:
        # print(f"Récupération des informations du film : {title}")

        # Récupération du script sur la page html    
        # print(f"Récupération du script")

        ### pour le test ###
        script = "Mathieu: I think Thomas stole my donut\nThomas: No it's Tiphaine I saw her!"

        # Communication avec l'API The Movie DataBase pour connaître les genres du film
        # print(f"Récupération des genres")

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


    nb_panels = 2
    interface = Interface(nb_panels, movies_by_genre) # bloquant


if __name__ == '__main__':
    main()