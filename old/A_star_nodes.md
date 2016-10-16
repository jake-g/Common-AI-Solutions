


# A* Search
score = cost + heuristic
heuristic = lowest approx cost to goal
cost = sum edges from start to goal

cost is just last_cost + distance from parent

for distance it would be sqr(x^2+y^2), dont do sqrt


```
Class Node
  self.state  # (x, y) int
  self.heuristic # h float
  self.score # f float
  self.cost # g float
  self.kids
  self.mom  # parent Node

Class problem
  self.open
  self.closed
```
```
ALg:

// A*
from heapq import *

class Node(object):
    def __init__(self, x, y):
        self.g = 0
        self.h = 0
        self.parent = None
        self.x = x
        self.y = x

    def move_cost(self, other):
        diagonal = abs(self.x - other.x) == 1 and abs(self.y - other.y) == 1
        return 14 if diagonal else 10  # TODO is this ok


def pop_best_f_from_open() return q Node
def generate_kids(mom) return list of kids Nodes, check length is 8

def add_to_open(s):
    for n in open (search from smallest to larges score):
        if n.f < s.f and n.state == s.state:
            return False
    for n in closed:
        if n.state == s.state:
            return False
    return True

def generate_path(n):
    path = []
    while n.parent:
        path.append(n)
        n = n.parent
    return path.append(n)

nodes = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)] # other spots to hop to
open = []  # HEAP sort so in order of f (need contains and add)
closed = set() #(need push and contains)
start_node = Node(f=0, h=0)
heappush(open, start_node)

while open: # while open not empty
    curr = heappop(oheap)[1]
    if curr == goal:
        return generate_path(curr)  # skip last? [::-1]
    
    closed.add(curr)
    for node in nodes:
        node.g = curr.g + distance(node, curr)
        node.h = distance(node, goal)
        node.f = s.g + s.h

```

Old

```
open = {}  # sort so in order of f (need contains and add)
closed = [] (need push and contains)
start_node = Node(f=0)
open.add(start_node)

def pop_best_f_from_open() return q Node
def generate_kids(mom) return list of kids Nodes, check length is 8

def add_to_open(s):
    for n in open (search from smallest to larges score):
        if n.f < s.f and n.state == s.state:
            return False
    for n in closed:
        if n.state == s.state:
            return False
    return True
    
    if n in closed and n.g >= closed.get(n).g:


    if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:


while open # while open not empty
    q = pop_best_f_from_open()
    kids = generate_kids return(q)
    for s in kids:
    	if s.state is the goal:
            exit()

        s.g = q.g + distance between s and q
        s.h = distance from goal to s
        s.f = s.g + s.h

        if add_to_open(s):
            open.add(s)
    closed.push(q)
```