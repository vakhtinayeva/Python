import networkx as nx
import random
import matplotlib.pyplot as plt

# number of rows and columns
rows = 5
columns = 5

# creating graph where every node is connected with neighbours
G = nx.grid_2d_graph(columns, rows)

# dictionary with nodes positions
pos = dict((n, n) for n in G.nodes())

# giving names-numbers to nodes
labels = dict(((i, j), i * rows + j ) for i, j in G.nodes())

# drawing the graph
nx.draw_networkx(G, pos=pos, node_size=1000, labels=labels)
plt.axis('off')
plt.show()
