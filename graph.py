import networkx as nx
import random
import matplotlib.pyplot as plt
import math

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

# colors for visited nodes
colors = []

# function to search for next available step
def find_next(nodes: list, finish: tuple, visited: list, graph):
  # conversion into numbers
  visited_nodes = list(dict(((i, j), i + rows * j ) for i, j in visited).values())
  endpoint = finish[0] + rows * finish[1]
  # min ditanse - the general num of edges
  min_distance = graph.number_of_edges()
  next_node = None

  # among adjacent nodes choosing an unvisited
  # and calculating the distance to the end (node 3 and 7 - dist 4)
  for node in nodes:
    if node not in visited_nodes:
      distance = int(math.fabs(endpoint - node))
      # if calculated distance is less than previous minimum
      # setting it as minimum and compare to it   
      if (distance < min_distance): 
        min_distance = distance
        next_node = node
  return next_node

# function - agent
def agent(start: tuple, finish: tuple, graph): 
  #conversion into numbers
  finish_int = finish[0] + rows * finish[1]
  start_int = start[0] + rows * start[1]

  current = start
  current_int = start_int

  visited = [start]
  next_node = start

  route = []
  route_int = []

  # start while current node isn't final, continuing
  print('Start: ', start_int)
  while(current != finish):
    adjacent = list(graph.neighbors(current))
    adjacent_int = list(dict(((i, j), i + rows * j ) for i, j in graph.neighbors(current)).values())

    # if final node in adjacent adding it to the route and exiting
    if finish in adjacent:
      route.append((current, finish))
      route_int.append((current_int, finish_int))
      print(route_int)
      print(route)
      print('Finish: ', finish_int)
      break
    
    # otherwise choosing next step
    next_node_int = find_next(adjacent_int, finish, visited, graph)

    # in case of dead end, stepping back and making a mark
    if (not next_node_int):
      print('Step back')
      index = visited.index(current)
      previous = visited[index - 1]

      route.append((current, previous))
      current = previous
      current_int = current[0] + rows * current[1]
      continue
    
    # after choosing next, adding it to route, marking as visited and setting as current
    index = adjacent_int.index(next_node_int)
    next_node = adjacent[index]
    route.append((current, next_node))
    route_int.append((current_int, next_node_int))

    visited.append(next_node)
    current = next_node
    current_int = current[0] + rows * current[1]
    print(route_int)

  # filling colors
  for u, v in graph.edges():
    if (u, v) in route and (v, u) in route:
        colors.append('red')
    elif (u, v) in route or (v, u) in route:
        colors.append('blue')
    else: 
        colors.append('black')   
        
# calling the agent
agent((0, 0), (2, 1), G)
# drawing the route
nx.draw_networkx(G, pos=pos, node_size=1000, edge_color=colors, labels=labels)
plt.axis('off')
plt.show()