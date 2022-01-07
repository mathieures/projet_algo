import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot, read_dot
import networkx as nx
import igraph as ig
import pickle
from time import perf_counter

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
        """À noter qu'ici le graph_dict n'est pas initialisé"""
        g = cls()
        g._graph = nx_graph
        return g

    @classmethod
    def from_pickle(cls, filename):
        with open(filename, 'rb') as f1:
            OL = pickle.load(f1)
            return OL

    def __init__(self):
        """Un graphe peut être généré grâce aux constructeurs alternatifs"""

        # On nomme la figure pour pouvoir la retrouver ensuite
        self.fig = plt.figure(num=f"Graph_{Graph.INDEX}")
        Graph.INDEX += 1

    def _set_edges(self):
        """Affecte les arêtes au graphe"""
        # Un dictionnaire pour ne pas avoir de doublons
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

        # Une liste de tuple de la forme [(sommet1, sommet2, poids) , (...), ...]
        edges = [(edge[0], edge[1], weights_dict[edge])
                 for edge in weights_dict]
        weights_dict.clear()

        # Les sommets sont créés automatiquement
        self._graph.add_weighted_edges_from(edges)

    def weight_filter(self, weight):
        new_edges = []
        for u, v, w in self._graph.edges(data=True):
            if w["weight"] >= weight:
                new_edges.append((u,v,w["weight"]))
        G = nx.Graph()
        G.add_weighted_edges_from(new_edges)
        return Graph.from_nx_graph(G)

    def draw(self):
        """Charge la figure en mémoire"""
        print("Temps de calcul des étapes d'affichage du graphe :")
        print("Détermination de la disposition : ", end="")
        t = perf_counter()
        pos = nx.spring_layout(self._graph)
        print(f"{perf_counter() - t}\n")

        print("Chargement des sommets et arêtes : ", end="")
        t = perf_counter()
        nx.draw(self._graph, pos, with_labels=True,
                font_weight='bold', font_size=8)
        print(f"{perf_counter() - t}\n")

        print("Affectation des poids : ", end="")
        t = perf_counter()
        edge_weight = nx.get_edge_attributes(self._graph, 'weight')
        print(f"{perf_counter() - t}\n")

        print("Affichage des poids : ", end="")
        t = perf_counter()
        nx.draw_networkx_edge_labels(
            self._graph, pos, edge_labels=edge_weight)
        print(f"{perf_counter() - t}\n")

    def get_sub_graph(self, node):
        """
        Prend en paramètre un sommet (str) et renvoie un sous-graphe
        contenant seulement les sommets liés à celui-ci.
        """
        if node in self._graph_dict:
            return Graph.from_dict({node: self._graph_dict[node]})
        else:
            return None

    def show_in_window(self):
        """Affiche le graphe dans une fenêtre séparée, gérée par matplotlib"""
        if self._graph is not None:
            self.draw()
            plt.show()

    # def save_as_png(self, filename):
    #     """
    #     Sauvegarde le graphe au format png
    #     (déjà implémenté par matplotlib)
    #     """
    #     if self._graph is not None:
    #         self.draw()
    #         plt.savefig(filename)

    def save_as_pickle(self, filename):
        if self._graph is not None:
            with open(filename, "wb") as f:
                pickle.dump(self, f)


    # -----------------------------Ces fonctionnalités nécessitent l'installation de graphviz-----------------------------
    #
    # @staticmethod
    # def import_graph(path):
    #     graph = read_dot(path)
    #     return Graph.from_nx_graph(graph)
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
        "salut": {"bonjour": 2, "ok": 3, "truc": 3},
        "bonjour": {"ok": 4},
        "ok": {"truc": 2, "bonjour": 2},
        "truc": {"ok": 5}
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
        "salut": {"bonjour": 2, "ok": 3, "truc": 3},
        "bonjour": {"ok": 4},
        "ok": {"truc": 2, "bonjour": 2},
        "truc": {"ok": 5}
    }

    g = Graph.from_dict(GRAPH_DICT)
    # g.save_as_pickle()
    # G = Graph.from_pickle("graph.pickle")
    # print(type(g))
    # print(type(G))

    print(g.edges)
    print(g.weight_filter(3).edges)

if __name__ == "__main__":
    # main()
    test()
