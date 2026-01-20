from generator import Generator, plot_graph
from christofides.christofides import christofides
from brute_force.brute_force import brute_force
from nearest_neighbour.nearest_neighbour import nearest_neighbour


nodes = 6
gen = Generator(nodes)
graph = gen.graph

source_node = 0

print("+++ Using Brute Force Algorithm +++")
weight, path = brute_force(graph)
print("Approximate TSP path:", path)
print("Total weight of the path:", weight)
plot_graph(graph, path=[(path[i], path[i + 1]) for i in range(len(path) - 1)] + [(path[-1], path[0])])

print()

print("+++ Using Christofides Algorithm +++")
weight, path = christofides(graph, source_node)
print("Approximate TSP path:", path)
print("Total weight of the path:", weight)
plot_graph(graph, path=[(path[i], path[i + 1]) for i in range(len(path) - 1)] + [(path[-1], path[0])])

print()

print("+++ Using Nearest Neighbour Heuristic +++")
weight, path = nearest_neighbour(graph, source_node)
print("Approximate TSP path:", path)
print("Total weight of the path:", weight)
plot_graph(graph, path=[(path[i], path[i + 1]) for i in range(len(path) - 1)] + [(path[-1], path[0])])

