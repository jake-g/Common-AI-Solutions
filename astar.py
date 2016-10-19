import math
from heapq import *

# TODO COMMENT CODE
class Map:
    def get_point(self, line):
        return tuple([self.scale * x for x in map(int, line.split())])

    def get_rectangle(self, line):
        arr = [self.scale * x for x in map(int, line.split())]
        rect = zip(arr[0::2], arr[1::2])
        return rect

    def get_lines_from_rect(self, r):
        return [(r[0], r[1]),
                (r[0], r[3]),
                (r[0], r[2]),
                (r[2], r[1]),
                (r[2], r[3]),
                (r[1], r[3])]

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
                    print self.lines
                    self.nodes |= set(rect)
                    self.rects.append(rect)
        print self.lines


class Problem:
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
    return math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)


# Checks if line1 intersects line2
def intersect(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    def point_on_line(line, p):  # C is on AB if distance(A,C) + distance(B,C) = length(AB)
        if line[0] == p or line[1] == p:
            return False
        return distance(line[0], p) + distance(line[1], p) == distance(line[0], line[1])

    # TODO clean up cases
    if sorted((p1, p2)) == sorted((p3, p4)):  # same segment
        return False

    if p2 == p3 or p2 == p4:
        return False

    if point_on_line((p1, p2), p3) or point_on_line((p1, p2), p4) or point_on_line((p3, p4), p1) or point_on_line(
            (p3, p4), p2):
        return True

    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)


def illegal(start, end, lines):
    # print lines
    for l in lines:

        if intersect(start, end, l[0], l[1]):
            print 'True'
            return True
        else:
            print 'False'
    return False


def print_path(path, cost):
    print 'Best Path:'
    print 'Point\t\t\tCost'
    for n in path[::-1]:  # reverse iterate
        print n, ' \t\t', cost.get(n)


def astar(p):
    # Init
    p.cost[p.start] = 0;  # cost to start node
    p.score[p.start] = distance(p.start, p.goal)
    heappush(p.open, (p.score[p.start], p.start))

    # Search
    while p.open:
        curr = heappop(p.open)[1]
        print 'Current:', curr

        if curr == p.goal:
            path = []
            while curr in p.parent:
                path.append(curr)
                curr = p.parent[curr]
            path.append(p.start)
            print_path(path, p.cost)
            return path[::-1]  # reverse

        p.closed.add(curr)
        for node in p.nodes:
            if curr == node:
                continue

            if node in p.closed and node_cost >= p.cost.get(node, 0):
                print 'Already Saw better: ', curr, node
                continue

            if illegal(curr, node, p.lines):
                continue
            node_cost = p.cost[curr] + distance(curr, node)
            print 'LEGAL:', curr, node

            if node_cost < p.cost.get(node, 0) or node not in [i[1] for i in p.open]:
                p.parent[node] = curr
                p.cost[node] = node_cost
                p.score[node] = node_cost + distance(node, p.goal)
                print 'Cost to here:', node_cost
                dist = distance(node, p.goal)
                print 'Distance to goal:', dist
                print 'Score:', node_cost + dist
                heappush(p.open, (p.score[node], node))
            else:
                print 'Cost too high'

    return False


if __name__ == '__main__':
    map = Map('data1.txt')
    p = Problem(map)
    astar(p)
