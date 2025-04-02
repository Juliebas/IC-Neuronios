import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import networkx as nx

plt.ion()

def Main(N, g, type_graph = 'path', p_ER = 0.5, plot = False, t_up_plot = 1000):
    '''
    Main simplificada buscando optimização do código

    N : int | número de neurônios
    g : float | gama da exponencial que dita a frequência de vazamentos
    type_graph : str | tipo de grafo que será usado ('path', 'ER')
    p_ER : float | probabilidade de vizinhança no caso grafo Erdos Renyi
    plot : bool | True se a função exibirá plot, False se não exibirá
    t_up_plot: int | tempo de passos até exibir o gráfico da função

    retorna o tempo para o processo morrer
    '''

    if type_graph == 'path':
        S = nx.path_graph(N) #Caso grafo de linha
    elif type_graph == 'ER':
        S = nx.erdos_renyi_graph(N, p_ER) #Caso grafo ER


    # Essa parte de cima será mudada futuramente e a Main() só receberá S


    t = 0
    n = 0
    for i in range(N):
        S.nodes[i]['value'] = 1  #Todos os neurônios começam ativos
    for i in range(N):
        d = np.random.exponential(1, size= N) #Cria o tempo de disparo aleatorio seguindo uma Exponencial
        v = np.random.exponential(g, size= N) #Idem com vazamento
    s = sum(nx.get_node_attributes(S, 'value').values()) #s é a soma de neurônios ativos
    n_ativos =[s]
    ind = 0
    while s != 0:
        ind += 1
        minv = min(v) #Pega o menor tempo de vazamentos e disparos
        mind = min(d)
        if minv < mind: #Compara eles
            t = minv
            i = np.where(v == t)[0][0]
            S.nodes[i]['value'] = 0
            v[i] = t + np.random.exponential(g) #Caso o vazamento menor o neuronio ganha outro tempo de vazamento
        else:
            t = mind
            i = np.where(d == t)[0][0]
            S.nodes[i]['value'] = 0
            for vizinhos in S.neighbors(i): #Caso disparo menor os neuronios vizinhos ativam e o neuronio ganha um novo tempo de disparo enquanto o mesmo zera
                S.nodes[vizinhos]['value'] = 1
            d[i] = t + np.random.exponential(1)
        s = sum(nx.get_node_attributes(S, 'value').values())
        n_ativos += [s]

        '''
        Parte voltada para o gráfico
        '''

        if plot and n%t_up_plot == 0:
            plt.clf()
            x = range(len(n_ativos))
            node_colors = ['red' if S.nodes[node]['value'] == 1 else 'blue' for node in S.nodes()]
            plt.subplot(2, 1, 1)
            plt.plot(x, n_ativos, color = 'g', label = "Soma de Neurônios ativos")
            plt.plot(x, [np.mean(n_ativos)]*len(n_ativos), color = 'b', label = f"Média: {np.mean(n_ativos)}")
            plt.plot(x, [np.median(n_ativos)]*len(n_ativos), color = 'r', label = f"Mediana:{np.median(n_ativos)}")
            plt.plot(x, [stats.mode(n_ativos)[0]]*len(n_ativos), color = 'k', label = f"Moda:{stats.mode(n_ativos)[0]}")
            plt.legend()
            plt.ylim(0, N+1)
            plt.subplot(2, 1, 2)
            nx.draw(S, pos = nx.circular_layout(S), node_color= node_colors)
            plt.pause(0.01)
        n += 1

    plt.ioff()

    return t

Main(100, 2, 'path', plot= True)