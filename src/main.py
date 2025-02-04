import os
import matplotlib.pyplot as plt
import networkx as nx
from graph_functions import (
    load_data, create_graph, draw_graph, greedy_coloring, dsatur_coloring,
    backtracking_coloring, visualize_coloring, save_results_to_file, test_algorithm,
    generate_large_graph, greedy_coloring_with_restrictions, simulated_annealing_coloring,
    visualize_and_save_coloring, analyze_color_distribution
)

def main():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    ### PARTE 1: GRAFO A PARTIR DO DATASET ###
    data_file = "dataset/DivinopolisMG.csv"  
    data = load_data(data_file)
    
    # Criar o grafo com base no dataset
    G = create_graph(data, threshold=5)
    
    # Desenhar e salvar o grafo original
    output_file = os.path.join(output_dir, "grafo_torres_telecomunicacao.png")
    draw_graph(G, output_file, title="Grafo de Torres de Telecomunicação")
    
    # Aplicar coloração gulosa e visualizar
    greedy_colors = greedy_coloring(G)
    output_file_colorido = os.path.join(output_dir, "grafo_colorido_guloso.png")
    visualize_coloring(G, greedy_colors, output_file_colorido, title="Grafo Colorido - Gulosa")
    
    resultados_file = os.path.join(output_dir, "resultados_coloracao.txt")
    save_results_to_file(resultados_file, "Gulosa", greedy_colors)
    
    # Aplicar DSATUR e salvar resultados
    dsatur_colors = dsatur_coloring(G)
    save_results_to_file(resultados_file, "DSATUR", dsatur_colors)
    
    # Aplicar Backtracking e salvar resultados
    backtracking_colors = backtracking_coloring(G)
    save_results_to_file(resultados_file, "Backtracking", backtracking_colors)
    
    # Testar e exibir tempos de execução dos algoritmos
    algorithms = {
        "Gulosa": greedy_coloring,
        "DSATUR": dsatur_coloring,
        "Backtracking": backtracking_coloring,
    }
    print("Testando algoritmos de coloração:")
    for name, algorithm in algorithms.items():
        colors, exec_time = test_algorithm(algorithm, G)
        print(f"{name}: {len(set(colors.values()))} cores, {exec_time:.4f} segundos")
    
    
    ### PARTE 2: GRAFO ALEATÓRIO MAIOR ###
    # Gerar um grafo aleatório com 50 nós e probabilidade de 0.2 para as arestas
    large_G = generate_large_graph(50, 0.2)
    
    output_file_large = os.path.join(output_dir, "grafo_aleatorio_50_nos.png")
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(large_G, k=2)
    nx.draw(large_G, pos, with_labels=True, node_color='lightblue', node_size=300, font_size=8)
    plt.title("Grafo Aleatório (50 nós)")
    plt.savefig(output_file_large)
    plt.close()
    print(f"Gráfico salvo em: {output_file_large}")
    
    # Pré-alocar cores para alguns nós (exemplo)
    pre_allocated_colors = {0: 0, 1: 1, 2: 2}
    print("Cores pré-alocadas:", pre_allocated_colors)
    
    # Coloração gulosa com restrições
    greedy_restricoes = greedy_coloring_with_restrictions(large_G, pre_allocated_colors)
    print("Coloração com restrições (Gulosa):", greedy_restricoes)
    
    # Aplicar Simulated Annealing
    sa_colors = simulated_annealing_coloring(large_G, max_colors=10)
    print("Coloração com Simulated Annealing:", sa_colors)
    
    # Visualizar e salvar as colorações para o grafo grande
    visualize_and_save_coloring(large_G, greedy_restricoes, "Gulosa com Restrições", output_dir, "gulosa_restricoes.png")
    dsatur_large = dsatur_coloring(large_G)
    visualize_and_save_coloring(large_G, dsatur_large, "DSATUR", output_dir, "dsatur_grafo_maior.png")
    visualize_and_save_coloring(large_G, sa_colors, "Simulated Annealing", output_dir, "simulated_annealing.png")
    
    # Comparar resultados (número de cores) para o grafo grande
    results_large = {
        "Gulosa": len(set(greedy_restricoes.values())),
        "DSATUR": len(set(dsatur_large.values())),
        "Simulated Annealing": len(set(sa_colors.values())),
    }
    print("\nResultados para o grafo maior:")
    for alg, num_colors in results_large.items():
        print(f"{alg}: {num_colors} cores")
    
    # Ajustar parâmetros do Simulated Annealing e visualizar o resultado otimizado
    sa_colors_optimized = simulated_annealing_coloring(large_G, max_colors=6, initial_temp=5000, cooling_rate=0.99)
    visualize_and_save_coloring(large_G, sa_colors_optimized, "Simulated Annealing Otimizado", output_dir, "simulated_annealing_otimizado.png")
    
    # Analisar a distribuição de cores
    print("\nAnálise da distribuição de cores para o grafo maior:")
    print("Gulosa:")
    analyze_color_distribution(greedy_restricoes)
    print("DSATUR:")
    analyze_color_distribution(dsatur_large)
    print("Simulated Annealing:")
    analyze_color_distribution(sa_colors)
    
    # Gerar grafos com diferentes densidades e testar os algoritmos
    sparse_graph = generate_large_graph(50, 0.1)  # Grafo esparso
    dense_graph = generate_large_graph(50, 0.5)   # Grafo denso
    
    for graph, density in [(sparse_graph, "Esparso"), (dense_graph, "Denso")]:
        print(f"\nResultados para grafo {density}:")
        print("Gulosa:", len(set(greedy_coloring(graph).values())), "cores")
        print("DSATUR:", len(set(dsatur_coloring(graph).values())), "cores")

if __name__ == '__main__':
    main()
