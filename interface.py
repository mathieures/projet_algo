import tkinter as tk
import matplotlib.pyplot as plt
from Graph import Graph

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



class Interface:
    """Interface complète à instancier"""

    @property
    def nb_panels(self):
        return len(self._panels)


    def __init__(self, nb_panels, graph_dict):
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

        # Crée une liste de taille `nb_panels` contenant des objets Panel
        self._panels = []
        for _ in range(nb_panels):
            self.add_panel()


        self._root.mainloop() # Bloquant


    def add_panel(self):
        """Ajoute un Panel à l'interface"""
        new_panel = Panel(self._root, self._graph_dict)
        self._panels.append(new_panel)
        new_panel.pack()


class Panel(tk.Frame):
    """
    Classe décrivant un "panneau", élément de l'interface qui contient :
    # TODO : remplir la docstring avec ce qu'il y a dans un Panel
    """
    def __init__(self, parent_frame, graph_dict):
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

        self.graph = Graph(dict_=graph_dict)
        self.plot_graph()

    def pack(self):
        """Écrase la méthode `pack()` des tk.Frame"""
        super().pack(side=tk.LEFT) # Les panneaux seront pack de gauche à droite
        # pack les autres éléments aussi je pense


    def plot_graph(self):
        # https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html#
        print("Plot du graphe (plot_graph)")
        self.graph.create_graph()
        self.graph.show_graph()
        graph_fig = self.graph.fig
        self._canvas = FigureCanvasTkAgg(graph_fig, master=self)
        # tk.Canvas(self, width=150, height=150, bg="red")
        self._canvas.get_tk_widget().pack(side=tk.BOTTOM)

        toolbar = NavigationToolbar2Tk(self._canvas, self)
        toolbar.pack(side=tk.BOTTOM)
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

    nb_panels = 1
    interface = Interface(nb_panels) # bloquant


if __name__ == '__main__':
    main()
