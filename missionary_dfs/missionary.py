# Missionary-Cannibal Problem
#   Jake Garrison
#   UW EE 562
#   HW 1


# Initial params
init_state = (3, 3, 'L')
goal_state = (0, 0, 'R')
visited = []  # tracks explored nodes
set = Set()
legal_actions = [(2, 0), (0, 2), (1, 1), (0, 1), (1, 0)]  # valid action set
count = {'dead': 0, 'revisit': 0, 'valid': 0, 'solution': 1}  # counter object


def is_safe(state):
    # Checks for dead state or visited state and tracks count, returns safe bool
    # Count includes starting and goal node
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
    # Applies input action to input state and moves boat to opposite side
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


def solution_info():
    # Prints info for solution
    return 'Solution %d\n Total Count: %r\n Repeat Count: %r\n Illegal Count: %r\n States: %r\n' \
           % (count['solution'], count['valid'], count['revisit'], count['dead'], visited)


def dfs(state):
    # DFS algorithm tries each action and that backtracks if not 'safe' state
    visited.append(state)  # FIFO Stack
    set.add((state[0], state[1]))
    if state == goal_state:
        print solution_info()
        count['solution'] += 1
    for a in legal_actions:
        new_state = apply_action(state, a)
        if new_state and is_safe(new_state):  # explore new state if safe
            dfs(new_state)
    visited.pop()  # next node


if __name__ == '__main__':
    dfs(init_state)
