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
    valid = (0 <= state[0] <= 3 and
            0 <= state[1] <= 3 and
            0 <= state[2] <= 1)
    if not valid:
        print 'DEBUG NOT VALID STATE'
    return valid


def is_dead(state):
    dead = not (state[0] == state[1] or
                state[0] == 3 or
                state[0] == 0)
    if dead:
        print 'DEBUG DEAD'
    return dead


def already_visited(state):
    seen = (state in visited)
    if seen:
        print 'DEBUG ALREADY VISITED'
    return seen


def is_goal(state):
    goal = (state == goal_state)
    if goal:
        print 'DEBUG GOAL!!!!!!'
    return goal


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
    return tuple(new)


def recurse(state):
    visited.append(state)
    print visited
    print display(state)
    for a in legal_actions:
        print 'Before : ', state
        print 'Action : ', a
        new = apply_action(state, a)
        print 'After  : ', new
        if is_goal(new):
            'GOAL'
            exit()
        if valid_state(new) and not is_dead(new) and not already_visited(new):
            print 'CONTINUE'
            recurse(new)

    print 'VISIT PARENT\n\n'
    visited.pop()


legal_actions = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]
init_state = (3, 3, 0)
goal_state = (0, 0, 1)
visited = []
recurse(init_state)
