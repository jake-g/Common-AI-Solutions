depth first, but stop depth diving if you encounter the same var as the prev
var

keep prev var stored to compare to next var...No repeated states
Count n of states...what the fuck counting rules....dont get it
```

    
    double    
    00W
    11W
    22W
    33W
    
    starts with 0
    01W
    02W
    03W
    
    starts with 3
    30W
    31W
    32W
    
    starts wit 1 or 2
    10L
    12L
    13L
    20L
    21L
    23L

def depthFirstSearch(problem):
    fringe = util.Stack()
    fringe.push( (problem.getStartState(), [], []) )
    while not fringe.isEmpty():
        node, actions, visited = fringe.pop()

        for coord, direction, steps in problem.getSuccessors(node):
            if not coord in visited:
                if problem.isGoalState(coord):
                    return actions + [direction]
                fringe.push((coord, actions + [direction], visited + [node] ))

    return []
```
