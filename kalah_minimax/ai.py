import copy
import random


class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"


class ai:
    def __init__(self):
        pass

    class state:
        def __init__(self, a, b, af, bf):
            self.a = a
            self.b = b
            self.af = af
            self.bf = bf
            self.last_move = 999

        def __str__(self):
            return 'move: %r\na: %r (%r)\nb: %r (%r)\n' \
                   % (self.last_move, self.a, self.af, self.b, self.bf)

    def move(self, a, b, af, bf, t):
        depth = 1
        # f = open('time.txt', 'a')  # Make sure to clean the file before each of your experiment
        # f.write('Move: depth = ' + str(depth) + '\n')
        # t_start = time.time()
        # print 'time', t

        state = ai.state(a, b, af, bf)
        self.state = state # store for later
        move, score = self.minimax(state, depth)

        print '-----'
        # f.write(str(time.time() - t_start) + '\n')
        # f.close()
        # print 'move %r' % move
        return move

    def random_move(self, state):
        r = []  # return a random move
        for i in range(6):  # Nonempty moves
            if state.a[i] != 0:
                r.append(i)
        return r[random.randint(0, len(r) - 1)]

    def get_states(self, state, max_player):
        def get_moves():
            # return non empty pits for player
            if max_player:
                player = state.a
            else:
                player = state.b
            for i, n in enumerate(player):
                if n > 0: yield i  # ith hole not empty

        def new_state(move):
            # returns new state resulting in applied move

            def apply_move(move, board):
                # apply move to board
                beads = board[move]
                board[move] = 0  # grab beads

                assert beads > 0
                assert move < 6
                while beads >= 0:
                    move += 1
                    board[move % 13] += 1  # drop bead
                    beads -= 1

                if move == 6:  # ended in player's pit +1 turn
                    return (board, True)  # player moves again
                else:
                    return (board, False) # turn over

            new = copy.deepcopy(state)  # clone game state
            new.last_move = move

            if max_player:  # a is moving
                board = new.a + [new.af] + new.b
                board, go_again = apply_move(move, board)
                new.go_again = go_again
                new.a = board[0:6]
                new.af = board[6]
                new.b = board[7::]
            else:  # b is moving
                board = new.b + [new.bf] + new.a
                board, go_again = apply_move(move, board)
                new.go_again = go_again
                new.b = board[0:6]
                new.bf = board[6]
                new.a = board[7::]

            return new

        for move in get_moves():
            yield new_state(move)  # new state

    def heuristic(self, state):
        # return sum(state.a) - sum(self.state.a) + (state.af - self.state.af)**2
        return state.af - state.bf

    def minimax(self, state, depth, max_player=True):
        # TODO alpha beta prune
        if depth == 0:  # or node is a terminal node
            # print 'reached leaf'
            # print state
            print 'move', state.last_move
            print 'score', self.heuristic(state)
            return state.last_move, self.heuristic(state) # return the heuristic value of node

        if max_player:
            best_val = -999
            for child in self.get_states(state, max_player):
                if child.go_again:
                    max_player = not max_player

                move, val = self.minimax(child, depth - 1, not max_player)
                # best_val = max(best_val, val)
                if val > best_val:
                    best_move = move
                    best_val = val
            return (best_move, best_val)
        else:  # min player
            best_val = 999
            for child in self.get_states(state, max_player):
                if child.go_again:
                    max_player = not max_player

                move, val = self.minimax(child, depth - 1, not max_player)
                # best_val = min(best_val, val)
                if val < best_val:
                    best_move = move
                    best_val = val
            return (best_move, best_val)
