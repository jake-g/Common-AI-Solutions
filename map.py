import pygame
import sys

BOUND = 40


class Map():
    def get_point(self, line):
        return tuple([self.scale*x for x in map(int, line.split())])

    def get_rectangle(self, line):
        arr = [self.scale*x for x in map(int, line.split())]
        rect = zip(arr[0::2], arr[1::2])
        return rect

    def __init__(self, f):
        self.rects = []
        self.scale = 600/BOUND
        n_rects = 0
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
                    self.rects.append(self.get_rectangle(line))


# Build static map
def draw_map(screen, map):
    screen.fill((255, 255, 255))     # erase the screen
    for rect in map.rects:
        pygame.draw.lines(screen, (0, 0, 0), True, rect, 2)
        for p in rect:
            pygame.draw.circle(screen, (0, 0, 255), p, 5)

    pygame.draw.circle(screen, (0, 255, 0), map.start, 10)
    pygame.draw.circle(screen, (255, 0, 0), map.goal, 10)
    pygame.display.update()

map = Map('data2.txt')

pygame.init()
pygame.display.set_caption('A* Pathfinding')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((map.scale * BOUND, map.scale * BOUND))
draw_map(screen, map)

while (True):

    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit();



    # draw the updated picture
    # pygame.draw.lines(screen, c.black, True, r3, 1)

    # update the state
    pygame.display.update()
    msElapsed = clock.tick(20)
