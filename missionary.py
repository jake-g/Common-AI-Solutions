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


def is_goal(state):  # todo remove def
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
