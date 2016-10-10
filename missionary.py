class Problem:
    def __init__(self, initial_state, actions, goal):
        # initializes state and actions
        self.state = initial_state  # object with print and vector
        self.actions = actions  # object with print and vector
        self.goal = goal  # same object
        self.visited = set()  # set of visited nodes

    def __str__(self):
        left = self.state
        right = (3 - left[0], 3 - left[1], 1 - left[2])
        visual = '%s%s' % (left[0] * 'M', left[1] * 'C')
        if left[2] == 0:
            visual += '|<B>\t\t|'
        elif left[2] == 1:
            visual += '|\t\t<B>|'
        visual += '%s%s\n' % (right[0] * 'M', right[1] * 'C')
        line = 18 * '-' + '\n'
        visited = 'Visited: ' + repr(self.visited)
        visual = '\n' + line + visual + line + visited
        return visual

    def valid_action(self, action):
        return action in self.actions

    def valid_state(self):
        return (0 <= self.state[0] <= 3 and
                0 <= self.state[1] <= 3 and
                0 <= self.state[2] <= 1)

    def is_dead(self):
        return not (self.state[0] == self.state[1] or
                    self.state[0] == 3 or
                    self.state[0] == 0)

    def already_visited(self):
        return self.state in self.visited

    def is_goal(self):
        return self.state == self.goal

    def visited(self):
        return self.visited

    def apply_action(self, a):
        if not self.valid_action(a):
            raise ValueError('Invalid Action'), a
        self.visited.add(self.state)
        new = list(self.state)
        for i, s in enumerate(self.state):
            if i == 2:  # flip side
                new[i] = int(not s)
                break
            else:
                j = 1  # right side case
                if self.state[2] == 0:  # left side boat
                    j = -1
                new[i] = self.state[i] + j * a[i]  # apply action
        self.state = tuple(new)

        if not self.valid_state():
            raise ValueError('Invalid State', new)

    def update(self, a):
        print 'Action : ', a
        print 'Before : ', self.state
        self.apply_action(a)
        print 'After  : ', self.state
        if self.is_dead():
            print 'DEAD'
            return None
        if self.already_visited():
            print 'ALREADY VISITED'
            return None
        elif self.is_goal():
            print 'GOAL'
            return True
        else:
            print 'CONTINUE'
            return False


# if __name__ == '__main__':
def display(state):
    left = state
    right = (3 - left[0], 3 - left[1], 1 - left[2])
    visual = '%s%s' % (left[0] * 'M', left[1] * 'C')
    if left[2] == 0:
        visual += '|<B>\t\t|'
    elif left[2] == 1:
        visual += '|\t\t<B>|'
    visual += '%s%s\n' % (right[0] * 'M', right[1] * 'C')
    line = 18 * '-' + '\n'
    visual = '\n' + line + visual + line
    return visual

def valid_action(action):
    return action in legal_actions

def valid_state(state):
    return (0 <= state[0] <= 3 and
            0 <= state[1] <= 3 and
            0 <= state[2] <= 1)

def is_dead(state):
    return not (state[0] == state[1] or
                state[0] == 3 or
                state[0] == 0)

def already_visited(state):  # todo remove def
    print 'DEBUG ALREADY VISITED'
    return state in visited

def is_goal(state):         # todo remove def
    print 'DEBUG GOAL!!!!!!'
    return state == goal_state

def apply_action(state, a):
    if not valid_action(a):
        raise ValueError('Invalid Action'), a
    new = list(state)
    for i, s in enumerate(state):
        if i == 2:  # flip side
            new[i] = int(not s)
            break
        else:
            j = 1  # right side case
            if state[2] == 0:  # left side boat
                j = -1
            new[i] = state[i] + j * a[i]  # apply action
    new = tuple(new)
    if not valid_state(new):
        raise ValueError('Invalid State', new)
    return new

# def update(state, a):
#     print 'Action : ', a
#     print 'Before : ', state
#     apply_action(state, a)
#     print 'After  : ', state
#     if self.is_dead():
#         print 'DEAD'
#         return None
#     if self.already_visited():
#         print 'ALREADY VISITED'
#         return None
#     elif self.is_goal():
#         print 'GOAL'
#         return True
#     else:
#         print 'CONTINUE'
#         return False

# def init():
#     # legal_actions = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 1)]
#     # init_state = (3, 3, 0)
#     # goal_state = (0, 0, 1)
#     return Problem(init_state, legal_actions, goal_state)


def recurse(state):
    for a in legal_actions:
        display(state)
        print 'Action : ', a
        print 'Before : ', state

        new = apply_action(state, a)
        print 'After  : ', new
        if is_goal(new):
            'GOAL'
            break
        if not is_dead(new) and not already_visited(new):
            'CONTINUE'
            visited.add(state)
            recurse(visited.pop)




legal_actions = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 1)]
init_state = (3, 3, 0)
goal_state = (0, 0, 1)
visited = [init_state]
recurse(init_state)

# missionary = init()  # object tracks game progress
# recurse(missionary)
# stack = [missionary.state]  # put initial state in LIFO

# win = [(0, 2), (0, 1), (0, 2), (0, 1), (2, 0), (1, 1), (2, 0), (0, 1), (0, 2), (0, 1), (0, 2)]
# for a in win:
#     missionary.update(a)
#     print missionary
