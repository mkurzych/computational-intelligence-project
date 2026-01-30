def nearest_neighbour(graph, start):
    visited = set()
    path = []
    current = start
    weight = 0

    while len(visited) < len(graph):
        visited.add(current)
        path.append(current)

        nearest = None
        nearest_distance = float('inf')

        for neighbour in graph[current].keys():
            if neighbour not in visited and graph[current][neighbour]['weight'] < nearest_distance:
                nearest = neighbour
                nearest_distance = graph[current][neighbour]['weight']

        if nearest is None:
            break

        current = nearest
        weight += nearest_distance

    weight += graph[current][start]['weight']
    index = path.index(start)
    path = path[index:] + path[:index] + [path[index]]

    return weight, path