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

# calling function
delete_edges(10)

# drawing the graph with removed edges
nx.draw_networkx(G, pos=pos, node_size=1000, labels=labels)
plt.axis('off')
plt.show()

# function to define next 2 nodes
def find_next(adjacent: list, adjacent_next: list, finish: int, visited: list, graph):

  # setting minimal distance as all edges
  min_distance = graph.number_of_edges()
  first_step = None
  second_step = None

  # conversion to numbers
  if (type(finish) != int):
    visited_nodes = list(dict(((i, j), i + rows * j ) for i, j in visited).values())
    endpoint = finish[0] + rows * finish[1]
  else: 
    visited_nodes = visited
    endpoint = finish

  # among adjacent nodes choosing unvisited one, if it doesn't have adjacent skipping it
  # calculating distance from chosen till the end (node 3 and 7 - dist 4)
  for node in adjacent:
   if node not in visited_nodes:  
     if adjacent_next and not adjacent_next[node]:
       continue
     # if the calculated distance is less than previous minimum
     # setting it as minimum and comparing with it
     distance = int(math.fabs(endpoint - node))
     if (distance < min_distance): 
      min_distance = distance
      first_step = node
      # calling a function again to calculate 2nd step
      if adjacent_next:
       second_step = find_next(adjacent_next[node], {}, endpoint, visited_nodes, graph)
  # returning either 1 move
  if not second_step:
    return first_step
  
  # or 2
  return [first_step, second_step]


# Introducing knowledge_base
# get value from base
def get(knowledge_base: list, property: str):
  return knowledge_base[property]

# set value in base
def tell(knowledge_base: list, property: str, value):
  if (property == 'current'):
    knowledge_base[property] = value
  else: 
    knowledge_base[property].append(value)

# function to make a step back in case od a dead end
def steps_back(knowledge_base: list):
  print('Step back')
  visited = get(knowledge_base, 'visited')
  index = 2
  running = True

  while (index < len(visited) and running):
    current = get(knowledge_base, 'current')
    previous = visited[len(visited) - index]
    options = list(G.neighbors(previous))
    for u in options:
      if u not in visited:
        running = False
        break
      else:
        continue
    
    index = index + 1
    tell(knowledge_base, 'route', (current, previous))
    tell(knowledge_base, 'route_int', (current[0] + rows * current[1], previous[0] + rows * previous[1]))
    print(get(knowledge_base, 'route_int'))
    tell(knowledge_base, 'current', previous)
    
  print('Moving on:')

# function to define a move depending on command
def ask(knowledge_base: list, adjacent: list, adjacent_next: list, finish: int, case: str):
  # final node is next
  if case == 'Finish in 1 step':
    current = get(knowledge_base, 'current')
    tell(knowledge_base, 'plan', (current, finish))
    tell(knowledge_base, 'route', (current, finish))
    tell(knowledge_base, 'route_int', (current[0] + rows * current[1], finish[0] + rows * finish[1]))
    print(get(knowledge_base, 'route_int'))
  
  # final node is adjacent to the next
  elif case == 'Finish in 2 steps':
    current = get(knowledge_base, 'current')
    plan = get(knowledge_base, 'plan')

    for i in adjacent:
      tell(knowledge_base, 'plan', (current, i))
      adjacent_next[i] = list(G.neighbors(i))
      for u in adjacent_next[i]:
        # if necessary updating plan
        if (i, u) not in plan:
          tell(knowledge_base, 'plan', (i, u))
        # adding info to the base
        if (u == finish):
          tell(knowledge_base, 'route', (current, i))
          tell(knowledge_base, 'route_int', (current[0] + rows * current[1], i[0] + rows * i[1]))
          print(get(knowledge_base, 'route_int'))
        
          tell(knowledge_base, 'route', (i, u))
          tell(knowledge_base, 'route_int', (i[0] + rows * i[1], u[0] + rows * u[1]))
          print(get(knowledge_base, 'route_int'))
          # returning true to exit loop in agent
          return True

  # final node is out of reach yet
  elif case == 'Define next step':
    adjacent_int = list(dict(((i, j), i + rows * j ) for i, j in adjacent).values())
    adjacent_next_int = {}
    for key, value in adjacent_next.items():
      key = key[0] + rows * key[1]
      value = list(dict(((i, j), i + rows * j ) for i, j in value).values())
      adjacent_next_int.update({key: value})

    # choosing 2 next steps
    steps = find_next(adjacent_int, adjacent_next_int, finish, get(knowledge_base, 'visited'), G)
    if (not steps):
      steps_back(knowledge_base)
      return True
    elif(type(steps) is int):
      first_step_int = steps
      second_step_int = None
    else:
      first_step_int = steps[0]
      second_step_int = steps[1]
    
    # adding info to the base
    index1 = adjacent_int.index(first_step_int)
    first_step = adjacent[index1]
    current = get(knowledge_base, 'current')
    tell(knowledge_base, 'route', (current, first_step))
    tell(knowledge_base, 'route_int', (current[0] + rows * current[1], first_step_int))
    tell(knowledge_base, 'visited', first_step)
    tell(knowledge_base, 'current', first_step)
    
    if(second_step_int):
      value = adjacent_next_int[first_step_int]
      index2 = value.index(second_step_int)
      second_step = adjacent_next[first_step][index2]
      tell(knowledge_base, 'route', (first_step, second_step))
      tell(knowledge_base, 'route_int', (first_step_int, second_step_int))
      print(knowledge_base['route_int'])
      tell(knowledge_base, 'visited', second_step)
      tell(knowledge_base, 'current', second_step)
    
# colors for visited nodes and edges
colors = []

# empty knowledge base
knowledge_base = {
  'current': (0, 0),
  'visited': [],
  'plan': [],
  'route': [],
  'route_int': [],
}

# agent function
def agent(start: tuple, finish: tuple, G): 
  finish_int = finish[0] + rows * finish[1]
  start_int = start[0] + rows * start[1]

  tell(knowledge_base, 'current', start) 
  tell(knowledge_base, 'visited', start) 

  current = get(knowledge_base, 'current')

  # starting a loop while current node isn't final
  while(current != finish):
    route_completed = False
    adjacent = list(G.neighbors(get(knowledge_base, 'current')))
    adjacent_next = {}

    # if final is adjacent to current calling Finish in 1
    if finish in adjacent:
      ask(knowledge_base, adjacent, adjacent_next, finish, 'Finish in 1 step')
      break

    # if final is in 2 steps calling Finish in 2
    route_completed = ask(knowledge_base, adjacent, adjacent_next, finish, 'Finish in 2 steps')
    if route_completed:
      break

    # Choosing next step, in case of dead end skipping an iteration
    need_to_go_back = ask(knowledge_base, adjacent, adjacent_next, finish, 'Define next step')
    if need_to_go_back:
      continue

  #filling colors
  for u,v in G.edges():
    if (u,v) in knowledge_base['route'] and (v,u) in knowledge_base['route']:
        colors.append('red')
    elif (u,v) in knowledge_base['route'] or (v,u) in knowledge_base['route']:
        colors.append('blue')
    else: 
        colors.append('black')
        
# calling agent
agent((0, 0), (4, 4), G)
# drawing the shortest path
nx.draw_networkx(G, pos=pos, node_size=1000, edge_color=colors, labels=labels)
plt.axis('off')
plt.show()
