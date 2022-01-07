import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot, read_dot
import networkx as nx
import igraph as ig
import pickle

# https://networkx.org/documentation/stable/reference/classes/multigraph.html


class Graph():

    INDEX = 0

    @property
    def nodes(self):
        return list(self._graph)

    @property
    def edges(self):
        return self._graph.edges()

    @classmethod
    def from_dict(cls, graph_dict):
        g = cls()
        g._graph = nx.Graph()
        g._graph_dict = graph_dict
        g._set_edges()
        return g

    @classmethod
    def from_nx_graph(cls, nx_graph):
        g = cls()
        g._graph = nx_graph
        return g

    @classmethod
    def from_pickle(cls, filename):
        raise NotImplementedError

    def __init__(self):
        """
            Le graphe peut soit être généré grâce a un dict
        """
        # self._graph_dict = graph_dict
        print(f"### Index: {Graph.INDEX}")
        Graph.INDEX += 1

        # On nomme la figure pour pouvoir la retrouver ensuite
        self.fig = plt.figure(num=f"Graph_{Graph.INDEX}")

        # if self._graph_dict is not None:
        #     self._graph = nx.Graph()
        #     self._set_edges()
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
        """

    def _set_edges(self):
        """Affecte les arêtes au graphe"""
        # Une liste de tuple de la forme [(sommet1, sommet2, poids) , (...), ...]
        # Un ensemble pour ne pas avoir de doublons
        weights_dict = {}
        for word in self._graph_dict:
            for other_word in self._graph_dict[word]:
                edge = [word, other_word]  # src, dest
                weight = self._graph_dict[word][other_word]
                # On trie la source et la destination par ordre croissant
                if edge[0] > edge[1]:
                    edge[0], edge[1] = edge[1], edge[0]
                edge = tuple(edge)
                if edge not in weights_dict:
                    weights_dict[edge] = weight

        edges = [(edge[0], edge[1], weights_dict[edge])
                 for edge in weights_dict]
        weights_dict.clear()

        # Les sommets sont créés automatiquement
        self._graph.add_weighted_edges_from(edges)

    def draw(self):
        """Charge la figure en mémoire"""
        # pour le debug
        from time import perf_counter
        print("début draw")
        print("spring_layout : ", end="")
        t = perf_counter()
        pos = nx.spring_layout(self._graph)
        print(f"{perf_counter() - t}\n")

        print("nx.draw : ", end="")
        t = perf_counter()
        nx.draw(self._graph, pos, with_labels=True,
                font_weight='bold', font_size=8)
        print(f"{perf_counter() - t}\n")

        print("nx.get_edge_attr : ", end="")
        t = perf_counter()
        edge_weight = nx.get_edge_attributes(self._graph, 'weight')
        print(f"{perf_counter() - t}\n")

        print("nx.draw_networkx_edge_labels : ", end="")
        t = perf_counter()
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

    def save_as_pickle(self):
        if self._graph is not None:
            nx.write_gpickle(self._graph, "graph.gpickle")

    def import_from_pickle(self, path):
        try:
            self._graph = nx.read_gpickle(path)
        except:
            print("[Errur] Le chemin du fichier est invalide")

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
    # On se repose sur le fait que les dict sauvegardent l'ordre d'insertion depuis Python 3.7
    graph_dict = {
        "salut": {"bonjour": 2, "ok": 3, "prout": 3},
        "bonjour": {"ok": 4},
        "ok": {"prout": 2, "bonjour": 2},
        "prout": {"ok": 5}
    }
    graph = Graph(graph_dict)
    graph.show_in_window()

    # """
    # Test d'igraph
    fig, ax = plt.subplots()

    g = ig.Graph(len(graph_dict))

    g.vs["word"] = list(graph_dict)  # liste des mots
    g.vs["label"] = g.vs["word"]

    # g.es["weight"] = # liste des poids ?

    # g = ig.Graph(len(graph_dict))

    weights_dict = {}
    for word in graph_dict:
        for other_word in graph_dict[word]:
            edge = [word, other_word]  # src, dest
            weight = graph_dict[word][other_word]
            # On trie la source et la destination par ordre croissant
            if edge[0] > edge[1]:
                edge[0], edge[1] = edge[1], edge[0]
            edge = tuple(edge)
            if edge not in weights_dict:
                weights_dict[edge] = weight

    edges = [(edge[0], edge[1], weights_dict[edge]) for edge in weights_dict]
    weights_dict.clear()

    g = ig.Graph.TupleList(edges, weights=True)

    for e in g.es:
        print(e)

    layout = g.layout_lgl()  # large graph layout
    ig.plot(g, layout=layout, target=ax, vertex_label=list(graph_dict))

    plt.show()
    # """

def test():
    GRAPH_DICT = {
        "salut": {"bonjour": 2, "ok": 3, "prout": 3},
        "bonjour": {"ok": 4},
        "ok": {"prout": 2, "bonjour": 2},
        "prout": {"ok": 5}
    }

    g = Graph(GRAPH_DICT)
    g.save_as_pickle()

if __name__ == "__main__":
    # main()
    test()
