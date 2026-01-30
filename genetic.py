import pygad


def genetic(graph, source_node):

    nodes = list(graph.nodes())
    num_nodes = len(nodes)

    def calculate_path_weight(path):
        distance = 0
        for i in range(len(path) - 1):
            u, v = nodes[path[i]], nodes[path[i + 1]]
            distance += graph[u][v]['weight']
        distance += graph[nodes[path[-1]]][nodes[path[0]]]['weight']
        return distance

    def fitness_function(ga_instance, solution, solution_idx):
        return 1.0 / (calculate_path_weight(solution) + 1e-6)

    gene_space = list(range(num_nodes))

    ga_instance = pygad.GA(
        num_generations=1000,
        num_parents_mating=20,
        fitness_func=fitness_function,
        sol_per_pop=200,
        num_genes=num_nodes,
        gene_type=int,
        gene_space=gene_space,
        parent_selection_type="tournament",
        crossover_type="single_point",
        mutation_type="swap",
        mutation_percent_genes=10,
        allow_duplicate_genes=False,
        keep_parents=5,
        keep_elitism=5,
        suppress_warnings=True
    )

    ga_instance.run()

    solution, solution_fitness, _ = ga_instance.best_solution()
    weight = calculate_path_weight(solution)

    path = [nodes[solution[i]] for i in range(len(solution))]
    if source_node in path:
        index = path.index(source_node)
        path = path[index:] + path[:index]

    path.append(path[0])

    return weight, path
