def is_valid(node, color, colors, graph):
    for neighbor in graph.neighbors(node):
        if colors.get(neighbor) == color:
            return False
    return True

def backtracking_coloring(graph, colors=None, node_list=None, current_index=0):  
    if colors is None:
        colors = {}
    if node_list is None:  
        node_list = list(graph.nodes())  
    if current_index == len(node_list):  
        return colors

    node = node_list[current_index]  

    for color in range(len(graph)):
        if is_valid(node, color, colors, graph):
            colors[node] = color
            result = backtracking_coloring(graph, colors, node_list, current_index + 1)  
            if result:
                return result
            colors.pop(node)
    return None
