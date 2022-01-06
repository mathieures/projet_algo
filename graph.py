import script_parsing
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
import networkx as nx


class Graph():

    def __init__(self, dico={}, graph=None):
        """
            Le graphe peut soit être généré grâce a un dico soit importer via un fichier dot
        """
        self.__dico = dico
        self.__graph = graph

    
    
    def __create_nodes_and_edges(self):
        """
            Methode privée
            Methode qui créé la liste des sommets et des arêtes puis les renvoies sous forme de tuple
        """
        pass

    def create_graph(self):
        """
            Methode qui génére le graphe 
        """
        if self.__dico != {}:
            nodes, edges = self.__create_nodes_and_edges()

            G = nx.MultiGraph()
            G.add_nodes_from(nodes)
            G.add_weighted_edges_from(edges)
            self.__graph = G

    def show_graph(self):
        if self.__graph != None:
            pass
    
    def save_graph_as_dot(self):
        """
            Methode qui sauvegarde le graphe dans le langage dot
        """
        if self.__graph != None:
            pos = nx.nx_agraph.graphviz_layout(self.__graph)
            nx.draw(self.__graph, pos=pos)
            write_dot(self.__graph, 'file.dot')

    def save_graph_as_png(self):
        """
            Methode qui sauvegarde le graphe en png
        """
        if self.__graph != None:
            nx.draw(self.__graph)
            plt.savefig("graph.png")

    @staticmethod
    def import_graph(path):

        return Graph(graph=None)





def graph_from_dict(dico):
    """
        Prend en entrée un dico de mot ainsi que leurs occurences { mot1 : occurences , mot2 : occurences, ... }
        et renvoie le graphe associé (Pour l'instant on va déjà essayer de l'afficher mdr)
    """
    G = nx.MultiGraph()
    # Liste des sommets
    nodes = list(set(dico.keys()))
    # Liste des aretes sous forme de tuple
    edges = []

    # G.add_nodes_from(nodes)

    previousWord = ""
    for word in dico:
        if not(previousWord == ""):
            print((previousWord, word))
            if (previousWord, word) not in edges:
                # G.add_weighted_edge(previousWord,word,1)
                edges.append((previousWord, word, 1))

        previousWord = word

    print(edges)

    G.add_weighted_edges_from(edges)

    pos=nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    edge_weight = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
    plt.show()

    # plt.figure(figsize=(6, 6))

    # pos = nx.spring_layout(G)
    # nx.draw_networkx_nodes(G, pos)
    # nx.draw_networkx_labels(G, pos)

    # for edge in G.edges(data=True):
    #     nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])])

    # plt.show()


def main():
    string = "Salut mathieu comment ça va dis donc, parce ce que moi ça va super aujourd'hui mathieu"
    dico = script_parsing.parse_script(
        script_parsing._remove_tags(script_parsing._remove_b_tags(string)))
    # print(dico)
    # On se repose sur le fait que les dico en python grade en mémoire l'ordre des clés (ce n'est pas un ensemble)
    graph_from_dict(dico)


def test(dico):
    G = nx.MultiDiGraph()
    # Liste des sommets
    nodes = list(set(dico.keys()))
    # Liste des aretes sous forme de tuple
    edges = []

    # G.add_nodes_from(nodes)

    previousWord = ""
    for word in dico:
        if not(previousWord == ""):
            if (previousWord, word) not in edges:
                # G.add_weighted_edge(previousWord,word,1)
                G.add_weighted_edges_from([(previousWord, word, 1)])
                edges.append((previousWord, word))

        previousWord = word

    # pos=nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, font_weight='bold')
    # edge_weight = nx.get_edge_attributes(G,'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
    # plt.show()

    plt.figure(figsize=(6, 6))

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)

    for edge in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])])

    plt.show()


if __name__ == "__main__":
    main()
    # test()
