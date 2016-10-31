# A* Pathfinding Problem
#   Jake Garrison
#   UW EE 562
#   HW 2

import math
from heapq import *


class Map:
    # Class to parse map file into map object
    def get_point(self, line):
        return tuple([self.scale * x for x in map(int, line.split())])

    def get_rectangle(self, line):
        arr = [self.scale * x for x in map(int, line.split())]
        rect = zip(arr[0::2], arr[1::2])
        return rect

    def get_lines_from_rect(self, r):
        return [(r[0], r[1]), (r[0], r[3]), (r[0], r[2]), (r[2], r[1]), (r[2], r[3]), (r[1], r[3])]

    def __init__(self, f, scale=1):
        self.nodes = set()
        self.lines = []
        self.rects = []  # optional for visual display
        self.scale = scale  # optional for visual display= []

        # Parse file into Map object
        with open(f) as f:
            for i, line in enumerate(f):
                line = line.strip()
                if i is 0:
                    self.start = self.get_point(line)
                elif i is 1:
                    self.goal = self.get_point(line)
                elif i is 2:
                    self.n_rects = int(line.strip())
                else:
                    rect = self.get_rectangle(line)
                    self.lines.extend(self.get_lines_from_rect(rect))
                    self.nodes |= set(rect)
                    self.rects.append(rect)


class Problem:
    # Class to initialize data structures and map condititions
    def __init__(self, m):  # Problem database
        self.start = m.start
        self.goal = m.goal
        self.nodes = m.nodes  # all nodes (rectangle corners)
        self.open = []  # need to explore
        self.closed = set()  # already explored
        self.lines = m.lines  # set of possible lines
        self.parent = {}  # dictionary of node -> parent
        self.cost = {}  # cost to get to this node from start
        self.score = {}  # score = g(n) + h(n)


# Returns distance between points
def distance(start, end):  # heuristic distance from a to b
    return math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) # technically dont need sqrt


# Checks if line1 intersects line2
# this *could* be optimize and written more concisely
def intersect(A, B, C, D):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    def on_line(line, p):  # C is on AB if distance(A,C) + distance(B,C) = length(AB)
        if line[0] == p or line[1] == p:
            return False
        return distance(line[0], p) + distance(line[1], p) == distance(line[0], line[1])

    # Check if comparing line AB to line AB or other permutaitons of AB
    if sorted((A, B)) == sorted((C, D)):  # same segment
        return False

    # Dont count two lines on a rect corner as an intersection
    if A == C or A == D or B == C or B == D:
        return False

    # Edge Case: If CD from another rect touchs somwhere on a AB, but doesn't go trhough AB, it is still an intersection
    if on_line((A, B), C) or on_line((A, B), D) or on_line((C, D), A) or on_line(
            (C, D), B):
        return True

    # Last case finds most intersections (aside from edge case above
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def illegal(start, end, lines):
    # Check if start and end intersect with any lines
    for l in lines:
        if intersect(start, end, l[0], l[1]):
            return True
    return False


def print_path(path, cost):
    # Print the final path
    print 'Best Path:'
    print 'Point\t\t\tCost'
    for n in path[::-1]:  # reverse iterate
        print n, ' \t\t', cost.get(n)


def astar(p):
    # Init
    p.cost[p.start] = 0;  # cost to start node
    p.score[p.start] = distance(p.start, p.goal) # score (cost to goal)
    heappush(p.open, (p.score[p.start], p.start))  # use priority heap

    # Search
    while p.open:
        curr = heappop(p.open)[1]  # get node to expand
        print '\nOn Node:', curr

        if curr == p.goal:  # check if at goal
            path = []  # build reverse path by following parent chain
            while curr in p.parent:
                path.append(curr)
                curr = p.parent[curr]
            path.append(p.start)
            print_path(path, p.cost)
            return path[::-1]  # reverse path to be in order

        p.closed.add(curr)  # add curr to close since we are expanding
        for node in p.nodes:  # search all nodes for possible path
            if curr == node:  # skip same node
                continue

            if node in p.closed and node_cost >= p.cost.get(node, 0):  # skip if seen better cost
                print 'Already Saw better: ', curr, node
                continue

            if illegal(curr, node, p.lines):  # skip if illegal move
                continue

            node_cost = p.cost[curr] + distance(curr, node)  # legal move! look at heuristic
            print 'Safe move:', curr, 'to', node

            if node_cost < p.cost.get(node, 0) or node not in [n[1] for n in p.open]:
                p.parent[node] = curr
                p.cost[node] = node_cost
                p.score[node] = node_cost + distance(node, p.goal)
                dist = distance(node, p.goal)
                print 'Cost to here:', node_cost
                print 'Distance to goal:', dist
                print 'Score:', node_cost + dist
                heappush(p.open, (p.score[node], node))  # this node is worth investigating, expand later
            else:
                print 'Cheaper option exists'  # not worth expanding

    return False  # No solution!


if __name__ == '__main__':
    map = Map('data_personal.txt')  # load map
    p = Problem(map)        # load problem
    if not astar(p):        # solve
        print 'No solution'
