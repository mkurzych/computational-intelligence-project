import acopy


def ant_colony(graph, source_node, n_ants=10, n_iterations=100, alpha=1.0, beta=2.0,
               evaporation_rate=0.5, Q=100):

    # alpha: Pheromone importance
    # beta: Distance importance (heuristic)
    # evaporation_rate: Pheromone evaporation rate
    # Q: Pheromone deposit factor

    # create solver and colony
    solver = acopy.Solver(rho=evaporation_rate, q=Q)
    colony = acopy.Colony(alpha=alpha, beta=beta)

    # solve TSP on the networkx graph
    tour = solver.solve(graph, colony, limit=n_iterations, gen_size=n_ants)

    # extract path and distance
    path = list(tour.nodes)
    distance = tour.cost

    # rotate path to start with source_node
    if source_node in path:
        index = path.index(source_node)
        path = path[index:] + path[:index]

    # ensure path ends with the starting node
    if not path or path[-1] != path[0]:
        path.append(path[0])

    return distance, path

