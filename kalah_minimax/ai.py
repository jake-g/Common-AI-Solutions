import copy
import random
import time
import multiprocessing



class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"


class ai:
    def __init__(self):
        self.parent =  None

    class State:
        def __init__(self, a, b, af, bf):
            self.a = a
            self.b = b
            self.af = af
            self.bf = bf
            self.move = None

        def __str__(self):
            return 'move: %r\na: %r (%r)\nb: %r (%r)\n' \
                   % (self.move, self.a, self.af, self.b, self.bf)


    def random_move(self, state):
        r = []  # return a random move
        for i in range(6):  # Nonempty moves
            if state.a[i] != 0:
                r.append(i)
        return r[random.randint(0, len(r) - 1)]

    def get_states(self, state, max_player=True):
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
            new.move = move

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
        # return sum(state.a) - sum(self.parent.a) + (state.af - self.parent.af)**2
        return state.af - state.bf


    def minimax(self, state, depth, max_player=False, alpha=-999, beta=999):
        # TODO alpha beta prune
        if depth == 0:  # or node is a terminal node
            ai.leafs_reached += 1 # TODO DEBUG only
            return self.heuristic(state) # return the heuristic value of node
        if max_player:
            best_val = -999
            for child in self.get_states(state, max_player):
                if child.go_again:
                    max_player = not max_player
                val = self.minimax(child, depth - 1, not max_player, alpha, beta)
                best_val = max(best_val, val)
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            return best_val
        else:  # min player
            best_val = 999
            for child in self.get_states(state, max_player):
                if child.go_again:
                    max_player = not max_player
                val = self.minimax(child, depth - 1, not max_player)
                best_val = min(best_val, val)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            return best_val

    def move(self, a, b, af, bf, t):
        depth = 4
        parent = self.State(a, b, af, bf)
        self.parent = parent # store for later

        start_time = time.time() # debug
        ai.leafs_reached = 0 # debug
        f = open('debug.txt', 'a')  # Make sure to clean the file before each of your experiment
        f.write('depth: %d\n' % depth)


        best_score = -999
        children = list(self.get_states(parent))
        for child in children:
            score = self.minimax(child, depth)
            if score > best_score:
                best_score = score
                best = child
        print parent
        print best
        elapsed = round(time.time() - start_time, 5)
        status = 'leaves visited %d\nelapsed time %f ms\n%f ms per leaf\n' \
              % (ai.leafs_reached, elapsed, ai.leafs_reached/elapsed)
        print status
        f.write(status)
        f.close()

        return best.move