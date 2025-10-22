import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import networkx as nx
import random

random.seed(42)

plt.ion()

def Main(S, g, p, plot = False, t_up_plot = 50000):
    '''
    Main simplificada buscando optimização do código

    S : graph | grafo formado com networkx
    g : float | gama da exponencial que dita a frequência de vazamentos
    p : float | proporção de neurônios inibitórios
    plot : bool | True se a função exibirá plot, False se não exibirá
    t_up_plot: int | tempo de passos até exibir o gráfico da função

    retorna o tempo para o processo morrer
    '''

    # Retirei o S
    N = S.number_of_nodes()
    t = 0
    n = 0
    val = random.choices(list(S.nodes()), k = int(N*p))
    for i in range(N):
        S.nodes[i]['value'] = 1  #Todos os neurônios começam ativos
        if i in val:             #Tipo do neurônio
            S.nodes[i]['tipo'] = "I"
        else:
            S.nodes[i]['tipo'] = "E" 
        
    s = sum(nx.get_node_attributes(S, 'value').values()) #s é a soma de neurônios ativos
    for i in range(N):
        d = np.random.exponential(1/s) #Cria o tempo de disparo aleatorio seguindo uma Exponencial
        v = np.random.exponential(g/s) #Idem com vazamento
    n_ativos =[s]
    while s != 0:
        if v < d: #Compara o tempo do vazamento e do disparo
            t = v
            i = np.random.choice([n for n in list(S.nodes()) if S.nodes[n]['value'] == 1]) #Escolhe um neuronio para vazamento
            S.nodes[i]['value'] = 0
            v = t + np.random.exponential(g/s) #Caso o vazamento menor o neuronio ganha outro tempo de vazamento
        else:
            t = d
            i = np.random.choice([n for n in list(S.nodes()) if S.nodes[n]['value'] == 1]) #Escolhe um neuronio para disparo
            S.nodes[i]['value'] = 0 #Se auto-desativa
            for vizinhos in S.neighbors(i): #Caso disparo menor os neuronios vizinhos ativam e o neuronio ganha um novo tempo de disparo enquanto o mesmo zera
                if S.nodes[i]['tipo'] == "E":
                    S.nodes[vizinhos]['value'] = 1
                else:
                    S.nodes[vizinhos]['value'] = 0
            d = t + np.random.exponential(1/s)
        s = sum(nx.get_node_attributes(S, 'value').values())
        n_ativos += [s]

        '''
        Parte voltada para o gráfico
        '''
        if plot and n%t_up_plot == 0:
            plt.clf()
            x = range(len(n_ativos))
            node_colors = ['red' if S.nodes[node]['value'] == 1 else 'blue' for node in S.nodes()]
            nodes_s = [i for i in S.nodes() if S.nodes[i]['tipo'] == 'I']
            nodes_o = [i for i in S.nodes() if S.nodes[i]['tipo'] == 'E']
            plt.subplot(2, 1, 1)
            plt.plot(x, n_ativos, color = 'g', label = "Soma de Neurônios ativos")
            #plt.plot(x, [np.mean(n_ativos)]*len(n_ativos), color = 'b', label = f"Média: {np.mean(n_ativos)}")
            #plt.plot(x, [np.median(n_ativos)]*len(n_ativos), color = 'r', label = f"Mediana:{np.median(n_ativos)}")
            #plt.plot(x, [stats.mode(n_ativos)[0]]*len(n_ativos), color = 'k', label = f"Moda:{stats.mode(n_ativos)[0]}")
            plt.legend()
            plt.ylim(0, N+1)
            #plt.subplot(2, 1, 2)
            #nx.draw(S, pos = nx.spring_layout(S, seed= 42), node_color= [node_colors[i] for i in nodes_s], nodelist = nodes_s, node_shape = "s")
            #nx.draw(S, pos = nx.spring_layout(S, seed= 42), node_color= [node_colors[i] for i in nodes_o], nodelist = nodes_o, node_shape = "o")
            plt.pause(0.01)
        n += 1

    plt.ioff()

    #plt.plot(range(len(n_ativos)), n_ativos, color = 'g', label = "Soma de Neurônios ativos")
    #plt.plot(range(len(n_ativos)), [np.mean(n_ativos)]*len(n_ativos), color = 'b', label = f"Média: {np.mean(n_ativos)}")
    #plt.show()

    return t