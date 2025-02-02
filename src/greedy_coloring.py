def greedy_coloring(graph):
    colors = {}
    for node in graph.nodes():
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
        colors[node] = next(color for color in range(len(graph)) if color not in neighbor_colors)
    return colors
