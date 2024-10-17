import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import stats
from collections import Counter
import pandas as pd
 #Usarei seed 100,200 e 300 nos testes



def Disparos(N, n):
    '''
    g: float | parâmetro da exponencial
    N: int | número de neurônios
    n: int | número de vazamentos

    returna uma matriz com os disparos de cada neurônio
    '''
    t = np.random.exponential(scale=1, size = (N, n))
    t_cumsum = np.cumsum(t, axis=1)

    return t_cumsum

def Vazamentos(g, N, n):
    '''
    g: float | parâmetro da exponencial
    N: int | número de neurônios
    n: int | número de vazamentos

    retorna uma matriz com os vazamentos de cada neurônio
    '''
    t = np.random.exponential(scale=g, size = (N, n))
    t_cumsum= np.cumsum(t, axis =1)
    
    return t_cumsum

def Passa_vizinhos(S, i):
    '''
    S: array | array de Status dos neurônios (ativos = 1, inativos = 0)
    i = indíce de disparo
    Tempo: O(1)
    '''
    S[i] = 0
    if i == len(S) - 1:
        pass
    else:
        S[i+1] = 1
    if i == 0:
        pass
    else:
        S[i - 1] = 1
    return S

def Zera(S, i):
    '''
    S: array | array de Status dos neurônios (ativos = 1, inativos = 0)
    i = indíce de vazamento
    Tempo: O(1)
    '''
    S[i] = 0
    return S

def Pega_min(S, N, ld, lv, d, v):
    '''
    S: array | array de Status dos neurônios (ativos = 1, inativos = 0)
    N: int | número de neurônios
    ld: int | índice atual utilizado para procurar em d o próximo disparo
    lv: int | índice atual utilizado para procurar em v o próximo vazamento
    d: np.array | matriz com o tempo dos disparos
    v: np.array | matriz com o tempo dos vazamentos
    
    '''
    #Criando uma lista com os próximos disparos e vazamentos
    listad = d[np.arange(N), ld] 
    listav = v[np.arange(N), lv]

    #Pegando o mínimo dessa lista
    mind = np.min(listad)
    minv = np.min(listav)

    #Coletando os índices dos mínimos
    id = np.argmin(listad)
    iv = np.argmin(listav)

    if  mind <= minv: #Caso o mínimo seja disparo
        if S[id] == 1: #Caso o neurônio esteja ativo
            S = Passa_vizinhos(S, id) 
        ld[id] += 1
    else: #Caso o mínimo seja vazamento
        if S[iv] == 1: #Caso esteja ativo
            S = Zera(S, iv)
        lv[iv] += 1
    
    return S, ld, lv
    

def Main(N, n, g, plot = False):
    '''
    N: int | número de neurônios utilizados
    n: int | número do tamanho da matriz
    g: float | valor da expornencial
    plot: bool | se pretende ver o gráfico da função
    '''
    S = [1]*N
    d = Disparos(N, n)
    v = Vazamentos(g, N, n)
    n_ativos =[sum(S)]
    x = range(len(n_ativos))
    ld = [0]*N
    lv = [0]*N
    t = 0

    plt.ion()
    
    while sum(S) > 0:
        S, ld, lv = Pega_min(S, N, ld, lv, d, v) #Pega o tempo mais recente na matriz
        n_ativos.append(sum(S))
        t += 1
        
        if plot and t%200 == 0: # Parte voltada pro gráfico
            plt.clf()
            x = range(len(n_ativos))
            print(t, (sum(S)))
            plt.plot(x, n_ativos, color = 'g', label = "Soma de Neurônios ativos")
            plt.plot(x, [np.mean(n_ativos)]*len(n_ativos), color = 'b', label = f"Média: {np.mean(n_ativos)}")
            plt.plot(x, [np.median(n_ativos)]*len(n_ativos), color = 'r', label = f"Mediana:{np.median(n_ativos)}")
            plt.plot(x, [stats.mode(n_ativos)[0]]*len(n_ativos), color = 'k', label = f"Moda:{stats.mode(n_ativos)[0]}")
            
            
            plt.legend()

            plt.ylim(0, N+1)
            plt.pause(0.0001)
    print("Resultado válido?", not np.max(ld) == n)
    print("Resultado válido?", not np.max(lv) == n)
    
    return t, not np.max(ld) == n, not np.max(lv) == n

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