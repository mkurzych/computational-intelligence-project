import networkx as nx
import random

class Generator:
    def __init__(self, nodes):
        self.max_edge_retries = 50  # max retries per edge before backtracking
        self.max_node_retries = 10   # max retries per node before removing it
        self.graph = self.generate(nodes)

    def check_triangle_with_edge(self, u, v, weight):
        # for each node w that is connected to both u and v
        for w in self.graph.nodes():
            if w == u or w == v:
                continue

            # check if w is connected to both u and v
            has_uw = self.graph.has_edge(u, w) and 'weight' in self.graph[u][w]
            has_vw = self.graph.has_edge(v, w) and 'weight' in self.graph[v][w]

            if has_uw and has_vw:
                uw = self.graph[u][w]['weight']
                vw = self.graph[v][w]['weight']
                uv = weight

                # check all triangle inequality conditions
                if uv + uw < vw or uv + vw < uw or uw + vw < uv:
                    return False
        return True

    def generate_edge_weight(self, u, v):
        for attempt in range(self.max_edge_retries):
            weight = random.randint(1, 10)
            if self.check_triangle_with_edge(u, v, weight):
                return weight
        return None

    def generate(self, num_nodes):
        self.graph = nx.Graph()

        # add nodes one by one
        for node_idx in range(num_nodes):
            success = self.add_node_with_edges(node_idx)

            if not success:
                # failed to add this node even after retries
                return self.generate(num_nodes)

        return self.graph

    def add_node_with_edges(self, new_node):
        for retry in range(self.max_node_retries):
            self.graph.add_node(new_node)

            # try to connect to all existing nodes
            success = True
            edges_added = []

            for existing_node in range(new_node):
                weight = self.generate_edge_weight(existing_node, new_node)

                if weight is None:
                    # failed to find valid weight for this edge
                    success = False
                    # remove the edges added so far
                    for u, v in edges_added:
                        self.graph.remove_edge(u, v)
                    break
                else:
                    # add edge with valid weight
                    self.graph.add_edge(existing_node, new_node, weight=weight)
                    edges_added.append((existing_node, new_node))

            if success:
                return True

        # failed to add node after all retries
        if self.graph.has_node(new_node):
            self.graph.remove_node(new_node)
        return False