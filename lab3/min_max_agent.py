from utils import *

def all_possible_new_states(init_state: list) -> list:
    """Define all possible new states and return them as a list"""
    possible_new_states = []

    for row in range(len(init_state)): # for every row
        for i in range(init_state[row]): # for the number of elem in row
            new_state = deepcopy(init_state)

            new_state[row] = new_state[row] - i - 1 #take away i+1 number of elem
            #print("new state: ", new_state)
            possible_new_states.append(new_state)
            #print(possible_new_states)
    #logging.debug(f"All possible new states: {possible_new_states}")
    return possible_new_states

def evaluate(state_as_list: list, player: int) -> int:
    """Evaluate if the game is over. Returns: 
    -1 if player 0 (maximizing) won
    1 if player 1 (minimizing) won
    None if the game is not over yet"""
    if sum(state_as_list) == 0: # if game is over
        return -1 if player == 0 else 1
    else:
        return None


def minimax(state_as_list: list, player: int) -> int:
    """Calculates all possible moves using the minmax method from a given state and then returns the score. It returns the best score considering the player.
    for player 0, best score is 1
    for player 1, best score is -1"""
    score = evaluate(state_as_list, player)

    if score != None:
        # if game is over
        return score

    if (player == 0): # if it is the maximizings turn
        scores = [minimax(new_state, player=1) for new_state in all_possible_new_states(state_as_list)]
        return max(scores)
    
    else: # if it is the minimizings turn
        scores = [minimax(new_state, player=0) for new_state in all_possible_new_states(state_as_list)]
        return min(scores)


def best_move(state_as_list: list, player: int) -> tuple:
    """Returns a tuple (winner, new_state)"""
    if player == 0: # if it is the maximizings turn
        new_player = 1 
        
        # calculate the moves for the minimizer and then pic the best one
        return max(
            (minimax(new_state, new_player), new_state) 
            for new_state in all_possible_new_states(state_as_list)
        )

    else: # it is the minimizings turn
        new_player = 0

        #calculate the moves for the maximizer and then try to minimize them
        return min( 
            (minimax(new_state, new_player), new_state)
        for new_state in all_possible_new_states(state_as_list))
    

def minimax_pruning(state_as_list: list, is_maximizing: bool, alpha=-1, beta=1) -> int:
    """Not working as intended.
    The idea is that this function only explores the nessecary nodes using alpha-beta pruning"""
    if (score := evaluate(state_as_list, is_maximizing)) is not None: 
        # if the game is over
        return score

    scores = []
    for new_state in all_possible_new_states(state_as_list):
        scores.append(
            score := minimax_pruning(new_state, not is_maximizing, alpha, beta)
        )
        
        if is_maximizing:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)

        if beta <= alpha:
            break
        
    return (max if is_maximizing else min)(scores)


def best_move_pruning(state_as_list: list, player: int) -> tuple:
    """Not working as intended.
    Should provide the best move using minimax_pruning
    """
    if player == 0: # maximizing
        return max(
            (minimax_pruning(new_state, is_maximizing=False), new_state)
            for new_state in all_possible_new_states(state_as_list)
        )
    else:
        return min(
            (minimax_pruning(new_state, is_maximizing=True), new_state)
            for new_state in all_possible_new_states(state_as_list)
        )


def nimply_move(current_state: Nim, new_state: list) -> Nimply:
    """Creates the Nimply by checkig the difference between the current state and the new state we get after the desired move"""
    diff = 0
    row = len(current_state.rows) #invalid row
    
    for i in range(len(current_state.rows)):
        
        if current_state.rows[i] != new_state[i]:
            diff = current_state.rows[i] - new_state[i]
            row = i
            
    ply = Nimply(row, diff)

    return ply


def min_max_agent(state: Nim):
    """Returns the best move from a state usin min-max"""
    state_as_list = [] # convert the state to list to easier handle the recursion later on

    for i in range(len(state.rows)):
        state_as_list.append(state.rows[i])

    logging.debug(f"State as a list: {state_as_list}")

    #best_m = best_move_pruning(state_as_list, player=0) 
    best_m = best_move(state_as_list=state_as_list, player=0)

    move = best_m[1] # since best_move = (score, [new state])
    logging.debug(f"MOVE: {move}")
    # from best move -> turn it into a nimply
    final_move = nimply_move(state, move)

    return final_move
