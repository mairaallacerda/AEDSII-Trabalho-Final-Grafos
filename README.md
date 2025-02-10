# AEDSII-Trabalho-Final-Grafos

<div align="center" style="display: inline_block">
  <img align="center" alt="VS" src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white" />
  <img align="center" alt="Windows" src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
  <img align="center" alt="Linux" src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img align="center" alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
  <img align="center" alt="Overleaf" src="https://img.shields.io/badge/Overleaf-47A141?style=for-the-badge&logo=Overleaf&logoColor=white" />
  <img align="center" alt="Latex" src="https://img.shields.io/badge/latex-%23008080.svg?style=for-the-badge&logo=latex&logoColor=white" />
</div>

<br>


<div align="justify">
Este repositório contém os arquivos relacionados ao artigo "Análise de Grafos para Alocação de Frequências em Redes de Telecomunicação", que explora a aplicação de algoritmos de coloração para minimizar interferências na distribuição de espectro em redes móveis.
</div>

## 📂 Estrutura do Repositório

- [`article/`](https://github.com/mairaallacerda/AEDSII-Trabalho-Final-Grafos/blob/main/article/Artigo_Final_AEDS_II__09_02_.pdf): Contém o artigo científico em formato LaTeX.
- `src/`: Scripts Python utilizados para modelagem e análise dos grafos.
- `dataset/`: Arquivo CSV com os dados georreferenciados das torres de telecomunicação.
- `imgs/`: Imagens e gráficos gerados a partir dos experimentos.

## 📄 Resumo

<div align="justify">

Este estudo investiga a alocação de frequências em redes de telecomunicações utilizando coloração de grafos para minimizar interferências entre torres de transmissão. A modelagem do problema considera fatores como localização geográfica, potência de transmissão e coexistência de múltiplas tecnologias (2G, 3G, 4G e 5G). Foram implementados e comparados diferentes algoritmos de coloração, incluindo Guloso, DSATUR, Backtracking e Simulated Annealing, avaliando sua eficiência em termos de número de cores utilizadas, tempo de execução e adaptabilidade a restrições pré-estabelecidas. Os experimentos foram conduzidos utilizando dados reais de torres de telecomunicações na região de Divinópolis-MG. Os resultados demonstram que abordagens heurísticas podem oferecer soluções eficazes, equilibrando qualidade da coloração e viabilidade computacional.

</div>


## ⚙️ Execução do Código  

Para rodar os experimentos, é necessário garantir que todas as bibliotecas necessárias estejam instaladas e que o ambiente esteja devidamente configurado.  

### 📦 Bibliotecas Necessárias  

- **Bibliotecas:**  
  - `pandas` - Manipulação de dados  
  - `geopy` - Cálculo de distâncias geográficas  
  - `networkx` - Modelagem de grafos  
  - `matplotlib` - Geração de gráficos  

Para instalar todas as dependências, utilize o seguinte comando:  

```bash
pip install pandas geopy networkx matplotlib numpy
```

### 🚀 Como Executar  

1. **Clone o repositório:**  
   ```bash
   git clone https://github.com/mairaallacerda/AEDSII-Trabalho-Final-Grafos.git
   cd src
   ```
2. **Acesse a pasta src antes de rodar o script principal**
   ```bash
   cd src
   ```
3. **Execute o script principal:**  
   ```bash
   python3 main.py
   ```


## 📞 Contato

<table align="center">
  <tr>
    <th>Participante</th>
    <th>Contato</th>
  </tr>
  <tr>
    <td>Maíra Beatriz de Almeida Lacerda</td>
    <td><a href="https://github.com/mairaallacerda"><img align="center" height="20px" width="90px" src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/> </td>
  </tr>
</table>
