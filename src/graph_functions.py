import os
import pandas as pd
import geopy.distance
import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import math
from collections import Counter

def convert_coordinates(coord):
    """
    Converte coordenadas no formato DMS (graus, minutos, segundos e direção)
    para decimal.
    Exemplo de entrada: "192345W" ou "192345E"
    """
    degrees = int(coord[:2])
    minutes = int(coord[3:5])
    seconds = int(coord[5:-1])
    direction = coord[-1]
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def load_data(file_path):
    """
    Carrega e processa os dados do arquivo CSV.
    Converte as colunas 'Latitude' e 'Longitude' para o formato decimal.
    """
    data = pd.read_csv(file_path)
    data['Latitude'] = data['Latitude'].apply(convert_coordinates)
    data['Longitude'] = data['Longitude'].apply(convert_coordinates)
    return data

def create_graph(data, threshold=5):
    """
    Cria um grafo a partir dos dados.
    Cada nó representa uma torre, e uma aresta é criada entre duas torres
    se a distância entre elas for menor ou igual ao threshold (em km).
    """
    torres = data[['NumEstacao', 'NomeEntidade', 'Latitude', 'Longitude']]
    G = nx.Graph()
    
    # Adicionar vértices
    for _, row in torres.iterrows():
        G.add_node(row['NumEstacao'], entidade=row['NomeEntidade'], pos=(row['Latitude'], row['Longitude']))
    
    # Adicionar arestas com base na distância
    for i, torre1 in torres.iterrows():
        for j, torre2 in torres.iterrows():
            if i < j:
                dist = geopy.distance.distance((torre1['Latitude'], torre1['Longitude']),
                                               (torre2['Latitude'], torre2['Longitude'])).km
                if dist <= threshold:
                    G.add_edge(torre1['NumEstacao'], torre2['NumEstacao'], weight=dist)
    return G

def draw_graph(G, output_file, title="Grafo de Torres"):
    plt.figure(figsize=(15, 12))
    pos = nx.spring_layout(G, k=2)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color='lightblue',
        node_size=500,
        font_size=8,
        edge_color='gray'
    )
    plt.title(title, fontsize=16)
    plt.savefig(output_file)
    plt.close()
    print(f"Gráfico salvo em: {output_file}")

def greedy_coloring(graph):
    """
    Implementa a coloração gulosa.
    Para cada nó, atribui a menor cor que não esteja sendo usada por seus vizinhos.
    """
    colors = {}
    for node in graph.nodes():
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
        colors[node] = next(color for color in range(len(graph)) if color not in neighbor_colors)
    return colors

def dsatur_coloring(graph):
    """
    Implementa a coloração DSATUR.
    Seleciona, a cada iteração, o nó com maior grau de saturação (número de cores já usadas
    pelos vizinhos) e, em caso de empate, usa o grau do nó.
    """
    degrees = {node: len(list(graph.neighbors(node))) for node in graph.nodes()}
    saturation = {node: 0 for node in graph.nodes()}
    colors = {}
    
    while degrees:
        node = max(degrees, key=lambda x: (saturation[x], degrees[x]))
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
        colors[node] = next(color for color in range(len(graph)) if color not in neighbor_colors)
        
        # Atualizar a saturação dos vizinhos
        for neighbor in graph.neighbors(node):
            if neighbor not in colors:
                saturation[neighbor] += 1
        degrees.pop(node)
    return colors

def is_valid(node, color, colors, graph):
    """
    Verifica se a cor 'color' pode ser atribuída ao 'node' sem entrar em conflito com os vizinhos.
    """
    for neighbor in graph.neighbors(node):
        if colors.get(neighbor) == color:
            return False
    return True

def backtracking_coloring(graph, colors=None, node_list=None, current_index=0):
    """
    Implementa a coloração por backtracking.
    Tenta atribuir cores a todos os nós sem conflitos.
    """
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

def visualize_coloring(graph, coloring, output_file, title="Grafo Colorido"):
    """
    Desenha e salva o grafo com a coloração aplicada.
    """
    plt.figure(figsize=(15, 12))
    pos = nx.spring_layout(graph, k=2)
    color_map = [coloring[node] for node in graph.nodes()]
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=color_map,
        node_size=500,
        font_size=8,
        cmap=plt.cm.Set3,
        edge_color='gray'
    )
    plt.title(title, fontsize=16)
    plt.savefig(output_file)
    plt.close()
    print(f"Gráfico salvo em: {output_file}")

def save_results_to_file(file_path, algorithm_name, results):

    with open(file_path, 'a') as file:
        file.write(f"Resultados da coloração - {algorithm_name}:\n")
        for node, color in results.items():
            file.write(f"Nó {node}: Cor {color}\n")
        file.write("\n")

def test_algorithm(algorithm, graph):
    """
    Testa um algoritmo de coloração e retorna o dicionário de cores e o tempo de execução.
    """
    start = time.time()
    colors = algorithm(graph)
    end = time.time()
    return colors, end - start

def generate_large_graph(num_nodes, edge_probability):
    """
    Gera um grafo aleatório com 'num_nodes' nós e arestas com a probabilidade dada.
    """
    large_graph = nx.Graph()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                large_graph.add_edge(i, j)
    return large_graph

def greedy_coloring_with_restrictions(graph, pre_allocated):
    """
    Implementa a coloração gulosa considerando cores pré-alocadas para alguns nós.
    """
    colors = pre_allocated.copy()
    for node in graph.nodes():
        if node in pre_allocated:
            continue
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
        colors[node] = next(color for color in range(len(graph)) if color not in neighbor_colors)
    return colors

def simulated_annealing_coloring(graph, max_colors, initial_temp=1000, cooling_rate=0.995):
    """
    Implementa a coloração usando o algoritmo Simulated Annealing.
    """
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

def visualize_and_save_coloring(graph, coloring, title, output_dir, filename):
 
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(graph, k=2)
    color_map = [coloring[node] for node in graph.nodes()]
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=color_map,
        node_size=300,
        font_size=8,
        cmap=plt.cm.Set3,
        edge_color='gray'
    )
    plt.title(title, fontsize=16)
    output_file = os.path.join(output_dir, filename)
    plt.savefig(output_file)
    plt.close()
    print(f"Gráfico salvo em: {output_file}")

def analyze_color_distribution(colors):
    """
    Analisa e imprime a distribuição de cores usada na coloração.
    """
    distribution = Counter(colors.values())
    print("Distribuição de cores:", distribution)
