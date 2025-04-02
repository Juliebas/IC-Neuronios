import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import networkx as nx
import time
 #Usarei seed 100,200 e 300 nos testes


def Disparos(N, n):
    '''
    N: int | número de neurônios
    n: int | número de disparos

    returna uma lista exponencial
    '''
    t = np.random.exponential(scale = 1/N, size = n) #Mudar a array, tem que ser por While, a exponencial é feita a cada passo
    t_cumsum = np.cumsum(t)

    return t_cumsum

def Vazamentos(g, N, n):
    '''
    g: float | parâmetro da exponencial
    N: int | número de neurônios
    n: int | número de vazamentos

    returna umas lista exponencial
    '''
    t = np.random.exponential(scale=g/N, size = n) #Mudar a array, tem que ser por While, a exponencial é feita a cada passo
    t_cumsum= np.cumsum(t)
    
    return t_cumsum

def Passa_vizinhos(S, i):
    '''
    S: grafo | grafo de status dos neurônios (ativos = 1, inativos = 0)
    i: indíce de disparo
    Tempo: O(1)
    '''
    S.nodes[i]['value'] = 0
    for vizinho in S.neighbors(i):
        S.nodes[vizinho]['value'] = 1
    
    return S

def Zera(S, i):
    '''
    S: array | array de Status dos neurônios (ativos = 1, inativos = 0)
    i = indíce de vazamento
    Tempo: O(1)
    '''
    S.nodes[i]['value'] = 0
    return S

def Pega_min(S, N, d, v):
    '''
    S: array | grafo de Status dos neurônios (ativos = 1, inativos = 0)
    N: int | número de neurônios
    d: np.array | matriz com o tempo dos disparos
    v: np.array | matriz com o tempo dos vazamentos
    
    '''

    #Pegando o mínimo dessa lista
    mind = d[0]
    minv = v[0]

    i = np.random.choice(range(N))

    if  mind <= minv: #Caso o mínimo seja disparo
        if S.nodes[i]['value'] == 1: #Caso o neurônio esteja ativo
            S = Passa_vizinhos(S, i)
        d = d[1:]
    else: #Caso o mínimo seja vazamento
        if S.nodes[i]['value'] == 1: #Caso esteja ativo
            S = Zera(S, i)
        v = v[1:]
    
    return S, d, v
    
def Main(N, n, g, plot = False, int_graph = 1000, type = 'path', p = 0.5):
    '''
    N: int | número de neurônios utilizados
    n: int | número do tamanho da matriz
    g: float | valor da expornencial
    plot: bool | se pretende ver o gráfico da função
    int_graph
    '''
    start = time.time()
    if type == 'path':
        S = nx.path_graph(N)
    elif type == 'ER':
        S = nx.erdos_renyi_graph(N, p)
    for node in S.nodes():
        S.nodes[node]['value'] = 1
    d = Disparos(N, n)
    v = Vazamentos(g, N, n)
    n_ativos =[sum(nx.get_node_attributes(S, 'value').values())]
    x = range(len(n_ativos))
    t = 0

    plt.ion()
    
    while sum(nx.get_node_attributes(S, 'value').values()) > 0:
        S, d, v = Pega_min(S, N, d, v) #Pega o tempo mais recente na matriz
        n_ativos.append(sum(nx.get_node_attributes(S, 'value').values()))
        t += 1
        if t == 1000000:
            end = time.time()
            print("Tempo desse processo:", end - start)


        if plot and t%int_graph == 0: # Parte voltada pro gráfico
            plt.clf()
            x = range(len(n_ativos))
            print(t, (sum(nx.get_node_attributes(S, 'value').values())))
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
            plt.pause(0.0001)
    #print("Resultado válido?", not len(d) == 0)
    #print("Resultado válido?", not len(v) == 0)

    plt.ioff()
    
    return t, not len(d) == 0, not len(v) == 0

'''

IGNORE AQUI PRA BAIXO, UTILIZADO PARA REALIZAR OS PRIMEIROS TESTES

'''

def amostra ():
    T = 5000
    n = 5000
    lista = []
    for i in range (200):
        N = int(np.random.uniform(0, 1000)//1)
        g = np.random.uniform(0, 20)
        m = Main(N, n, g, T)
        print(i)
        lista += [[g, N, m]]
    df = pd.DataFrame(lista)
    with pd.ExcelWriter("Simulação1.xlsx") as writer:
        df.to_excel(writer, sheet_name="dados2")

Main(100, 1000000, 2, plot = True, int_graph = 1000, type = 'path', p = 0.5)