import time
import random
import copy

import io




class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"


class ai:
    def __init__(self):
        pass

    class state:
        def __init__(self, a, b, af, bf, parent=None):
            self.a = a
            self.b = b
            self.af = af
            self.bf = bf
            self.last_move = None

        def __str__(self):
            return 'last move: %r\na: %r (%r)\nb: %r (%r)\n' \
                   % (self.last_move, self.a, self.af, self.b, self.bf)

    def random_move(self):
        r = []  # return a random move
        for i in range(6):  # Nonempty moves
            if self.state.a[i] != 0:
                r.append(i)
        return r[random.randint(0, len(r) - 1)]

    def get_states(self):
        def get_moves(player):
            for i, n in enumerate(player):
                if n > 0: yield i  # ith hole not empty

        def new_state(move):
            # returns new state resulting in applied move

            assert move < 6
            assert self.state.a[move] > 0

            new = copy.deepcopy(self.state)  # clone game state
            new.last_move = move
            board = new.a + [new.af] + new.b
            beads = board[move]
            board[move] = 0 # grab beads
            while beads >= 0:
                move += 1
                board[move % 13] += 1  # drop bead
                beads -= 1

            new.a = board[0:6]
            new.af = board[6]
            new.b = board[7::]
            return new

        for move in get_moves(self.state.a):
            yield new_state(move)  # new state

    def move(self, a, b, af, bf, t):
        self.state = ai.state(a, b, af, bf)
        d = 3  # depth
        f = open('fuck.txt', 'a')  # Make sure to clean the file before each of your experiment
        f.write('Move: depth = ' + str(d) + '\n')
        t_start = time.time()
        print 'time', t

        move = self.minimax(d)

        print '-----'
        f.write(str(time.time() - t_start) + '\n')
        f.close()
        # print 'move %r' % move
        return move

    # calling function
    def minimax(self, depth):
        for state in self.get_states():
            print state
        time.sleep(0.1 * depth)
        return self.random_move()
