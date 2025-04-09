# %%
"""
<h1> <b>Testes para diversos grafos <b><h1>
"""

# %%
#Import do código que habilita esses testes
import sys
sys.path.insert(1, '/home/julio/Projects/IC-Neuronios')
from Algoritmo_do_Artigo import Main as AA
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



# %%

nG = int(input("Quantos grafos você quer linkar?: "))
list_G = []
for i in range(nG):
    t = input(f"Qual o tipo de grafo {i}? (path, erdos ou grid): ")
    if t == 'path':
        N = int(input(f"número de neurônios do grafo {i}: "))
        list_G += [nx.path_graph(N)]
    elif t == 'erdos':
        N = int(input(f"número de neurônios do grafo {i}: "))
        p = float(input("Qual a probabilidade de conexão?: "))
        list_G += [nx.erdos_renyi_graph(N, p)]
    elif t == 'grid':
        N1 = int(input(f"Número de colunas da grid: "))
        N2 = int(input(f"Número de linhas da grid: "))
        list_G += [nx.convert_node_labels_to_integers(nx.grid_2d_graph(N1, N2), ordering='sorted')]


# %%
#Chamando os nós de outros números para evitar sobreposição

for i in range(nG - 1):
    mapping = {node: node + list(list_G[i].nodes())[-1]+1 for node in list_G[i+1].nodes()}
    list_G[i+1] = nx.relabel_nodes(list_G[i+1], mapping)



# %%
#Adiciona todas as linhas da matriz
G = nx.Graph()
for g in list_G:
    G = nx.compose(G, g)

# Conectando a 0 (primeira de G1) com N (primeira de G2)
for i in range(nG-1):
    G.add_edge(list(list_G[i].nodes)[-1], list(list_G[i+1].nodes)[0])

print(nx.to_numpy_array(G))
# %%
"""
Repare que o G1 sempre terá os pontos iniciais {0, 1, 2, ..., N-1}
e G2 o resto: {N, N+1, ..., 2N-1}
"""

# %%
AA(G, 1, plot=True, t_up_plot=100)