# Missionary-Cannibal Problem
#   Jake Garrison
#   UW EE 562
#   HW 1

# Initial params
legal_actions = [(0, 1), (1, 0), (1, 1), (0, 2), (2, 0)]
init_state = (3, 3, 'L')
goal_state = (0, 0, 'R')
count = {'dead': 0, 'revisit': 0, 'valid': 0}
visited = []


def is_safe(state):
    # Checks for dead state or visited state and tracks count
    count['valid'] += 1
    if not (state[0] == state[1] or state[0] == 3 or state[0] == 0):
        count['dead'] += 1
        return False
    elif state in visited:
        count['revisit'] += 1
        return False
    else:  # safe to change state
        count['valid'] += 1
        return True


def apply_action(state, a):
    # Applies action to state and moves boat to opposite side
    # return new state if valid state, otherwise return None
    new = list(state)
    for i, s in enumerate(state):
        if i == 2:  # flip side
            new[i] = 'R' if new[i] == 'L' else 'L'
            break
        else:
            j = 1  # right side case
            if state[2] == 'L':  # left side boat, subtract people
                j = -1
            new[i] = state[i] + j * a[i]  # apply action

    if 0 <= new[0] <= 3 and 0 <= new[1] <= 3:  # check number of M and C
        return tuple(new)  # Only return valid state EX: invalid (4, 1, 0)


def display(left):
    # Print diagram of current state
    right = (3 - left[0], 3 - left[1])
    visual = '%s%s' % (left[0] * 'M', left[1] * 'C')
    visual += '|<B>\t\t|' if left[2] == 'L' else '|\t\t<B>|'
    visual += '%s%s\n' % (right[0] * 'M', right[1] * 'C')
    line = 18 * '-' + '\n'
    visual = '\n' + line + visual + line
    return visual


def info(state, new_state, a):
    # Prints info for each state change
    return display(state) + \
           'Before : %r \nAction : %r \nAfter  : %r\nVisited: %r\nCount: %r' \
           % (state, a, new_state, visited, count)


def dfs(state):
    # DFS algorithm tries each action and that backtrackes if not 'safe' state
    visited.append(state)  # FIFO Stack
    for a in legal_actions:
        new_state = apply_action(state, a)
        if new_state:  # explore new state
            if new_state == goal_state:
                print info(state, new_state, a)
                print '\nGoal reached'
                exit()
            if is_safe(new_state):
                print info(state, new_state, a)
                dfs(new_state)

    visited.pop()  # next node


if __name__ == '__main__':
    dfs(init_state)
