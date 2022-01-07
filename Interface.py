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
        self._root.title("bg ma gueule")

        # Cadre du bas
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
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            padx=10, bd=5,
            **kwargs
        )

    def pack(self):
        """Écrase la méthode `pack()` de la classe parente"""
        super().pack(side=tk.LEFT) # Les panneaux seront pack de gauche à droite


class InfoPanel(Panel):
    def __init__(self, parent, movies_infos):
        super().__init__(parent)

        # Barre de défilement
        # self._scrollbar = tk.Scrollbar(self, orient="vertical")
        # self._scrollbar.pack(anchor="e", side=tk.RIGHT, fill=tk.Y)
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
    def __init__(self, parent, graph_dict):
        super().__init__(parent, bg="#bbb")

        # Cadre du haut
        self._top_frame = tk.Frame(self)
        self._top_frame.pack(side=tk.TOP, anchor="nw", fill=tk.X)

        # Bouton pour supprimer un GraphPanel
        self._destroy_button = tk.Button(self._top_frame, text="x",
                                         command=self.destroy, width=2)
        self._destroy_button.pack(side=tk.RIGHT)

        # Zone de recherche
        self._search_text = tk.StringVar()
        self._search_text.set("Rechercher un mot")
        self._search_entry = tk.Entry(self._top_frame, width=20, textvariable=self._search_text)
        self._search_entry.pack(side=tk.LEFT)
        self._search_button = tk.Button(self._top_frame, text="Ok", command=self._search_action)
        self._search_button.pack(side="left")

        self._search_entry.bind("<Button-1>", self._clear_search_entry)

        # Canvas
        self._canvas = None
        self._toolbar = None

        self.graph = Graph.from_dict(graph_dict)
        self.plot_graph()


    def plot_graph(self, graph=None):
        # Grâce à : https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html#
        if graph is None:
            graph = self.graph

        # On enlève ce qui était présent
        if self._canvas is not None:
            self._canvas.get_tk_widget().destroy()
            self._toolbar.destroy()
            # self._toolbar.get_tk_widget().destroy()

        print("Plot du graphe (plot_graph)")
        graph_fig = graph.fig
        graph.draw()
        self._canvas = FigureCanvasTkAgg(graph_fig, master=self)
        # tk.Canvas(self, width=150, height=150, bg="red")
        self._canvas.get_tk_widget().pack(side=tk.BOTTOM)

        self._toolbar = NavigationToolbar2Tk(self._canvas, self)
        self._toolbar.pack(side=tk.BOTTOM)
        self._canvas.draw()
        print("Fin du plot")

    def _search_action(self):
        node = self._search_text.get()
        # Si l'input n'est pas nul
        if node != "":
            sub_graph = self.graph.get_sub_graph(node)
            if sub_graph is not None:
                self.plot_graph(sub_graph)
            else:
                self._search_text.set("Mot introuvable")
        # Sinon on affiche tout
        else:
            self.plot_graph()

    def _clear_search_entry(self, evt):
        """
        Efface le contenu de la case s'il y a plusieurs mots (permet
        d'efface "Rechercher un mot" et "Mot introuvable" entre autres)
        """
        if len(self._search_text.get().split()) > 1:
            self._search_text.set("")


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
