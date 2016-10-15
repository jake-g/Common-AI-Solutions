


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
