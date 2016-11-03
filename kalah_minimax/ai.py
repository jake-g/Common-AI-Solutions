import copy
import multiprocessing
import time
from operator import itemgetter

# TODO comment code

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"


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


def process(arg, **kwarg):
    return ai.minimax(*arg, **kwarg)


class ai:
    def __init__(self):
        self.init = None

    def get_states(self, state, max_player=True):
        def get_moves():
            # return non empty pits for player
            if max_player:
                player = state.a
            else:
                player = state.b
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
                board[pos] += 1

            s.go_again = True if pos == 6 else False
            if 0 <= pos <= 5 and board[pos] == 1:
                board[6] += (board[12 - pos] + 1) # move stolen
                board[pos] = board[12 - pos] = 0 # empty

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


    def heuristic(self, score, loss, stolen):
        # TODO make way better one
        # TODO make heuristic class H.loss, H.score, H.calulate()
        # TODO check for defense? dont leave board in state that opponent can steal>
        return score + 0.5*stolen - (loss*0.1)**3


    def minimax(self, state, depth=None, max_player=False, alpha=-999, beta=999):
        if depth is None:
            depth = self.init.depth
        if depth == 0 or time.time() - self.init.time > self.init.cutoff:
            # TODO messy
            a_loss = sum(self.init.a) - sum(state.a)
            b_loss = sum(self.init.b) - sum(state.b)
            if max_player:
                score = state.af - self.init.af
                return self.heuristic(score, a_loss, b_loss)
            else:
                score = state.bf - self.init.bf
                return self.heuristic(score, b_loss, a_loss)
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


    def move(self, a, b, af, bf, max_time):
        init = State(a, b, af, bf)
        self.init = init  # store for later
        self.init.time = time.time()
        self.init.cutoff = .9  # max_time/1000 * 0.9
        self.init.depth = 7 # TODO use max_time input !

        #
        # f = open('debug.txt', 'a')  # Make sure to clean the file before each of your experiment
        # f.write('depth: %d\n' % self.init.depth)

        children = list(self.get_states(init))
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        scores = pool.map(process, zip([self] * len(children), children))
        score, best = sorted(zip(scores, children), key=itemgetter(0)).pop()  # get best score tuple(score, state)
        pool.terminate()

        status = 'elapsed time: %f s\n' % round(time.time() - self.init.time, 5)
        print self.init.depth,score,status

        # print 'Before %s\nAfter %s\n%s' % (init, best, status)
        # f.write(status)
        # f.close()
        return best.move


def process_simple(arg, **kwarg):
    return ai_simple.minimax(*arg, **kwarg)

class ai_simple:
    def __init__(self):
        self.init = None

    def get_states(self, state, max_player=True):
        def get_moves():
            # return non empty pits for player
            if max_player:
                player = state.a
            else:
                player = state.b
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
                board[pos] += 1

            s.go_again = True if pos == 6 else False
            if 0 <= pos <= 5 and board[pos] == 1:
                board[6] += (board[12 - pos] + 1) # move stolen
                board[pos] = board[12 - pos] = 0 # empty

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


    def heuristic(self, score, loss, stolen):
        return (score - (loss*0.3)**2) + stolen


    def minimax(self, state, depth=None, max_player=False, alpha=-999, beta=999):
        if depth is None:
            depth = self.init.depth
        if depth == 0 or time.time() - self.init.time > self.init.cutoff:
            # # TODO messy
            a_loss = sum(self.init.a) - sum(state.a)
            b_loss = sum(self.init.b) - sum(state.b)
            if max_player:
                score = state.af - self.init.af
                return self.heuristic(score, a_loss, b_loss)
            else:
                score = state.bf - self.init.bf
                return self.heuristic(score, b_loss, a_loss)
            # return score
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


    def move(self, a, b, af, bf, max_time):
        print 'Sup simple simon'
        init = State(a, b, af, bf)
        self.init = init  # store for later
        self.init.time = time.time()
        self.init.cutoff = .9  # max_time/1000 * 0.9
        self.init.depth = 7 # TODO use max_time input !

        # f = open('debug.txt', 'a')  # Make sure to clean the file before each of your experiment
        # f.write('depth: %d\n' % self.init.depth)

        children = list(self.get_states(init))
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        scores = pool.map(process_simple, zip([self] * len(children), children))
        score, best = sorted(zip(scores, children), key=itemgetter(0)).pop()  # get best score tuple(score, state)
        pool.terminate()

        status = 'elapsed time: %f s\n' % round(time.time() - self.init.time, 5)
        print self.init.depth,score,status

        # print 'Before %s\nAfter %s\n%s' % (init, best, status)
        # f.write(status)
        # f.close()
        return best.move
        # TODO DO WE HAVE TO RETURN RANDOM -- if so ultra failsafe return random if time is max time
        # TODO maybe store to file parameters to use for improvement. like if elapsed time < VAL: depth +=1

if __name__ == "__main__":
    # arbitrary board state
    a = [9, 8, 8, 0, 3, 1]
    b = [9, 3, 1, 3, 11, 11]
    af = 3
    bf = 3
    t = 1000
    test = ai()
    move = test.move(a[:], b[:], af, bf, t)
    print 'Exiting...'
