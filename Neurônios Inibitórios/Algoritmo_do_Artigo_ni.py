import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

def Main(S, g, val, plot=False, t_up_plot=50000):
    '''
    Simulação altamente otimizada usando arrays NumPy e tracking dinâmico.
    '''
    N = S.number_of_nodes()
    
    # Abandonei o Networkx, vamos apenas receber o grafo e extrair sua topologia
    adj = [list(S.neighbors(i)) for i in range(N)]

    is_inhibitory = np.zeros(N, dtype=bool)
    is_inhibitory[val] = True
    

    state = np.ones(N, dtype=int) #Os estados dos neurônios (ativos ou inativos)
    s = N                         
    
    t = 0.0
    n = 0
    
    # Primeiros tempos sorteados
    d = np.random.exponential(1.0 / s)
    v = np.random.exponential(1.0 / (s * g))
    
    n_ativos = [s] # Variável de tracking para o plot
    
    while s > 0:
        active_indices = np.nonzero(state)[0]
        
        if v < d:
            t = v
            # Vazamento
            i = np.random.choice(active_indices)
            state[i] = 0
            s -= 1
            v = t + np.random.exponential(1.0 / (s * g))
            
        else:
            t = d
            # Disparo
            i = np.random.choice(active_indices)
            state[i] = 0
            s -= 1
            
            # Propagação para os vizinhos
            if is_inhibitory[i]:
                for viz in adj[i]:
                    if state[viz] == 1:
                        state[viz] = 0
                        s -= 1
            else: # Excitatório
                for viz in adj[i]:
                    if state[viz] == 0:
                        state[viz] = 1
                        s += 1
            d = t + np.random.exponential(1.0 / s)
    return t
