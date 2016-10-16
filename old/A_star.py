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

class Problem(object):
    def __init__(self, graph):
        self.graph = graph

    def heuristic(self, node, start, end):
        return (end.x - node.x)**2 + (end.y - node.y)**2

    def generate_path(n):
        path = []
        while n.parent:
            path.append(n)
            n = n.parent
        return path.append(n)

    def search(self, start, end):
        O = set()
        C = set()
        curr = start
        O.add(curr)
        while O: # open not empty
            curr = min(O, key=lambda o:o.g + o.h # most fit from open
            if curr == end:
                generate_path(curr)
                return path[::-1]  # why?
            O.remove(curr)
            C.add(curr)
            for k in self.graph[curr]: # for each kid of current
                if k in C: # SKIP: already saw in and its kids
                    continue

                new_g = curr.g + curr.move_cost(k) # is move_cost fcn necessary
                k.parent = curr
                if k in O: # already saw, update if better g score
                    if k.g > new_g:
                        k.g = new_g
                else:  # never seen... investigate
                    k.g = new_g
                    k.h = self.heuristic(n, start, end)
                    O.add(k)
        return None
