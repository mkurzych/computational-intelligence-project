import networkx as nx


def build_multigraph(tree, matching, graph):
    h = nx.MultiGraph(tree)
    for u, v in matching:
        h.add_edge(u, v, weight=graph[u][v]['weight'])
    return h


def find_minimal_matching(graph, odd_nodes):
    subgraph = nx.Graph()
    for i in range(len(odd_nodes)):
        for j in range(1, len(odd_nodes)):
            u, v = odd_nodes[i], odd_nodes[j]
            if graph.has_edge(u, v):
                subgraph.add_edge(u, v, weight=graph[u][v]['weight'])
    return nx.min_weight_matching(subgraph, weight='weight')


def christofides(graph, source):

    t = nx.minimum_spanning_tree(graph)

    odd_nodes = []
    for node in t.nodes:
        if t.degree(node) % 2 != 0:
            odd_nodes.append(node)

    m = find_minimal_matching(graph, odd_nodes)
    h = build_multigraph(t, m, graph)

    eulerian = list(nx.eulerian_circuit(h))
    visited = set()
    path = []
    for u, v in eulerian:
        if u not in visited:
            path.append(u)
            visited.add(u)
        if v not in visited:
            path.append(v)
            visited.add(v)

    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    path_edges.append((path[-1], path[0]))
    weight = 0
    for edge in path_edges:
        weight += graph[edge[0]][edge[1]]['weight']

    if source in path:
        start_index = path.index(source)
        path = path[start_index:] + path[:start_index] + [source]

    return weight, path

