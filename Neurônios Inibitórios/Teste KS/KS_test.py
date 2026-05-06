import sys
sys.path.insert(1, '/home/julio/Modelos/IC-Neuronios/Neurônios Inibitórios/')
from Algoritmo_do_Artigo_ni import Main as A
import scipy as sc
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas


g = 1
e = 0.1
d = 0.01 #Divisão de probabilidades e Gamas
results = {} #Resultados do teste
results[(g,1)] = 0
results[(g, 0.99)] = 0
with open('resultados.txt', 'a') as f: #Abre o .txt dos resultados
    f.write('Novo registro: \n')
    while g < 2:
        T = True
        U = True
        p = 1
        p-= 2*d
        S = nx.convert_node_labels_to_integers(nx.grid_2d_graph(12, 12), ordering='sorted')
        N = S.number_of_nodes()
        val = random.choices(list(S.nodes()), k = int(N*p))
        while T or U: #Vai repartir a probabilidade em d partes
            while int(N*p) < len(val):
                random_index = random.randrange(len(val))
                val.pop(random_index)
            f.write("\n") #Pula linha
            AA = [] #Lista de amostra
            print(val)
            for k in range (500): #Repetição da Amostra
                AA += [A(S, g, val, plot = False)] #Testa uma grid de neurônios inibitórios
                print("p: ", round(p,2), "| g: ", g, "| amostra: ",k, "| t: ", AA[k])
            #print(np.mean(AA))
            AA = AA/np.mean(AA) #Normaliza essa amostra
            #print(AA)
            #time.sleep(60)
            result = sc.stats.kstest(AA, sc.stats.expon.cdf) #Verifica se parece com a Exponencial
            if result.pvalue < 0.05:
                results[(g, round(p, 2))] = 0
                f.write(f"g: {g} p: {round(p, 2)}: 0")
            elif T and result.value >= 0.05:
                results[(g, round(p, 2))] = 1
                f.write(f"g: {g} p: {round(p, 2)}: 1")
                T = False
            else:
                results[(g, round(p, 2))] = 1
                f.write(f"g: {g} p: {round(p, 2)}: 1")
                U = False
            print(result.pvalue)
            print(f"dicionário: {results}\n")
            print("P>>>>>>>>>>>>>>>", round(p, 2))
            p -= d
        g += e
'''
grid = np.zeros((d, d)) 

for (j_val, i_val), value in results.items():
    i_idx = int(i_val * d / p)  # converte p/d para índice
    j_idx = int(j_val * d / g)  # converte g/d para índice
    grid[i_idx, j_idx] = value

plt.imshow(grid, cmap='Greys', origin='lower')
plt.title("Resultados do KS Test")
plt.xlabel("Proporção de Inibitórios (j*g/d)")
plt.ylabel("Probabilidade de Disparo (i*p/d)")
plt.colorbar(label="KS Aceita (1) ou Rejeita (0)")
plt.xticks(ticks=range(d), labels=[f"{j*g/d:.2f}" for j in range(d)])
plt.yticks(ticks=range(d), labels=[f"{i*p/d:.2f}" for i in range(d)])
plt.grid(False)
plt.show()
'''