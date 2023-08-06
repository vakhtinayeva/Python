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

# setting the max number of nodes to delete
max_deleted = rows*columns - rows - columns + 1

# function to remove edges
def delete_edges(num: int):
  # quantity to delete
  to_delete = num
  # deleted counter
  deleted = 0

  # checking if the number's within limits
  if to_delete > max_deleted:
    print('Impossible. Max allowed number is: %d' %max_deleted)
    return

  while deleted < to_delete:
    # converting edges into list
    edges = list(G.edges)
    # choosing random edge
    cur_edge = random.choice(edges)
    # removing it
    G.remove_edge(cur_edge[0], cur_edge[1])
    # checking if the graph's still connected
    connected = nx.is_connected(G)
    
    # adding 1 to counter and continuing
    if connected:
      deleted += 1
    # or returning the edge and trying again
    else:
      G.add_edge(cur_edge[0], cur_edge[1])

# calling functrion
delete_edges(10)

# drawing the graph with removed edges
nx.draw_networkx(G, pos=pos, node_size=1000, labels=labels)
plt.axis('off')
plt.show()
