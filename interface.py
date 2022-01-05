import tkinter as tk


class Interface:
    """Interface complète à instancier"""
    def __init__(self, nb_panels, movies_by_genre):
        self._nb_panels = nb_panels
        self._movies_by_genre = movies_by_genre

        # Instanciation des éléments graphiques
        self._root = tk.Tk()

        # Cadre du haut
        self._bottom_frame = tk.Frame(self._root)
        self._bottom_frame.pack(side=tk.BOTTOM, anchor="se") # En bas à droite

        # Bouton pour ajouter un panneau
        self._add_panel_button = tk.Button(self._bottom_frame, text="+", command=self.add_panel)
        self._add_panel_button.pack()

        # Crée une liste de taille `nb_panels` contenant des objets Panel
        self._panels = []
        for _ in range(self._nb_panels):
            self.add_panel()

        for panel in self._panels:
            # Faire ici les trucs à faire pour chaque panneau
            panel.pack()

        self._root.mainloop() # Bloquant


    def add_panel(self):
        self._nb_panels += 1
        new_panel = Panel(
            self._root, bg="#bbb",
            width=500, height=300,
            padx=10, bd=5
        )
        self._panels.append(new_panel)
        new_panel.pack()


class Panel(tk.Frame):
    """
    Classe décrivant un "panneau", élément de l'interface qui contient :
        - Deux listes déroulantes (ttk.Combobox), une pour le genre de film et une pour le titre du film
        - Deux labels (tk.Label), un par liste déroulante pour décrire ce que l'utilisateur doit faire
        - Un bouton (tk.Button) pour valider la sélection
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
