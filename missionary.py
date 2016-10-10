# if __name__ == '__main__':
# TODO bundle defs into class with self.state,debug,init,count
# TODO add comments


def display(left):
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


# TODO dont need to check all three return false on first unsafe...
def is_safe(state, debug=False):
    valid = (0 <= state[0] <= 3 and
             0 <= state[1] <= 3 and
             0 <= state[2] <= 1)
    seen = (state in visited)
    dead = not (state[0] == state[1] or
                state[0] == 3 or
                state[0] == 0)
    safe = (valid and not dead and not seen)
    if debug and not safe:
        print 'Bad State: %s\n Invalid: %s\n Seen: %s\n Dead: %s' \
              % (state, not valid, seen, dead)
    return safe


def apply_action(state, a):
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


def info(state, new_state, a):
    return display(state) + \
           'Visited: %r\nBefore : %r \nAction : %r \nAfter  : %r' \
           % (visited, state, a, new_state)


# TODO dont need global
def dfs(state):
    visited.append(state)  # FIFO Stack
    global count
    for a in legal_actions:
        new_state = apply_action(state, a)
        count += 1
        if new_state == goal_state:
            print info(state, new_state, a)
            print 'Goal reached after %d tries' % count
            exit()
        if is_safe(new_state, True):
            print info(state, new_state, a)
            dfs(new_state)
    visited.pop()


legal_actions = [(0, 1), (1, 0), (1, 1), (0, 2), (2, 0)]
init_state = (3, 3, 0)
goal_state = (0, 0, 1)
visited = []
count = 0
dfs(init_state)
