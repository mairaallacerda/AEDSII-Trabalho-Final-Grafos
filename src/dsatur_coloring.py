def dsatur_coloring(graph):
    degrees = {node: len(list(graph.neighbors(node))) for node in graph.nodes()}
    saturation = {node: 0 for node in graph.nodes()}
    colors = {}
    
    while degrees:
        node = max(degrees, key=lambda x: (saturation[x], degrees[x]))
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
        colors[node] = next(color for color in range(len(graph)) if color not in neighbor_colors)

        for neighbor in graph.neighbors(node):
            if neighbor not in colors:
                saturation[neighbor] += 1
        degrees.pop(node)
    
    return colors
