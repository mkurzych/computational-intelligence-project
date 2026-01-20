from itertools import permutations

def brute_force(graph, source_node=0):

    nodes = list(graph.nodes)
    min_path = None
    min_cost = float('inf')

    for perm in permutations(nodes):
        current_cost = 0
        for i in range(len(perm)):
            current_cost += graph[perm[i]][perm[(i + 1) % len(perm)]]['weight']

        if current_cost < min_cost:
            min_cost = current_cost
            min_path = perm

    index = min_path.index(source_node)
    min_path = min_path[index:] + min_path[:index] + (min_path[index],)
    return min_cost, min_path