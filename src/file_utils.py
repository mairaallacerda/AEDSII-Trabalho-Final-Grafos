import os

def save_results_to_file(file_path, algorithm_name, results):
    with open(file_path, 'a') as file:
        file.write(f"Resultados da coloração - {algorithm_name}:\n")
        for node, color in results.items():
            file.write(f"Nó {node}: Cor {color}\n")
        file.write("\n")
