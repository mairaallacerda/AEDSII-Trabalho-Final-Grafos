import os
import pandas as pd
import geopy.distance
import networkx as nx
import matplotlib.pyplot as plt
import random

def convert_coordinates(coord):
    degrees = int(coord[:2])
    minutes = int(coord[3:5])
    seconds = int(coord[5:])
    direction = coord[-1]
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def create_graph(file_path, threshold=5):
    data = pd.read_csv(file_path)
    data['Latitude'] = data['Latitude'].apply(convert_coordinates)
    data['Longitude'] = data['Longitude'].apply(convert_coordinates)
    torres = data[['NumEstacao', 'NomeEntidade', 'Latitude', 'Longitude']]

    G = nx.Graph()
    for _, row in torres.iterrows():
        G.add_node(row['NumEstacao'], entidade=row['NomeEntidade'], pos=(row['Latitude'], row['Longitude']))

    for i, torre1 in torres.iterrows():
        for j, torre2 in torres.iterrows():
            if i < j:
                dist = geopy.distance.distance((torre1['Latitude'], torre1['Longitude']),
                                               (torre2['Latitude'], torre2['Longitude'])).km
                if dist <= threshold:
                    G.add_edge(torre1['NumEstacao'], torre2['NumEstacao'], weight=dist)
    return G

def visualize_coloring(graph, coloring, title, output_dir="output", filename="grafo_colorido.png"):
    os.makedirs(output_dir, exist_ok=True)
    color_map = [coloring[node] for node in graph.nodes()]
    plt.figure(figsize=(15, 12))
    pos = nx.spring_layout(graph, k=2)
    nx.draw(graph, pos, with_labels=True, node_color=color_map, node_size=700, font_size=9, cmap=plt.cm.Set3, edge_color="gray")
    plt.title(title, fontsize=16)
    output_file = os.path.join(output_dir, filename)
    plt.savefig(output_file)
    print(f"Gráfico salvo em: {output_file}")
    plt.show()

def generate_large_graph(num_nodes, edge_probability):
    large_graph = nx.Graph()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                large_graph.add_edge(i, j)
    return large_graph
