import tkinter as tk
from tkinter import ttk


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
        # TODO : récupérer les scripts des films sélectionnés


def main():
    """
    Simulation de ce qu'un script regroupant la
    récupération des données et l'affichage ferait
    """

    import imsdb_api
    
    # Récupération des données sur le site de scénarios
    data = imsdb_api.getName()

    # On extraie seulement les genres et les titres pour le test
    movies_by_genre = { genre: list(data[genre]) for genre in data }

    nb_panels = 2
    interface = Interface(nb_panels, movies_by_genre) # bloquant


if __name__ == '__main__':
    main()
