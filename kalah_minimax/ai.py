import copy
import multiprocessing
import time
from operator import itemgetter


class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"


class State:
    # defines state object
    def __init__(self, a, b, af, bf):
        self.a = a
        self.b = b
        self.af = af
        self.bf = bf
        self.move = None

    def __str__(self):  # for print
        return 'move: %r\na: %r (%r)\nb: %r (%r)\n' \
               % (self.move, self.a, self.af, self.b, self.bf)


def process(arg, **kwarg):
    # used for multiprocessing search
    return ai.minimax(*arg, **kwarg)


class ai:
    def __init__(self):
        self.init = None

    def get_states(self, state, max_player=True):
        # gets possible states after move
        def get_moves():
            # return non empty pits for player
            player = state.a if max_player else state.b
            for i, n in enumerate(player):
                if n > 0: yield i  # ith hole not empty

        def new_state(pos):
            # returns new state resulting in applied move
            s = copy.deepcopy(state)  # clone game state
            board = s.a + [s.af] + s.b if max_player else s.b + [s.bf] + s.a
            s.move = pos
            # apply move to board
            beads = board[pos]
            board[pos] = 0  # grab beads
            while beads > 0:
                pos = (pos + 1) % 13
                beads -= 1  # drop bead
                board[pos] += 1  # next hole

            s.go_again = True if pos == 6 else False  # check if additional move
            if 0 <= pos <= 5 and board[pos] == 1:
                board[6] += (board[12 - pos] + 1)  # move stolen
                board[pos] = board[12 - pos] = 0  # empty

            # subdivide board
            if max_player:
                s.a = board[0:6]
                s.af = board[6]
                s.b = board[7::]
            else:
                s.b = board[0:6]
                s.bf = board[6]
                s.a = board[7::]

            return s

        for m in get_moves():
            yield new_state(m)  # new state

    def heuristic(self, score, loss, stolen, again):
        # evaluates board and returns a heuristic score
        return score + (again + stolen) ** 2 - loss

    def minimax(self, state, depth=None, max_player=False, alpha=-999, beta=999):
        # minimax with alpha-beta pruning and go again logic
        if depth is None:  # first time
            depth = self.init.depth

        if depth == 0 or time.time() - self.init.time > self.init.cutoff:
            # leaf node, evaluate heuristic
            a_loss = sum(self.init.a) - sum(state.a)
            b_loss = sum(self.init.b) - sum(state.b)
            if max_player:
                score = state.af - self.init.af
                return self.heuristic(score, a_loss, b_loss, state.go_again)
            else:
                score = state.bf - self.init.bf
                return self.heuristic(score, b_loss, a_loss, state.go_again)

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
                    max_player = not max_player  # dont swap max player
                val = self.minimax(child, depth - 1, not max_player)
                best_val = min(best_val, val)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            return best_val

    def move(self, a, b, af, bf, max_time):
        # return a move to the game using minimax
        # init state before move
        init = State(a, b, af, bf)
        self.init = init  # store for later
        self.init.time = time.time()
        self.init.cutoff = max_time / 1000 * 0.86  # tuned to return move in < 1 sec
        self.init.depth = 6
        children = list(self.get_states(init))  # available moves

        # Set up and execute multiprocessing
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        scores = pool.map(process, zip([self] * len(children), children))
        score, best = sorted(zip(scores, children), key=itemgetter(0)).pop()  # get best score tuple(score, state)
        pool.terminate()

        # Results
        status = 'elapsed time: %f s\n' % round(time.time() - self.init.time, 5)
        print self.init.depth, score, status
        return best.move


if __name__ == "__main__":
    # arbitrary board state
    a = [9, 8, 8, 1, 2, 1]  # hard
    b = [9, 3, 1, 3, 11, 11]
    af = 3
    bf = 3
    t = 1000
    test = ai()
    move = test.move(a[:], b[:], af, bf, t)
    print 'Exiting...'
