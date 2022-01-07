import tkinter as tk
import matplotlib.pyplot as plt
from Graph import Graph

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class Interface:
    """Interface complète à instancier"""

    @property
    def nb_graph_panels(self):
        return len(self._graph_panels)


    def __init__(self, nb_graph_panels, movies_infos, graph_dict):
        self._movies_infos = movies_infos
        self._graph_dict = graph_dict

        # Instanciation des éléments graphiques
        self._root = tk.Tk()

        # Cadre du haut
        self._bottom_frame = tk.Frame(self._root)
        self._bottom_frame.pack(side=tk.BOTTOM, anchor="se") # En bas à droite

        # Bouton pour ajouter un panneau
        self._add_panel_button = tk.Button(self._bottom_frame, text="+",
                                           command=self.add_panel, width=2)
        self._add_panel_button.pack()

        # InfoPanel
        self._info_panel = InfoPanel(self._root, self._movies_infos)
        self._info_panel.pack()

        # Crée une liste de taille `nb_graph_panels` contenant des objets GraphPanel
        self._graph_panels = []
        for _ in range(nb_graph_panels):
            self.add_panel()

        # Pour gerer la fermeture de la fenetre
        self._root.protocol("WM_DELETE_WINDOW", self._quit_interface)

        self._root.mainloop() # Bloquant


    def add_panel(self):
        """Ajoute un GraphPanel à l'interface"""
        new_panel = GraphPanel(self._root, self._graph_dict)
        self._graph_panels.append(new_panel)
        new_panel.pack()

    def _quit_interface(self):
        exit(1)


class Panel(tk.Frame):
    """Classe décrivant un "panneau", élément de l'interface."""
    def __init__(self, parent_frame, **kwargs):
        super().__init__(
            parent_frame,
            padx=10, bd=5,
            **kwargs
        )

    def pack(self):
        """Écrase la méthode `pack()` de la classe parente"""
        super().pack(side=tk.LEFT) # Les panneaux seront pack de gauche à droite


class InfoPanel(Panel):
    def __init__(self, parent_frame, movies_infos):
        super().__init__(parent_frame)

        # Barre de défilement
        self._scrollbar = tk.Scrollbar(self, orient="vertical")
        self._scrollbar.pack(anchor="e", side=tk.RIGHT, fill=tk.Y)
        # TODO : trouver faire défiler une Frame
        # self.config(yscrollcommand=self._scrollbar.set)
        # self._scrollbar.config(command=self.yview)

        # Cases d'infos
        self._labelframes = []
        # On ajoute un LabelFrame par film, avec comme texte le titre du film
        for movie in movies_infos:
            lf = tk.LabelFrame(self, text=movie.title)
            # On crée un Label contenant les informations du film
            tk.Label(lf, text=str(movie)).pack() # __str__ est modifiée dans Movie
            self._labelframes.append(lf)
        for lf in self._labelframes:
            lf.pack(anchor="n", side=tk.BOTTOM)



class GraphPanel(Panel):
    """Panneau contenant un graphe."""
    def __init__(self, parent_frame, graph_dict):
        super().__init__(parent_frame, bg="#bbb")

        # Cadre du haut
        self._top_frame = tk.Frame(self)
        self._top_frame.pack(side=tk.TOP, anchor="ne")

        # Bouton pour supprimer un GraphPanel
        self._destroy_button = tk.Button(self._top_frame, text="-",
                                         command=self.destroy, width=2)
        self._destroy_button.pack()

        self.graph = Graph(graph_dict)
        self.plot_graph()


    def plot_graph(self):
        # https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html#
        print("Plot du graphe (plot_graph)")
        graph_fig = self.graph.fig
        self.graph.draw()
        Graph.INDEX += 1
        self._canvas = FigureCanvasTkAgg(graph_fig, master=self)
        # tk.Canvas(self, width=150, height=150, bg="red")
        self._canvas.get_tk_widget().pack(side=tk.BOTTOM)

        self._toolbar = NavigationToolbar2Tk(self._canvas, self)
        self._toolbar.pack(side=tk.BOTTOM)
        self._canvas.draw()
        print("Fin du plot")


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

    nb_graph_panels = 1
    interface = Interface(nb_graph_panels) # bloquant


if __name__ == '__main__':
    main()
