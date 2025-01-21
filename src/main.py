import os
import pandas as pd
import geopy.distance
import networkx as nx
import matplotlib.pyplot as plt

# Criar a pasta de saída, se não existir
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "grafo_torres_telecomunicacao.png")

# Carregar os dados
file_path = "dataset/DivinopolisMG.csv"
data = pd.read_csv(file_path)
print("Nomes das colunas:", data.columns)

# Exibir os dados carregados
print(data.head())

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