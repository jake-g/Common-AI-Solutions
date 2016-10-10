class State:
    def __init__(self, initial_state, actions, goal):
        # initializes state and actions
        self.state = initial_state  # object with print and vector
        self.actions = actions  # object with print and vector
        self.goal = goal  # same object

    def __str__(self):
        left = self.state
        right = (3 - left[0], 3 - left[1], 1 - left[2])
        str = '%s%s' % (left[0] * 'M', left[1] * 'C')
        if left[2] == 0:
            str += '|<B>\t\t|'
        elif left[2] == 1:
            str += '|\t\t<B>|'
        str += '%s%s\n' % (right[0] * 'M', right[1] * 'C')
        str = '----------------\n' + str + '----------------\n'
        return str

    def valid_action(self, action):
        return action in self.actions

    def valid_state(self, state):
        return 0 <= state[0] <= 3 and \
               0 <= state[1] <= 3 and \
               0 <= state[2] <= 1

    def is_dead(self):
        safe = (self.state[0] == self.state[1] or \
                self.state[0] + self.state[1] == 3)
        return not safe

    def is_goal(self):
        return self.state == self.goal

    def apply_action(self, a):
        if not self.valid_action(a):
            raise ValueError('Invalid Action'), a

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
        new = tuple(new)
        if not self.valid_state(new):
            raise ValueError('Invalid State', new)
        self.state = new

    def update(self, a):
        print 'Action : ', a
        print 'Before : ', self.state
        self.apply_action(a)
        print 'After  : ', self.state
        if self.is_dead():
            print 'DEAD'
            return None
        elif self.is_goal():
            print 'GOAL'
            return True
        else:
            print 'CONTINUE'
            return False


# if __name__ == '__main__':
'''
state = State(initial vars)
state.print

loop
choose action (try all combos in same order? (use list of actions)
update state(action)
state.print
state.message
act basd off message (recures if continue, backtrack if not valid or dead, stop if goal)
'''

actions = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 1)]
init_state = (3, 3, 0)
goal_state = (0, 0, 1)
state = State(init_state, actions, goal_state)

print state
state.update((1, 1))
print state
state.update((1, 0))
print state
state.update((2, 0))
print state
