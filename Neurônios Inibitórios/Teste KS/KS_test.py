import sys
import networkx as nx
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import concurrent.futures

# Importação da sua simulação refatorada
sys.path.insert(1, '/home/julio/Projects/IC-Neuronios/Neurônios Inibitórios/')
from Algoritmo_do_Artigo_ni import Main as SimulaRede

# Fixamos a seed do NumPy para garantir que as uniformes sejam reprodutíveis
np.random.seed(42) 

g_start = 1.0
g_end = 2.0
e_step = 0.1
d_step = 0.01

results = {}
results[(g_start, 1.0)] = 0
results[(g_start, 0.99)] = 0

S = nx.convert_node_labels_to_integers(nx.grid_2d_graph(12, 12), ordering='sorted')
N = S.number_of_nodes()

uniform_vals = np.random.rand(N)

with open('resultados.txt', 'a') as f:
    f.write('Novo registro:\n')
    
    g = g_start
    while g < g_end:
        T = True
        U = True
        p = 1.0 - (2 * d_step)
        
        while T or U:
            val = np.where(uniform_vals < p)[0].tolist()
            
            f.write("\n")
            print(f"p: {p:.2f} | g: {g:.2f} | Nós inibitórios (tamanho {len(val)}): {val}")
            
            # Executa as 500 simulações em paralelo
            print(f"Rodando 500 simulações em paralelo...")
            with concurrent.futures.ProcessPoolExecutor() as executor:
                futures = [executor.submit(SimulaRede, S, g, val, plot=False) for _ in range(500)]
                
                AA_list = []
                for future in concurrent.futures.as_completed(futures):
                    AA_list.append(future.result())
                    
            AA = np.array(AA_list)
            
            # Normalização e Teste KS
            mean_AA = np.mean(AA)
            AA / mean_AA
                
            result = stats.kstest(AA_norm, stats.expon.cdf)
            p_rounded = round(p, 2)
            g_rounded = round(g, 2)
            
            if result.pvalue < 0.05:
                results[(g_rounded, p_rounded)] = 0
                f.write(f"g: {g_rounded} p: {p_rounded}: 0")
            elif T and result.pvalue >= 0.05:
                results[(g_rounded, p_rounded)] = 1
                f.write(f"g: {g_rounded} p: {p_rounded}: 1")
                T = False
            else:
                results[(g_rounded, p_rounded)] = 1
                f.write(f"g: {g_rounded} p: {p_rounded}: 1")
                U = False
                
            print(f"p-value: {result.pvalue}")
            print(f"dicionário: {results}\n")
            print(f"P>>>>>>>>>>>>>>> {p_rounded}")
            
            p -= d_step
            
        g += e_step
