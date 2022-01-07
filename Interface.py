import tkinter as tk
import matplotlib.pyplot as plt
from Graph import Graph

from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


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
        self._root.title("Visualisation de graphe")

        # Cadre du bas
        self._bottom_frame = tk.Frame(self._root)
        self._bottom_frame.pack(side=tk.BOTTOM, anchor="se")  # En bas à droite

        # Bouton pour ajouter un panneau
        self._add_panel_button = tk.Button(self._bottom_frame, text="Ajouter un panneau",
                                           command=self.add_panel)
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

        self._root.mainloop()  # Bloquant

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
        super().pack(side=tk.LEFT)  # Les panneaux seront pack de gauche à droite


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
            # __str__ est modifiée dans Movie
            tk.Label(lf, text=str(movie)).pack()
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

        # Menu "Fichier"
        self._menu_frame = tk.Frame(self._top_frame)
        self._menu_frame.pack(anchor="w", side=tk.LEFT, expand=True, fill=tk.X)

        self._file_menu = tk.Menubutton(
            self._menu_frame,
            text="Fichier",
            relief="raised")

        self._file_sub_menu = tk.Menu(self._file_menu, tearoff=False)
        self._file_sub_menu.add_command(label="Importer (pickle)",
                                        command=self._import_graph_from_pickle)
        self._file_sub_menu.add_command(label="Exporter (pickle)",
                                        command=self._export_graph_to_pickle)

        self._file_menu.config(menu=self._file_sub_menu)
        self._file_menu.pack(side=tk.LEFT)

        # Bouton pour supprimer un GraphPanel
        self._destroy_button = tk.Button(self._menu_frame, text="Fermer le panneau",
                                         command=self.destroy)
        self._destroy_button.pack(side="left")

        # Zone de filtre (à droite)
        self._filter_frame = tk.Frame(self._menu_frame)
        self._filter_frame.pack(side="right")

        self._filter_text = tk.StringVar()
        self._filter_text.set("Filtrer par poids")
        self._filter_entry = tk.Entry(
            self._filter_frame, width=20, textvariable=self._filter_text)
        self._filter_entry.pack(side="top")
        self._filter_button = tk.Button(
            self._filter_frame, text="Ok", command=self._filter_action)
        self._filter_button.pack(expand=True, fill="x")

        self._filter_entry.bind("<Button-1>", self._clear_filter_entry)

        # Zone de recherche (à gauche)
        self._search_frame = tk.Frame(self._menu_frame)
        self._search_frame.pack(side="right")

        self._search_text = tk.StringVar()
        self._search_text.set("Rechercher un mot")
        self._search_entry = tk.Entry(
            self._search_frame, width=20, textvariable=self._search_text)
        self._search_entry.pack(side="top")
        self._search_button = tk.Button(
            self._search_frame, text="Ok", command=self._search_action)
        self._search_button.pack(expand=True, fill="x")

        self._search_entry.bind("<Button-1>", self._clear_search_entry)

        # Canvas
        self._canvas = None
        self._toolbar = None

        self.graph = Graph.from_dict(graph_dict)
        # self._sub_graph va garder en memoire le sous graphe d'une recherche de mot
        self._sub_graph = None
        self.plot_graph()

    def plot_graph(self, graph=None):
        # Grâce à : https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html#
        if graph is None:
            graph = self.graph

        # On enlève ce qui était présent
        self.clear_graph()

        print("Plot du graphe (plot_graph)")
        graph_fig = graph.fig
        graph.draw()
        self._canvas = FigureCanvasTkAgg(graph_fig, master=self)
        # tk.Canvas(self, width=150, height=150, bg="red")
        self._canvas.get_tk_widget().pack(side=tk.BOTTOM)

        self._toolbar = NavigationToolbar2Tk(self._canvas, self)
        self._toolbar.pack(side=tk.BOTTOM)
        self._canvas.draw()

    def clear_graph(self):
        """Détruit les widgets contenant le graphe, le supprimant en même temps"""
        if self._canvas is not None:
            self._canvas.get_tk_widget().destroy()
            self._toolbar.destroy()


    def _filter_action(self):
        weight = self._filter_text.get()
        # Si l'input n'est pas nul
        if weight:
            if weight.isnumeric():
                # Si une recherche était en cours, on applique le filtre dessus
                if self._sub_graph is not None:
                    sub_graph = self._sub_graph.weight_filter(int(weight))
                else:
                    sub_graph = self.graph.weight_filter(int(weight))
                # Si on a bien affecté sub_graph, on le plot
                if sub_graph is not None:
                    self.plot_graph(sub_graph)
                # Sinon on le signale
                else:
                    self._filtre_text.set("Poids introuvable")
            else:
                self._filtre_text.set("Ce n'est pas un nombre")
        # Sinon on affiche tout
        else:
            if self._sub_graph is not None:
                self.plot_graph(self._sub_graph)
            else:
                self.plot_graph()
            self._filter_text.set("Filtrer par poids")

    def _search_action(self):
        node = self._search_text.get()
        # Si l'input n'est pas nul
        if node:
            self._sub_graph = self.graph.get_sub_graph(node)
            if self._sub_graph is not None:
                self.plot_graph(self._sub_graph)
            else:
                self._search_text.set("Mot introuvable")
        # Sinon on affiche tout
        else:
            self._search_text.set("Rechercher un mot")
            self.plot_graph()
            self._sub_graph = None

    def _clear_search_entry(self, event):
        """
        Efface le contenu de la case s'il y a plusieurs mots (permet
        d'efface "Rechercher un mot" et "Mot introuvable" entre autres)
        """
        if len(self._search_text.get().split()) > 1:
            self._search_text.set("")

    def _clear_filter_entry(self, event):
        """
        Efface le contenu de la case s'il y a plusieurs mots (permet
        d'efface "Filtrer un poids" et "Ce n'est pas un nombre" entre autres)
        """
        if len(self._filter_text.get().split()) > 1:
            self._filter_text.set("")


    def _import_graph_from_pickle(self, event=None):
        ext = ""
        filename = filedialog.askopenfilename(
            defaultextension=".pickle",
            filetypes=(("Fichiers pickle (*.pickle)", ".pickle"), ("Tous les fichiers", ".*")))
        if filename:
            self.graph = Graph.from_pickle(filename)
            self.plot_graph()

    def _export_graph_to_pickle(self, event=None):
        # On demande a l'utilisateur dans quel fichier il veut sauver le graphe
        filename = filedialog.asksaveasfilename(
            defaultextension=".pickle",
            filetypes=(("Fichiers pickle (*.pickle)", ".pickle"), ("Tous les fichiers", ".*"))
        )
        # Si l'utilisateur a annulé ou fermé la fenêtre
        if not filename:
            return
        try:
            self.graph.save_as_pickle(filename)
        except FileNotFoundError:
            messagebox.showerror(
                title="Error",
                message="Erreur : fichier non trouvé"
            )
        except IOError:
            messagebox.showerror(
                title="Error",
                message="Le fichier n'existe pas"
            )


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
    interface = Interface(nb_graph_panels)  # bloquant


if __name__ == '__main__':
    main()
