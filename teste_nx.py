import networkx as nx
import matplotlib.pyplot as plt

# Criando um grafo simples
G = nx.erdos_renyi_graph(5, 0.5)

# Escolhendo um nó para analisar
for node in range(4):
    print(f"Conexões do nó {node}:")
    for neighbor in G.neighbors(node):
        print(neighbor)

nx.draw(G, with_labels = True)
plt.show()