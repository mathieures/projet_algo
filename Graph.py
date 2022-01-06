import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot, read_dot
import networkx as nx

# https://networkx.org/documentation/stable/reference/classes/multigraph.html


class Graph():

    @property
    def nodes(self):
        return list(self._graph)

    @property
    def edges(self):
        return self._graph.edges()   

    def __init__(self, graph_dict=None, graph=None):
        """
            Le graphe peut soit être généré grâce a un dict
        """
        self._graph_dict = graph_dict
        self._graph = graph
        if graph is None:
            if self._graph_dict is not None:
                self._graph = nx.Graph()
                self._set_edges()


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


    def _draw(self):
        """Charge la figure en mémoire"""
        pos = nx.spring_layout(self._graph)
        nx.draw(self._graph, pos, with_labels=True, font_weight='bold')
        edge_weight = nx.get_edge_attributes(self._graph, 'weight')
        nx.draw_networkx_edge_labels(
            self._graph, pos, edge_labels=edge_weight)

    def show(self):
        """Affiche le graphe"""
        if self._graph is not None:
            self._draw()
            plt.show()

    def save_as_png(self):
        """Sauvegarde le graphe au format png"""
        if self._graph is not None:
            self._draw()
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


# def graph_from_dict(dico):
#     """
#         Prend en entrée un dico de mot ainsi que leurs occurences { mot1 : occurences , mot2 : occurences, ... }
#         et renvoie le graphe associé (Pour l'instant on va déjà essayer de l'afficher mdr)
#     """
#     G = nx.Graph()
#     # Liste des sommets
#     nodes = list(set(dico.keys()))
#     # Liste des aretes sous forme de tuple
#     edges = []

#     # G.add_nodes_from(nodes)

#     previousWord = ""
#     for word in dico:
#         if not(previousWord == ""):
#             print((previousWord, word))
#             if (previousWord, word) not in edges:
#                 # G.add_weighted_edge(previousWord,word,1)
#                 edges.append((previousWord, word, 1))

#         previousWord = word

#     print(edges)

#     G.add_weighted_edges_from(edges)

#     pos = nx.spring_layout(G)
#     nx.draw(G, pos, with_labels=True, font_weight='bold')
#     edge_weight = nx.get_edge_attributes(G, 'weight')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weight)
#     plt.show()

#     # plt.figure(figsize=(6, 6))

#     # pos = nx.spring_layout(G)
#     # nx.draw_networkx_nodes(G, pos)
#     # nx.draw_networkx_labels(G, pos)

#     # for edge in G.edges(data=True):
#     #     nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])])

#     # plt.show()


def main():
    # string = "Salut mathieu comment ça va dis donc, parce ce que moi ça va super aujourd'hui mathieu"
    # graph_dict = script_parsing.parse_script(
    #     script_parsing._remove_tags(script_parsing._remove_b_tags(string)))
    # On se repose sur le fait que les dict sauvegardent l'ordre d'insertion depuis 3.7
    # graph_from_dict(graph_dict)
    graph_dict = {"salut": {"bonjour": 2, "ok": 3, "prout": 3}, "bonjour": {
        "ok": 4}, "ok": {"prout": 2, "bonjour": 2}, "prout": {"ok": 5}}
    graph = Graph(graph_dict=graph_dict)
    graph.show()


if __name__ == "__main__":
    main()
