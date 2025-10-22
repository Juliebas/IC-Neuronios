import sys
sys.path.insert(1, '/home/julio/Projects/IC-Neuronios/Neurônios Inibitórios/')
from Algoritmo_do_Artigo_ni import Main as A
import scipy as sc
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time


p = 1 #Probabilidade inicial
g = 1.5 #Gama Inicial

d = 10 #Divisão de probabilidades e Gamas
results = {} #Resultados do teste
with open('resultados.txt', 'w') as f: #Abre o .txt dos resultados
    T = True 
    for i in range(1, d+1, 1): #Vai repartir o gama e a probabilidade em d partes
        f.write("\n") #Pula linha
        j = d
        T = True
        while T and j > 0 : #Se T é verdadeiro e d é positivo
            AA = [] #Lista de amostra
            for k in range (100): #Repetição da Amostra
                AA += [A(nx.convert_node_labels_to_integers(nx.grid_2d_graph(10, 10), ordering='sorted'), 1/(i*g/d), j*p/d)] #Testa uma grid de neurônios inibitórios 
                print("p: ", j*p/d, "| g: ", i*g/d, "| amostra: ",k, "| t: ", AA[k])
            print(np.mean(AA)) 
            AA = AA/np.mean(AA) #Normaliza essa amostra
            print(AA)

            #time.sleep(60)
            result = sc.stats.kstest(AA, sc.stats.expon.cdf) #Verifica se parece com a Exponencial
            if result.pvalue < 0.05:
                results[(i*g/d, j*p/d)] = 0
            else:
                results[(i*g/d, j*p/d)] = 1
                T = False
            f.write(f"{results[(i*g/d, j*p/d)]}")
            print(result.pvalue)
            j -= 1
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