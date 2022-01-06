import script_parsing
import networkx as nx
import matplotlib.pyplot as plt


def graph_from_dict(dico):
    """
        Prend en entrée un dico de mot ainsi que leurs occurences { mot1 : occurences , mot2 : occurences, ... }
        et renvoie le graphe associé (Pour l'instant on va déjà essayer de l'afficher mdr)
    """
    G = nx.DiGraph()
    # Liste des sommets
    nodes = list(set(dico.keys()))
    # Liste des aretes sous forme de tuple
    edges = []

    # G.add_nodes_from(nodes)

    previousWord = ""
    for word in dico:
        if not(previousWord == ""):
            if (previousWord,word) not in edges:
                # G.add_weighted_edge(previousWord,word,1)
                G.add_weighted_edges_from([(previousWord,word,1)])
                edges.append((previousWord,word))
        
        previousWord = word
        
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True)
    edge_weight = nx.get_edge_attributes(G,"weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weight)
    plt.show()


def main():
    string = "Salut mathieu comment ça va dis donc, parce ce que moi ça va super aujourd'hui mathieu"
    dico = script_parsing.parse_script(script_parsing.cleanString(string))
    print(dico)
    graph_from_dict(dico)

def test():
    G = nx.Graph() 
    E = [('A', 'B', 2), ('A', 'C', 1), ('B', 'D', 5), ('B', 'E', 3), ('C', 'E', 2)]
    G.add_weighted_edges_from(E)
    pos=nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    edge_weight = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
    plt.show()

if __name__ == "__main__":
    main()
    # test()
