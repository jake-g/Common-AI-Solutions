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
            return 'move: %r\na: %r (%r)\nb: %r (%r)\n' \
                   % (self.last_move, self.a, self.af, self.b, self.bf)

    def random_move(self):
        r = []  # return a random move
        for i in range(6):  # Nonempty moves
            if self.state.a[i] != 0:
                r.append(i)
        return r[random.randint(0, len(r) - 1)]

    def get_states(self, max_player):
        def get_moves():
            if max_player:
                player = self.state.a
            else:
                player = self.state.b
            for i, n in enumerate(player):
                if n > 0: yield i  # ith hole not empty

        def new_state(move):
            # returns new state resulting in applied move
            assert move < 6
            assert self.state.a[move] > 0

            def apply_move(move, board):
                beads = board[move]
                board[move] = 0  # grab beads
                while beads >= 0:
                    move += 1
                    board[move % 13] += 1  # drop bead
                    beads -= 1
                return board

            new = copy.deepcopy(self.state)  # clone game state
            new.last_move = move

            if max_player:  # a is moving
                board = new.a + [new.af] + new.b
                board = apply_move(move, board)
                new.a = board[0:6]
                new.af = board[6]
                new.b = board[7::]
            else:    # b is moving
                board = new.b + [new.bf] + new.a
                board = apply_move(move, board)
                new.b = board[0:6]
                new.bf = board[6]
                new.a = board[7::]

            return new


        for move in get_moves():
            yield new_state(move )  # new state


    def move(self, a, b, af, bf, t):
        self.state = ai.state(a, b, af, bf)
        d = 3  # depth
        f = open('fuck.txt', 'a')  # Make sure to clean the file before each of your experiment
        f.write('Move: depth = ' + str(d) + '\n')
        t_start = time.time()
        print 'time', t

        next_state = self.minimax(d)

        print '-----'
        f.write(str(time.time() - t_start) + '\n')
        f.close()
        # print 'move %r' % move
        return next_state.last_move

    # calling function
    def minimax(self, depth, max_player=True, state=None):
        if depth == 0: # or out of moves
            print 'reached depth'
            return

        if max_player:
            best_val = -999
            for state in self.get_states(max_player):
                child = self.minimax(depth-1, not max_player, state)
                if child.af > best_val:
                    best_val = child.af
                    best_state = child

        else :
            best_val = 999
            for state in self.get_states(max_player):
                child = self.minimax(depth-1, not max_player, state)
                if child.af < best_val:
                    best_val = child.af
                    best_state = child
        return best_state
