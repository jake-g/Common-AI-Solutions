# A* Pathfinding Problem
#   Jake Garrison
#   UW EE 562
#   HW 2

import pygame
import sys
from astar import *


'''
Visualizes the path and map
need to have pygame. run `pip install pygame` to use visualizer, otherwise just run `astar.py
'''

BOUND = 40
FPS = 2


# check for quit events
def quit_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit();


# Build static map
def draw_map(screen, map):
    screen.fill((255, 255, 255))  # erase the screen
    for rect in map.rects:
        pygame.draw.lines(screen, (0, 0, 0), True, rect, 2)  # draw rectangles
        for p in rect:
            pygame.draw.circle(screen, (0, 0, 255), p, 3)  # draw corners
    pygame.draw.circle(screen, (0, 255, 0), map.goal, 5)  # draw goal
    pygame.display.update()


# Dynamic map
def update_map(screen, map, path, clock):
    last_node = path[0]
    # draw path
    for node in path:
        pygame.draw.lines(screen, (255, 0, 0), True, [last_node, node], 2)
        pygame.draw.circle(screen, (255, 0, 0), last_node, 5)
        pygame.draw.circle(screen, (255, 255, 0), node, 5)
        last_node = node
        pygame.display.update()
        msElapsed = clock.tick(FPS)

    pygame.draw.circle(screen, (0, 255, 0), map.goal, 5)
    pygame.display.update()


def visualize(f):
    scale = 600 / BOUND
    map = Map(f, scale)
    p = Problem(map)
    pygame.init()
    pygame.display.set_caption('A* Pathfinding')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((map.scale * BOUND, map.scale * BOUND))
    draw_map(screen, map)
    path = astar(p)
    if path:
        update_map(screen, map, path, clock)
        print 'Note: lines and costs are scaled by %r to fill the window' % scale
    else:
        print 'No solution...'

    while 1:  # stay open after solve
        quit_handler()
        msElapsed = clock.tick(FPS)

if __name__ == '__main__':
    visualize('data_personal.txt')
