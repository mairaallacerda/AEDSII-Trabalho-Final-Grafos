import random
import math

def simulated_annealing_coloring(graph, max_colors, initial_temp=1000, cooling_rate=0.995):
    current_solution = {node: random.randint(0, max_colors - 1) for node in graph.nodes()}
    current_cost = len(set(current_solution.values()))
    temp = initial_temp

    while temp > 1:
        node = random.choice(list(graph.nodes()))
        old_color = current_solution[node]
        new_color = random.randint(0, max_colors - 1)
        current_solution[node] = new_color

        new_cost = len(set(current_solution.values()))
        delta_cost = new_cost - current_cost

        if delta_cost <= 0 or random.random() < math.exp(-delta_cost / temp):
            current_cost = new_cost
        else:
            current_solution[node] = old_color

        temp *= cooling_rate

    return current_solution
