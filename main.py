from generator import Generator
from christofides import christofides
from brute_force import brute_force
from nearest_neighbour import nearest_neighbour
from genetic import genetic
from ant_colony import ant_colony
import time

nodes = 7
gen = Generator(nodes)
graph = gen.graph

source_node = 0

print("+++ Using Brute Force Algorithm +++")
start_time = time.time()
weight, path = brute_force(graph)
elapsed_time = time.time() - start_time
print("Approximate TSP path:", path)
print("Total weight of the path:", weight)
print(f"  ✓ Completed in {elapsed_time:.4f}s")

print()

print("+++ Using Christofides Algorithm +++")
start_time = time.time()
weight, path = christofides(graph, source_node)
elapsed_time = time.time() - start_time
print("Approximate TSP path:", path)
print("Total weight of the path:", weight)
print(f"  ✓ Completed in {elapsed_time:.4f}s")

print()

print("+++ Using Nearest Neighbour Heuristic +++")
start_time = time.time()
weight, path = nearest_neighbour(graph, source_node)
elapsed_time = time.time() - start_time
print("Approximate TSP path:", path)
print("Total weight of the path:", weight)
print(f"  ✓ Completed in {elapsed_time:.4f}s")

print()

print("+++ Using Genetic Algorithm +++")
start_time = time.time()
weight, path = genetic(graph, source_node)
elapsed_time = time.time() - start_time
print("Approximate TSP path:", path)
print("Total weight of the path:", weight)
print(f"  ✓ Completed in {elapsed_time:.4f}s")

print()

print("+++ Using Ant Colony Optimization +++")
start_time = time.time()
weight, path = ant_colony(graph, source_node)
elapsed_time = time.time() - start_time
print("Approximate TSP path:", path)
print("Total weight of the path:", weight)
print(f"  ✓ Completed in {elapsed_time:.4f}s")
