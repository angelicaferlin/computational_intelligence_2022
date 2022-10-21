import random
import logging

def problem(N, seed=None):
    """Creates a list of lists that contains a random amount of numbers between 0 and N-1."""
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

def goal_test(current_state, goal_state):
    """Checks if the current state is the same as the goal state."""
    return all(elem in current_state for elem in goal_state)

def count_unique_elem(current_state, l):
    """Returns the number of unique elements between the lists."""
    return len(set(l).difference(set(current_state)))

def count_unique_elem_opt(current_state, l):
    """Returns the number of unique elements between the lists also regarding duplicates of numbers."""
    return (len(set(l).difference(set(current_state)))*(len(set(l)) == len(l)))

def search(N, seed=None):
    """Searches for the least amount of lists that together contains the numbers from 0 to N-1."""
    state_space = problem(N, seed)
    GOAL_STATE = set(range(N))
    current_state = list()
    visited_nodes = 0
    weight = 0
    state_space = sorted(state_space, key=lambda l: count_unique_elem(current_state, l))

    while state_space and not goal_test(current_state, GOAL_STATE):
        element = state_space.pop()
        visited_nodes += 1
        weight += len(element)

        for num in element:
            current_state.append(num)
        
        state_space = sorted(state_space, key=lambda l: count_unique_elem_opt(current_state, l))

    if (goal_test(current_state, GOAL_STATE)):
        logging.info(f' Solution found for N={N}: w={weight}: visited nodes={visited_nodes}: (bloat={(weight-N)/N*100:.0f}%)') 
    else:
        logging.info(f' No solution found')

logging.getLogger().setLevel(logging.INFO)  

seed = 42
for N in [5, 10, 20, 100, 500, 1000]:           
    search(N, seed)