import time
import random
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
            self.parent = None

        def __str__(self):
            return 'a: %r (%r)\nb: %r (%r)\n' \
                   % (self.a, self.af, self.b, self.bf)

    def random_move(self):
        r = []  # return a random move
        for i in range(6):  # Nonempty moves
            if self.state.a[i] != 0:
                r.append(i)
        return r[random.randint(0, len(r) - 1)]

    def get_states(self):
        def get_moves(player):
            for i, n in enumerate(player):
                if n > 0:
                    yield i  # ith hole not empty

        def apply_move(move, player=1):
            new = self.state
            if player:  # 1 = player a
                beads = self.state.a[move]
                # FINISH THIS!!!!!!!!!
                if beads > move:
                    for i in beads % 14
                    new.a = [n+1 for n in self.state.a]
                    new.af += 1

                    print 'score!'

            return new




        for move in get_moves(self.state.a):
            new_state = apply_move(move)
            yield new_state

    def move(self, a, b, af, bf, t):
        self.state = ai.state(a, b, af, bf)
        d = 3  # depth
        f = open('fuck.txt', 'a')  # Make sure to clean the file before each of your experiment
        f.write('Move: depth = ' + str(d) + '\n')
        t_start = time.time()
        print 'time', t

        move = self.minimax(d)

        f.write(str(time.time() - t_start) + '\n')
        f.close()
        print 'move %r' % move
        return move

    # calling function
    def minimax(self, depth):
        print self.state
        for state in self.get_states():
            print state
        print '-----'
        time.sleep(0.1 * depth)
        return self.random_move()
