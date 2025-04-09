# %%
"""
<h1> <b>Testes para diversos grafos <b><h1>
"""

# %%
#Import do código que habilita esses testes
import sys
sys.path.insert(1, '/home/julio/Projects/IC-Neuronios/Neurônios Inibitórios/')
from Algoritmo_do_Artigo_ni import Main as AA
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



# %%

t = input(f"Qual o tipo de grafo? (path, erdos ou grid): ")
q = float(input(f"Qual a proporção de inibitórios?: "))
if t == 'path':
    N = int(input(f"número de neurônios do grafo: "))
    G = nx.path_graph(N)
elif t == 'erdos':
    N = int(input(f"número de neurônios do grafo: "))
    p = float(input("Qual a probabilidade de conexão?: "))
    G = nx.erdos_renyi_graph(N, p)
elif t == 'grid':
    N1 = int(input(f"Número de colunas da grid: "))
    N2 = int(input(f"Número de linhas da grid: "))
    G = nx.convert_node_labels_to_integers(nx.grid_2d_graph(N1, N2), ordering='sorted')

# %%
AA(G, 1, q, plot=False, t_up_plot=10)