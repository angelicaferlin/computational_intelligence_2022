from utils import *

def hard_coded_agent(state: Nim):
    """Agent using fixed rules"""
    data = cook_status(state=state)

    active_rows_number = data["active_rows_number"]
    active_rows_index = data["active_rows_index"]
    rows_with_multiple_elem = data["rows_multiple_elem"]
    longest_row = data["longest_row"]

    if active_rows_number == 1:
        row = active_rows_index[0]
        elem = state.rows[row]
        
    elif active_rows_number % 2 == 0:
        if len(rows_with_multiple_elem) == 1: 
            row = rows_with_multiple_elem[0][0]
            elem = rows_with_multiple_elem[0][1] - 1 # take all elem exept one
            logging.debug(f"Even rows one mul, elem: {elem}") 
        else:
            row = longest_row
            logging.debug(f"longest row index: {longest_row}, elem: {state.rows[longest_row]}")
            elem = max(state.rows[longest_row] - 1, 1) # take all elem exept one
            logging.debug(f"Even rows, several mul, elem: {elem}") 
    else:
        if len(rows_with_multiple_elem) == 1:
            row = rows_with_multiple_elem[0][0]
            elem = rows_with_multiple_elem[0][1] # take all elem
            logging.debug(f"Odd rows, one mul, elem: {elem}") 
        else:
            row = longest_row
            elem = state.rows[longest_row]
            logging.debug(f"Even rows, several mul, elem: {elem}") 

    ply = Nimply(row, elem)
    return ply

def nim_sum_strategy(state: Nim):
  """"Using the optimal strategy with nim-sum to calculate the best possible next move"""
  X = state.rows[0]
  
  # X is the nim_sum(bitwise xor) of all heap sizes
  for i in range(1, len(state.rows)):
    X = X ^ state.rows[i]

  nim_sum_val = []
  # calculate the nim_sum between X and each heap size
  for i in state.rows:
    val = i ^ X
    nim_sum_val.append(val)

  row = "false"
 
  for i in range(len(nim_sum_val)):
    if nim_sum_val[i] < state.rows[i]: 
      row = i
      break
  
  # reduce that heap to value nim_sum
  if (row != "false"):
    num_objects = state.rows[row] - nim_sum_val[row]
    move = Nimply(row, num_objects)
  
  else:
    rand_row = random.randrange(0,len(state.rows))

    while(state.rows[rand_row] == 0):
      rand_row = random.randrange(0,len(state.rows))

    if(state.rows[rand_row] != 1):
      rand_obj = random.randrange(1, state.rows[rand_row])
                                  
    else: rand_obj = 1
    move = Nimply(rand_row, rand_obj)
  
  return move


def optimal_startegy(state: Nim) -> Nimply:
    """A strategy using nim sum to return the optimal move"""
    data = cook_status(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]


def random_agent(state: Nim):
    """A strategy returning a random possible move"""
    data = cook_status(state)
    return data["pure_random"]

def random_smart_agent(state: Nim):
    """A strategy returning a random possible move"""
    data = cook_status(state)
    if (data["active_rows_number"] == 1):
        row = data["active_rows_index"][0]
        elem = state.rows[row]
        ply = Nimply(row, elem)
    else:
        ply = data["pure_random"]
    return ply
    
def dumb(state: Nim):
    """A dumb strategy that always picks one element from the longest row"""
    data = cook_status(state=state)
    row = data["longest_row"]
    
    return Nimply(row, 1)
