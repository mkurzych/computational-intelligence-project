import time
import csv
from datetime import datetime
from generator import Generator
from christofides.christofides import christofides
from brute_force.brute_force import brute_force
from nearest_neighbour.nearest_neighbour import nearest_neighbour
from genetic.genetic import genetic
from ant_colony.ant_colony import ant_colony


def run_algorithm(name, algorithm_func, graph, source_node=0):
    try:
        start_time = time.time()
        weight, path = algorithm_func(graph, source_node) if source_node is not None else algorithm_func(graph)
        execution_time = time.time() - start_time
        return execution_time, weight, path

    except Exception as e:
        print(f"  Error running {name}: {e}")
        return None, None, None


def benchmark_graph(graph_num, num_nodes, source_node=0):
    print(f"\n{'='*70}")
    print(f"Graph #{graph_num + 1}")
    print(f"{'='*70}")

    # generate graph
    gen = Generator(num_nodes)
    graph = gen.graph

    results = {
        'graph_num': graph_num + 1,
        'num_nodes': num_nodes,
    }

    # run brute force (only for small graphs)
    if num_nodes < 10:
        print("Running Brute Force...", end=" ", flush=True)
        exec_time, weight, path = run_algorithm("Brute Force", brute_force, graph, source_node)
        if exec_time is not None:
            print(f"Done in {exec_time:.4f}s, weight: {weight}")
            results['brute_force_time'] = exec_time
            results['brute_force_weight'] = weight
        else:
            print("Failed")
            results['brute_force_time'] = None
            results['brute_force_weight'] = None
    else:
        print("Skipping Brute Force (too large)")
        results['brute_force_time'] = None
        results['brute_force_weight'] = None


    # run christofides
    print("Running Christofides...", end=" ", flush=True)
    exec_time, weight, path = run_algorithm("Christofides", christofides, graph, source_node)
    if exec_time is not None:
        print(f"Done in {exec_time:.4f}s, weight: {weight}")
        results['christofides_time'] = exec_time
        results['christofides_weight'] = weight
    else:
        print("Failed")
        results['christofides_time'] = None
        results['christofides_weight'] = None

    # run nearest neighbour
    print("Running Nearest Neighbour...", end=" ", flush=True)
    exec_time, weight, path = run_algorithm("Nearest Neighbour", nearest_neighbour, graph, source_node)
    if exec_time is not None:
        print(f"Done in {exec_time:.4f}s, weight: {weight}")
        results['nearest_neighbour_time'] = exec_time
        results['nearest_neighbour_weight'] = weight
    else:
        print("Failed")
        results['nearest_neighbour_time'] = None
        results['nearest_neighbour_weight'] = None

    # run genetic algorithm
    print("Running Genetic Algorithm...", end=" ", flush=True)
    exec_time, weight, path = run_algorithm("Genetic Algorithm", genetic, graph, source_node)
    if exec_time is not None:
        print(f"Done in {exec_time:.4f}s, weight: {weight}")
        results['genetic_time'] = exec_time
        results['genetic_weight'] = weight
    else:
        print("Failed")
        results['genetic_time'] = None
        results['genetic_weight'] = None

    # run ant colony optimization
    print("Running Ant Colony Optimization...", end=" ", flush=True)
    exec_time, weight, path = run_algorithm("Ant Colony", ant_colony, graph, source_node)
    if exec_time is not None:
        print(f"Done in {exec_time:.4f}s, weight: {weight}")
        results['ant_colony_time'] = exec_time
        results['ant_colony_weight'] = weight
    else:
        print("Failed")
        results['ant_colony_time'] = None
        results['ant_colony_weight'] = None

    return results


def run_benchmark(num_graphs=50, num_nodes=10):
    print("="*70)
    print("TSP ALGORITHMS BENCHMARK")
    print("="*70)
    print(f"Number of graphs: {num_graphs}")
    print(f"Nodes per graph: {num_nodes}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    all_results = []

    # run benchmark on each graph
    for i in range(num_graphs):
        results = benchmark_graph(i, num_nodes)
        all_results.append(results)

    # save results to CSV
    csv_filename = f"benchmark_results_{num_nodes}.csv"

    print(f"\n{'='*70}")
    print(f"Saving results to {csv_filename}...")

    fieldnames = [
        'graph_num', 'num_nodes',
        'brute_force_time', 'brute_force_weight',
        'christofides_time', 'christofides_weight',
        'nearest_neighbour_time', 'nearest_neighbour_weight',
        'genetic_time', 'genetic_weight',
        'ant_colony_time', 'ant_colony_weight'
    ]

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"✓ Results saved to {csv_filename}")


if __name__ == "__main__":
    run_benchmark(num_graphs=100, num_nodes=5)
    run_benchmark(num_graphs=100, num_nodes=6)
    run_benchmark(num_graphs=100, num_nodes=7)
    run_benchmark(num_graphs=100, num_nodes=8)
    run_benchmark(num_graphs=100, num_nodes=9)
    run_benchmark(num_graphs=100, num_nodes=10)
    run_benchmark(num_graphs=100, num_nodes=12)
    run_benchmark(num_graphs=100, num_nodes=13)
    run_benchmark(num_graphs=100, num_nodes=15)
    run_benchmark(num_graphs=100, num_nodes=17)
    run_benchmark(num_graphs=100, num_nodes=18)
    run_benchmark(num_graphs=100, num_nodes=20)
    run_benchmark(num_graphs=100, num_nodes=22)
    run_benchmark(num_graphs=100, num_nodes=23)
    run_benchmark(num_graphs=100, num_nodes=25)
    run_benchmark(num_graphs=100, num_nodes=27)
    run_benchmark(num_graphs=100, num_nodes=28)
    run_benchmark(num_graphs=100, num_nodes=30)




