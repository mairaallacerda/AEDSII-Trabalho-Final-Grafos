import os
import time
import random
import networkx as nx
import matplotlib.pyplot as plt
from graph_utils import create_graph, visualize_coloring, generate_large_graph
from file_utils import save_results_to_file
from greedy_coloring import greedy_coloring
from dsatur_coloring import dsatur_coloring
from backtracking_coloring import backtracking_coloring
from simulated_annealing import simulated_annealing_coloring

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "resultados_coloracao.txt")

# Criar grafo principal
G = create_graph("dataset/DivinopolisMG.csv", threshold=5)

# Rodar e salvar resultados dos algoritmos
greedy_colors = greedy_coloring(G)
save_results_to_file(output_file, "Gulosa", greedy_colors)

dsatur_colors = dsatur_coloring(G)
save_results_to_file(output_file, "DSATUR", dsatur_colors)

backtracking_colors = backtracking_coloring(G)
save_results_to_file(output_file, "Backtracking", backtracking_colors)

# Visualizar resultados
visualize_coloring(G, greedy_colors, title="Grafo Colorido - Gulosa", filename="gulosa.png")
visualize_coloring(G, dsatur_colors, title="Grafo Colorido - DSATUR", filename="dsatur.png")
visualize_coloring(G, backtracking_colors, title="Grafo Colorido - Backtracking", filename="backtracking.png")

# Gerar grafo grande para testes
large_G = generate_large_graph(50, 0.2)

# Testar Simulated Annealing
sa_colors = simulated_annealing_coloring(large_G, max_colors=10)
visualize_coloring(large_G, sa_colors, title="Simulated Annealing", filename="simulated_annealing.png")

print("Execução concluída. Resultados e gráficos salvos na pasta output.")
