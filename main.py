from generator import Generator, plot_graph
from christofides.christofides import christofides


nodes = 6
gen = Generator(nodes)
graph = gen.graph

source_node = 0
weight, path = christofides(graph, source_node)

print("Approximate TSP path:", path)
print("Total weight of the path:", weight)

plot_graph(graph, path=[(path[i], path[i + 1]) for i in range(len(path) - 1)] + [(path[-1], path[0])])