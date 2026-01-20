import networkx as nx
import random
import matplotlib.pyplot as plt

class Generator:
    def __init__(self, nodes):
        self.graph = self.generate(nodes)

    def generate_weights(self):
        for (u, v) in self.graph.edges:
            rand = random.randint(1, 10)
            self.graph.edges[u, v]['weight'] = rand

    def check_triangle_sides_condition(self):
        for clique in nx.enumerate_all_cliques(self.graph):
            if len(clique) == 3:
                u, v, w = clique
                if (self.graph[u][v]['weight'] + self.graph[u][w]['weight'] < self.graph[v][w]['weight'] or
                        self.graph[u][v]['weight'] + self.graph[v][w]['weight'] < self.graph[u][w]['weight'] or
                        self.graph[u][w]['weight'] + self.graph[v][w]['weight'] < self.graph[u][v]['weight']):
                    return False
        return True

    def generate(self, nodes):
        self.graph = nx.complete_graph(nodes)
        self.generate_weights()
        while not self.check_triangle_sides_condition():
            self.generate_weights()
        return self.graph


def plot_graph(graph, path=None):
    pos = nx.shell_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, "weight")

    edge_colors = ['red' if path and ((u, v) in path or (v, u) in path) else 'black' for u, v in
                   graph.edges(data=False)]

    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(graph, pos)
    plt.show()