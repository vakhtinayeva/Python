# Python
 Graphs AI in Python consisting of 3 parts

# Part 1
- Generate a graph (grid representing a road) of a specific size (rows x columns)
- Remove a specific amount of edges keeping the graph connected

# Part 2
Create an agent (car) moving from point A to B through the graph (road)

An agent has certain limitations:

- agent sees only the node it's currently located in and edges leading to adjacent nodes
- can go straight, turn left/right/180, stop
- keeps track of visited nodes and agents
- can move between nodes only along edges
- knows coordinates of start and finish but not of a full map

# Part 3
Create a knowledge-based agent moving from point A to B through the graph along the road

Add a knowledge base to previous algorithm to give agent access to 3 operations

- TELL - record data discovered along the way
- ASK  - request information about what move to make
- DO   - perform requested move

Agent can avoid dead ends, walking in circles and now 'sees' 2 steps in advance
