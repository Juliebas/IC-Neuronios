import sys
sys.path.insert(1, '/home/julio/Modelos/IC-Neuronios/Neurônios Inibitórios/')
from Algoritmo_do_Artigo_ni import Main as A
import scipy as sc
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time


g = 1.5 #Gama Inicial
a = 1
ps = 1
pi = 0
prec = 1/100

d = 100 #Divisão de probabilidades e Gamas
results = {} #Resultados do teste
with open('resultados.txt', 'a') as f: #Abre o .txt dos resultados
    f.write('Novo registro: \n')
    T = True
    ps = 1
    pi = 0
    while ps - pi > prec: #Vai repartir o gama e a probabilidade em d partes
        pk = (ps + pi)/2
        f.write("\n") #Pula linha
        T = time.time()
        AA = [] #Lista de amostra
        for k in range (500): #Repetição da Amostra
            AA += [A(nx.convert_node_labels_to_integers(nx.grid_2d_graph(12, 12), ordering='sorted'), 1, pk)] #Testa uma grid de neurônios inibitórios 
            print("p: ", pk, "| g: ", 1, "| amostra: ",k, "| t: ", AA[k])
        #print(np.mean(AA))
        AA = AA/np.mean(AA) #Normaliza essa amostra
        #print(AA)
        #time.sleep(60)
        result = sc.stats.kstest(AA, sc.stats.expon.cdf) #Verifica se parece com a Exponencial
        if result.pvalue < 0.05:
            ps = pk
            results[(1, pk)] = 0
            f.write(f"g: 1, p: {pk}: 0")
        else:
            pi = pk
            results[(1, pk)] = 1
            f.write(f"g: 1, p: {pk}: 1")
        print(result.pvalue)
        print(f"dicionário: {results}\n")
        print("PK>>>>>>>>>>>>>>>", pk)
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