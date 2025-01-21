import os
import pandas as pd
import geopy.distance
import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import math


# Criar a pasta de saída, se não existir
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "grafo_torres_telecomunicacao.png")

# Carregar os dados
file_path = "dataset/DivinopolisMG.csv"
data = pd.read_csv(file_path)
#print("Nomes das colunas:", data.columns)

# Exibir os dados carregados
#print(data.head())

# Converter latitude e longitude para coordenadas numéricas
def convert_coordinates(coord):
    degrees = int(coord[:2])
    minutes = int(coord[3:5])
    seconds = int(coord[5:])
    direction = coord[-1]
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

data['Latitude'] = data['Latitude'].apply(convert_coordinates)
data['Longitude'] = data['Longitude'].apply(convert_coordinates)

# Criar um dataframe apenas com as colunas relevantes
torres = data[['NumEstacao', 'NomeEntidade', 'Latitude', 'Longitude']]

# Criar o grafo
G = nx.Graph()

# Adicionar vértices
for _, row in torres.iterrows():
    G.add_node(row['NumEstacao'], entidade=row['NomeEntidade'], pos=(row['Latitude'], row['Longitude']))

# Adicionar arestas com base na distância
threshold = 5  # Distância máxima para considerar interferência (em km)
for i, torre1 in torres.iterrows():
    for j, torre2 in torres.iterrows():
        if i < j:
            dist = geopy.distance.distance((torre1['Latitude'], torre1['Longitude']),
                                           (torre2['Latitude'], torre2['Longitude'])).km
            if dist <= threshold:
                G.add_edge(torre1['NumEstacao'], torre2['NumEstacao'], weight=dist)

# Ajustar o espaçamento entre os nós para melhor visualização
plt.figure(figsize=(15, 12))  # Aumentar o tamanho do gráfico

# Usar o layout spring para distribuir os nós de forma mais uniforme
pos = nx.spring_layout(G, k=2)  # O parâmetro `k` ajusta o espaçamento

# Desenhar o grafo ajustado
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color='lightblue',
    node_size=500,
    font_size=8,
    edge_color='gray'
)

# Adicionar título
plt.title("Grafo de Torres de Telecomunicação (Ajustado)", fontsize=16)

plt.savefig(output_file)
print(f"Gráfico salvo em: {output_file}")

# Mostrar o gráfico
plt.show()  


# Definir o número de linhas a serem usadas aleatoriamente
line_limit = 50  # Ajuste o número de linhas que deseja usar (exemplo: 100 ou 200)

# Selecionar aleatoriamente `line_limit` linhas do DataFrame
torres_limited = torres.sample(n=line_limit, random_state=42)

# Criar o grafo
G = nx.Graph()

# Adicionar vértices
for _, row in torres_limited.iterrows():
    G.add_node(row['NumEstacao'], entidade=row['NomeEntidade'], pos=(row['Latitude'], row['Longitude']))

# Adicionar arestas com base na distância
threshold = 5  # Distância máxima para considerar interferência (em km)
for i, torre1 in torres_limited.iterrows():
    for j, torre2 in torres_limited.iterrows():
        if i < j:
            dist = geopy.distance.distance((torre1['Latitude'], torre1['Longitude']),
                                           (torre2['Latitude'], torre2['Longitude'])).km
            if dist <= threshold:
                G.add_edge(torre1['NumEstacao'], torre2['NumEstacao'], weight=dist)

# Ajustar o espaçamento entre os nós para melhor visualização
plt.figure(figsize=(15, 12))  # Aumentar o tamanho do gráfico

# Usar o layout spring para distribuir os nós de forma mais uniforme
pos = nx.spring_layout(G, k=2)  # O parâmetro `k` ajusta o espaçamento

# Desenhar o grafo ajustado
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color='lightblue',
    node_size=500,
    font_size=8,
    edge_color='gray'
)

# Adicionar título
plt.title(f"Grafo de Torres de Telecomunicação (Ajustado, Linhas Aleatórias)", fontsize=16)


output_file = os.path.join(output_dir, "grafo_de_torres_de_telecomunicacao_ajustado_linhas_aleatorias.png")

plt.savefig(output_file)
print(f"Gráfico salvo em: {output_file}")


# Mostrar o gráfico
plt.show()


#Coloração Gulosa

def greedy_coloring(graph):
    colors = {}
    for node in graph.nodes():
        # Obter cores dos vizinhos
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
        # Atribuir a menor cor disponível
        colors[node] = next(color for color in range(len(graph)) if color not in neighbor_colors)
    return colors


#DSATUR
def dsatur_coloring(graph):
    degrees = {node: len(list(graph.neighbors(node))) for node in graph.nodes()}
    saturation = {node: 0 for node in graph.nodes()}
    colors = {}

    while degrees:
        # Selecionar nó com maior grau de saturação
        node = max(degrees, key=lambda x: (saturation[x], degrees[x]))
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
        colors[node] = next(color for color in range(len(graph)) if color not in neighbor_colors)

        # Atualizar saturação dos vizinhos
        for neighbor in graph.neighbors(node):
            if neighbor not in colors:
                saturation[neighbor] += 1
        degrees.pop(node)

    return colors

#Backtracking
def is_valid(node, color, colors, graph):
    for neighbor in graph.neighbors(node):
        if colors.get(neighbor) == color:
            return False
    return True

def backtracking_coloring(graph, colors=None, node_list=None, current_index=0):  # Change here
    if colors is None:
        colors = {}
    if node_list is None:  # Change here
        node_list = list(graph.nodes())  # Change here
    if current_index == len(node_list):  # Change here
        return colors

    node = node_list[current_index]  # Change here

    for color in range(len(graph)):
        if is_valid(node, color, colors, graph):
            colors[node] = color
            result = backtracking_coloring(graph, colors, node_list, current_index + 1)  # Change here
            if result:
                return result
            colors.pop(node)
    return None

#Executar os algoritmos no grafo criado

def visualize_coloring(graph, coloring, title="Coloração de Grafos", output_dir="output", filename="grafo_colorido.png"):
    # Criar a pasta de saída, se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Gerar o mapa de cores baseado na coloração fornecida
    color_map = [coloring[node] for node in graph.nodes()]

    # Configurar o tamanho da figura para maior clareza
    plt.figure(figsize=(15, 12))  # Aumentar o tamanho do gráfico

    # Usar spring_layout para distribuir os nós de forma mais uniforme
    pos = nx.spring_layout(graph, k=2)  # O parâmetro `k` ajusta o espaçamento

    # Desenhar o grafo com a coloração aplicada
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=color_map,
        node_size=700,
        font_size=9,
        cmap=plt.cm.Set3,  # Paleta de cores agradável
        edge_color="gray"
    )

    # Adicionar título ao gráfico
    plt.title(title, fontsize=16)

    # Salvar o gráfico antes de exibi-lo
    output_file = os.path.join(output_dir, filename)
    plt.savefig(output_file)
    print(f"Gráfico salvo em: {output_file}")

    # Mostrar o gráfico
    plt.show()


# Função para salvar os resultados em um arquivo
def save_results_to_file(file_path, algorithm_name, results):
    with open(file_path, 'a') as file:  # 'a' para adicionar conteúdo ao arquivo sem sobrescrever
        file.write(f"Resultados da coloração - {algorithm_name}:\n")
        for node, color in results.items():
            file.write(f"Nó {node}: Cor {color}\n")
        file.write("\n")  # Adicionar uma linha em branco para separar os resultados


# Definir o arquivo para salvar os resultados
output_file = os.path.join(output_dir, "resultados_coloracao.txt")

# Testar os algoritmos e salvar os resultados
print("Rodando coloração Gulosa...")
greedy_colors = greedy_coloring(G)
save_results_to_file(output_file, "Gulosa", greedy_colors)

print("Rodando coloração DSATUR...")
dsatur_colors = dsatur_coloring(G)
save_results_to_file(output_file, "DSATUR", dsatur_colors)

print("Rodando Backtracking...")
backtracking_colors = backtracking_coloring(G)
save_results_to_file(output_file, "Backtracking", backtracking_colors)

print(f"Resultados salvos em: {output_file}")

visualize_coloring(G, greedy_colors, title="Grafo Colorido - Gulosa", filename="gulosa.png")
visualize_coloring(G, dsatur_colors, title="Grafo Colorido - DSATUR", filename="dsatur.png")
visualize_coloring(G, backtracking_colors, title="Grafo Colorido - Backtracking", filename="backtracking.png")

print("\n")

def test_algorithm(algorithm, graph):
    start = time.time()
    colors = algorithm(graph)
    end = time.time()
    return colors, end - start

algorithms = {
    "Gulosa": greedy_coloring,
    "DSATUR": dsatur_coloring,
    "Backtracking": backtracking_coloring,
}

results = {}
for name, algorithm in algorithms.items():
    print(f"Testando {name}...")
    colors, exec_time = test_algorithm(algorithm, G)
    results[name] = {"colors": len(set(colors.values())), "time": exec_time}

# Exibir resultados
for alg, result in results.items():
    print(f"{alg}: {result['colors']} cores, {result['time']:.4f} segundos")

print("\n")

# Gerar grafo aleatório maior
def generate_large_graph(num_nodes, edge_probability):
    large_graph = nx.Graph()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                large_graph.add_edge(i, j)
    return large_graph

# Gerar grafo com 50 nós e probabilidade de 0.2 para arestas
large_G = generate_large_graph(50, 0.2)

# Visualizar o grafo
plt.figure(figsize=(12, 10))
nx.draw(large_G, with_labels=True, node_color='lightblue', node_size=300, font_size=8)
plt.title("Grafo Aleatório (50 nós)")

output_file = os.path.join(output_dir, "grafo_aleatorio_50_nos.png")

plt.savefig(output_file)
print(f"Gráfico salvo em: {output_file}")

plt.show()

print("\n")

# Pré-alocar cores para alguns nós
pre_allocated_colors = {0: 0, 1: 1, 2: 2}  # Exemplo: Nós 0, 1, 2 já têm cores atribuídas
print("Frequências pré-alocadas:", pre_allocated_colors)

print("\n")

# Modificar algoritmos para considerar pré-alocações
def greedy_coloring_with_restrictions(graph, pre_allocated):
    colors = pre_allocated.copy()
    for node in graph.nodes():
        if node in pre_allocated:
            continue
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
        colors[node] = next(color for color in range(len(graph)) if color not in neighbor_colors)
    return colors

print("\n")

# Testar algoritmo guloso com restrições
restricted_colors = greedy_coloring_with_restrictions(large_G, pre_allocated_colors)
print("Coloração com restrições:", restricted_colors)


def simulated_annealing_coloring(graph, max_colors, initial_temp=1000, cooling_rate=0.995):
    # Inicialização
    current_solution = {node: random.randint(0, max_colors - 1) for node in graph.nodes()}
    current_cost = len(set(current_solution.values()))
    temp = initial_temp

    while temp > 1:
        # Escolher um nó e alterar sua cor aleatoriamente
        node = random.choice(list(graph.nodes()))
        old_color = current_solution[node]
        new_color = random.randint(0, max_colors - 1)
        current_solution[node] = new_color

        # Recalcular custo
        new_cost = len(set(current_solution.values()))
        delta_cost = new_cost - current_cost

        # Aceitar ou rejeitar a nova solução
        if delta_cost <= 0 or random.random() < math.exp(-delta_cost / temp):
            current_cost = new_cost
        else:
            current_solution[node] = old_color  # Reverter mudança

        # Resfriamento
        temp *= cooling_rate

    return current_solution

print("\n")

# Executar Simulated Annealing
sa_colors = simulated_annealing_coloring(large_G, max_colors=10)
print("Coloração com Simulated Annealing:", sa_colors)

print("\n")

# Função para salvar os gráficos com base na coloração
def visualize_and_save_coloring(graph, coloring, title, output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)  # Criar a pasta de saída, se necessário
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(graph, k=2)  # Layout uniforme
    color_map = [coloring[node] for node in graph.nodes()]
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=color_map,
        node_size=300,
        font_size=8,
        cmap=plt.cm.Set3,
        edge_color="gray"
    )
    plt.title(title, fontsize=16)
    output_file = os.path.join(output_dir, filename)
    plt.savefig(output_file)  # Salvar o gráfico
    print(f"Gráfico salvo em: {output_file}")
    plt.show()  # Mostrar o gráfico

# Definir pasta de saída
output_dir = "output"

# Testar algoritmos no grafo maior
print("Rodando Gulosa com restrições...")
greedy_large = greedy_coloring_with_restrictions(large_G, pre_allocated_colors)

print("Rodando DSATUR no grafo maior...")
dsatur_large = dsatur_coloring(large_G)

print("Rodando Simulated Annealing...")
sa_large = simulated_annealing_coloring(large_G, max_colors=10)

# Salvar e visualizar os resultados
visualize_and_save_coloring(large_G, greedy_large, "Gulosa com Restrições", output_dir, "gulosa_restricoes.png")
visualize_and_save_coloring(large_G, dsatur_large, "DSATUR", output_dir, "dsatur_grafo_maior.png")
visualize_and_save_coloring(large_G, sa_large, "Simulated Annealing", output_dir, "simulated_annealing.png")

# Comparar tempo e número de cores
results_large = {
    "Gulosa": len(set(greedy_large.values())),
    "DSATUR": len(set(dsatur_large.values())),
    "Simulated Annealing": len(set(sa_large.values())),
}

# Salvar os resultados comparativos em um arquivo de texto
# results_file = os.path.join(output_dir, "resultados_grafo_maior.txt")
# with open(results_file, 'w') as f:
#     f.write("Resultados para o grafo maior:\n")
#     for alg, num_colors in results_large.items():
#         f.write(f"{alg}: {num_colors} cores\n")
#     print(f"Resultados comparativos salvos em: {results_file}")

# Exibir os resultados no console
print("\nResultados para o grafo maior:")
for alg, num_colors in results_large.items():
    print(f"{alg}: {num_colors} cores")


\
print("\n")

# # Ajustar parâmetros do Simulated Annealing
# sa_colors_optimized = simulated_annealing_coloring(large_G, max_colors=6, initial_temp=5000, cooling_rate=0.99)
# print("Coloração com Simulated Annealing (Parâmetros Otimizados):", len(set(sa_colors_optimized.values())))

# # Visualizar o resultado otimizado
# visualize_coloring(large_G, sa_colors_optimized, title="Simulated Annealing Otimizado")


# Função para visualizar e salvar o grafo com coloração
def visualize_and_save_coloring(graph, coloring, title, output_dir, filename):
    # Criar a pasta de saída, se necessário
    os.makedirs(output_dir, exist_ok=True)
    
    # Configurar o tamanho e layout do gráfico
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(graph, k=2)  # Distribuição uniforme dos nós
    color_map = [coloring[node] for node in graph.nodes()]
    
    # Desenhar o grafo
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=color_map,
        node_size=300,
        font_size=8,
        cmap=plt.cm.Set3,
        edge_color="gray"
    )
    plt.title(title, fontsize=16)
    
    # Salvar o gráfico
    output_file = os.path.join(output_dir, filename)
    plt.savefig(output_file)
    print(f"Gráfico salvo em: {output_file}")
    
    # Mostrar o gráfico
    plt.show()

# Ajustar parâmetros do Simulated Annealing
output_dir = "output"  # Diretório para salvar gráficos
sa_colors_optimized = simulated_annealing_coloring(large_G, max_colors=6, initial_temp=5000, cooling_rate=0.99)

# Exibir e salvar o grafo com a coloração otimizada
visualize_and_save_coloring(
    large_G,
    sa_colors_optimized,
    title="Simulated Annealing Otimizado",
    output_dir=output_dir,
    filename="simulated_annealing_otimizado.png"
)

from collections import Counter

def analyze_color_distribution(colors):
    distribution = Counter(colors.values())
    print("Distribuição de cores:", distribution)

# Analisar distribuições
analyze_color_distribution(greedy_large)
analyze_color_distribution(dsatur_large)
analyze_color_distribution(sa_large)


# Gerar grafos com diferentes densidades
sparse_graph = generate_large_graph(50, 0.1)  # Esparso
dense_graph = generate_large_graph(50, 0.5)   # Denso

# Testar algoritmos nesses grafos
for graph, density in [(sparse_graph, "Esparso"), (dense_graph, "Denso")]:
    print(f"\nResultados para grafo {density}:")
    print("Gulosa:", len(set(greedy_coloring(graph).values())), "cores")
    print("DSATUR:", len(set(dsatur_coloring(graph).values())), "cores")
