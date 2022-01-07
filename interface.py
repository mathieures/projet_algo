import tkinter as tk


class Interface:
    """Interface complète à instancier"""

    @property
    def nb_panels(self):
        return len(self._panels)


    def __init__(self, nb_panels, movies_by_genre):
        self._movies_by_genre = movies_by_genre

        # Instanciation des éléments graphiques
        self._root = tk.Tk()

        # Cadre du haut
        self._bottom_frame = tk.Frame(self._root)
        self._bottom_frame.pack(side=tk.BOTTOM, anchor="se") # En bas à droite

        # Bouton pour ajouter un panneau
        self._add_panel_button = tk.Button(self._bottom_frame, text="+",
                                           command=self.add_panel, width=2)
        self._add_panel_button.pack()

        # Crée une liste de taille `nb_panels` contenant des objets Panel
        self._panels = []
        for _ in range(nb_panels):
            self.add_panel()


        self._root.mainloop() # Bloquant


    def add_panel(self):
        """Ajoute un Panel à l'interface"""
        new_panel = Panel(self._root)
        self._panels.append(new_panel)
        new_panel.pack()


class Panel(tk.Frame):
    """
    Classe décrivant un "panneau", élément de l'interface qui contient :
    # TODO : remplir la docstring avec ce qu'il y a dans un Panel
    """
    def __init__(self, parent_frame):
        super().__init__(
            parent_frame, bg="#bbb",
            width=500, height=300,
            padx=10, bd=5
        )

        # Cadre du haut
        self._top_frame = tk.Frame(self)
        self._top_frame.pack(side=tk.TOP, anchor="ne")

        # Bouton pour supprimer un Panel
        self._destroy_button = tk.Button(self._top_frame, text="-",
                                         command=self.destroy, width=2)
        self._destroy_button.pack()

        # Canvas où le graphe ira
        # TODO : Modifier les dimensions pour qu'elles soient pratiques
        self._canvas = tk.Canvas(self, width=150, height=150, bg="red")
        self._canvas.pack(side=tk.BOTTOM)


    def pack(self):
        """Écrase la méthode `pack()` des tk.Frame"""
        super().pack(side=tk.LEFT) # Les panneaux seront pack de gauche à droite
        # pack les autres éléments aussi je pense


def main():
    """
    Simulation de ce qu'un script regroupant la
    récupération des données et l'affichage ferait
    """

    """
    import imsdb_api
    
    # Récupération des données sur le site de scénarios
    data = imsdb_api.getName()

    # On extraie seulement les genres et les titres pour le test
    movies_by_genre = { genre: list(data[genre]) for genre in data }
    """
    movies_by_genre = {}

    nb_panels = 1
    interface = Interface(nb_panels, movies_by_genre) # bloquant


if __name__ == '__main__':
    main()
