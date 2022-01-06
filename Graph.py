import matplotlib.pyplot as plt
# from networkx.drawing.nx_pydot import write_dot, read_dot
# import networkx as nx
import igraph as ig

# https://networkx.org/documentation/stable/reference/classes/multigraph.html


class Graph():

    INDEX = 0

    @property
    def nodes(self):
        return list(self._graph)

    @property
    def edges(self):
        return self._graph.edges()  

    def __init__(self, graph_dict=None):
        """
            Le graphe peut soit être généré grâce a un dict
        """
        self._graph_dict = graph_dict

        """
        # On nomme la figure pour pouvoir la retrouver ensuite
        self.fig = plt.figure(f"Graph_{self.INDEX}")
        self.INDEX += 1

        if self._graph_dict is not None:
            self._graph = nx.Graph()
            self._set_edges()
        """
        edges = [] # liste de tuples (src, dest, poids)
        for word in graph_dict:
            print(f"adding edge for: {word}")
            for other_word in graph_dict[word]:
                edges.append((word, other_word, graph_dict[word][other_word]))


        fig, ax = plt.subplots()

        print("avant graph")
        g = ig.Graph.TupleList(edges, weights=True)
        print("après graph")

        print("avant layout")
        layout = g.layout_lgl() # large graph layout
        print("après layout")
        print("avant plot")
        ig.plot(g, layout=layout, target=ax, vertex_label=list(graph_dict))
        print("après plot")

        print("avant plt.show")
        plt.show()
        print("après plt.show")


    def _set_edges(self):
        """Affecte les arêtes au graphe"""
        # Une liste de tuple de la forme [(sommet1, sommet2, poids) , (...), ...]
        edges = []
        for word in self._graph_dict:
            for other_word in self._graph_dict[word]:
                edges.append((word, other_word, self._graph_dict[word][other_word]))

            # Pour libérer de la mémoire
            # del self._graph_dict[word]

        # return (nodes, edges)
        # Les sommets sont créés automatiquement
        self._graph.add_weighted_edges_from(edges)


    def draw(self):
        """Charge la figure en mémoire"""
        # pour le debug
        from time import perf_counter
        print("début draw")
        print("spring_layout : ", end="") ; t = perf_counter()
        pos = nx.spring_layout(self._graph)
        print(f"{perf_counter() - t}\n")

        print("nx.draw : ", end="") ; t = perf_counter()
        nx.draw(self._graph, pos, with_labels=True, font_weight='bold')
        print(f"{perf_counter() - t}\n")

        print("nx.get_edge_attr : ", end="") ; t = perf_counter()
        edge_weight = nx.get_edge_attributes(self._graph, 'weight')
        print(f"{perf_counter() - t}\n")

        print("nx.draw_networkx_edge_labels : ", end="") ; t = perf_counter()
        nx.draw_networkx_edge_labels(
            self._graph, pos, edge_labels=edge_weight)
        print(f"{perf_counter() - t}\n")
        print("fin draw")

    def show_in_window(self):
        """Affiche le graphe"""
        print("début show_in_window")
        if self._graph is not None:
            self.draw()
            plt.show()
        print("fin show_in_window")

    def save_as_png(self):
        """Sauvegarde le graphe au format png"""
        if self._graph is not None:
            self.draw()
            plt.savefig("graph.png")

    # -----------------------------Ces fonctionnalités nécessitent l'installation de graphviz-----------------------------
    #
    # @staticmethod
    # def import_graph(path):
    #     graph = read_dot(path)
    #     return Graph(graph=graph)
    #
    # def save_as_dot(self):
    #     """
    #         Methode qui sauvegarde le graphe dans le langage dot
    #     """
    #     if self._graph != None:
    #         pos = nx.nx_agraph.graphviz_layout(self._graph)
    #         nx.draw(self._graph, pos=pos)
    #         write_dot(self._graph, 'file.dot')
    #
    # --------------------------------------------------------------------------------------------------------------------


def main():
    # string = "Salut mathieu comment ça va dis donc, parce ce que moi ça va super aujourd'hui mathieu"
    # graph_dict = script_parsing.parse_script(
    #     script_parsing._remove_tags(script_parsing._remove_b_tags(string)))
    # On se repose sur le fait que les dict sauvegardent l'ordre d'insertion depuis 3.7
    # graph_from_dict(graph_dict)
    graph_dict = {
        "salut": {"bonjour": 2, "ok": 3, "prout": 3},
        "bonjour": {"ok": 4},
        "ok": {"prout": 2, "bonjour": 2},
        "prout": {"ok": 5}
    }
    """
    graph = Graph(graph_dict)
    graph.show_in_window()
    """

    # Test d'igraph
    fig, ax = plt.subplots()

    """
    g = ig.Graph(len(graph_dict))

    g.vs["word"] = list(graph_dict) # liste des mots
    g.vs["label"] = g.vs["word"]

    # g.es["weight"] = # liste des poids ?
    """

    # g = ig.Graph(len(graph_dict))

    edges = [] # liste de tuples (src, dest, poids)
    for word in graph_dict:
        for other_word in graph_dict[word]:
            edges.append((word, other_word, float(graph_dict[word][other_word])))

    g = ig.Graph.TupleList(edges, weights=True)

    for e in g.es:
        print(e)

    layout = g.layout_lgl() # large graph layout
    ig.plot(g, layout=layout, target=ax, vertex_label=list(graph_dict))

    plt.show()



if __name__ == "__main__":
    main()
