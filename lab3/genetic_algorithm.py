from other_agents import *

# variables
OPPONENT = [nim_sum_strategy, random_agent, dumb]
OFFSPRING_SIZE = 200
K= 5
POPULATION_SIZE = 50
TOURNAMENT_SIZE = 5
nim_size = 5
GENERATIONS = 2

#%% Rules

def rule_one_multiple_left(state: Nim, data:dict, genome: dict, rule: str):
  """If only one of the active rows has multiple elem left. Depending on the rule it returns a move that take from one of the rows with single elem or multiple elem"""
  
  single_elem_rows = data["rows_with_one_element"]
  multiple_elem_rows = data["rows_multiple_elem"]

  if genome[rule][0] == 0: # take from a row with one elem
    elem = 1 # want to take the last elem in row
    single_elem_row = single_elem_rows[0][0] # looks like [(row,elem),(row,elem)] if two rows with single elem
    ply = Nimply(single_elem_row, 1)

  else: #take from the row with more than one element
    # choose row
    if len(multiple_elem_rows) == 0: # if no row with multiple elem 
      row = single_elem_rows[0][0]
      elem = 1
    else: 
      row = multiple_elem_rows[0][0] # [(row,elem)] -> since only one row with multiple elem

    # get elem to be removed
    if (genome[rule][1] > state.rows[row]): # if it wants to leave more elem than exists in row
      elem = 1                    
    else: 
      elem = max(state.rows[row] - genome[rule][1], 1)
    
    ply = Nimply(row, elem)
      
  return ply


def rule_several_multiple_left(state: Nim, data: dict, genome: dict, rule: str):
  """If several active rows has multiple elements left, take elements from either the longest or the shortest row depending on rule"""
  if (genome[rule][0] == 0): # choose from row with fewest elemt
    row = data['shortest_row']
  else:
    row = data['longest_row']
  
  elem = max(state.rows[row] - genome[rule][1], 1) # if it wants to leave more elem than exists in row
  ply = Nimply(row, elem)

  return ply

def even_rows_left(state: Nim, data: dict, genome: dict ) -> Nimply:
  """There are an even number of active rows left, returns move using rule 2 if only one row has multiple elem else rule 3"""
  rows_multiple_elem = data["rows_multiple_elem"]

  # rule 2
  if len(rows_multiple_elem) == 1: # only one row with multiple elems
    ply = rule_one_multiple_left(state=state, data=data, genome=genome, rule='Rule2')
  
  # rule 3  
  else: # several rows with multiple elem         
    ply = rule_several_multiple_left(state, data, genome, rule='Rule3')

  return ply

def one_row_left(state: Nim, data: dict, genome: dict) -> Nimply:
    """There is only one row left, return a move using rule 1"""
    active_row = data["active_rows_index"][0]

    elem_last_row = state.rows[active_row] #active_rows_index returns a list -> need to get the first one
   
    if elem_last_row < genome['Rule1']: #if the rule want to leave more elems than exists in row
        elem = 1
        ply = Nimply(active_row, elem)
        
    else:
        # possible improvement: add if you want to take more than K elem - take K
        elem_to_remove = max(elem_last_row - genome["Rule1"], 1) #if take more elem than exists -> take all
        ply = Nimply(active_row, elem_to_remove)

    return ply
  
def odd_number_of_rows_left(state: Nim, data: dict, genome: dict):
    """There are an odd number of active rows left, returns move using rule 4 if only one row has multiple elem else rule 5"""
    rows_multiple_elem = data["rows_multiple_elem"]

    # Rule 4
    if len(rows_multiple_elem) == 1: #only one row with multiple elems
        ply = rule_one_multiple_left(state=state, data=data, genome=genome, rule='Rule4')
    
    # Rule 5
    else: # several rows with multiple elem        
        ply = rule_several_multiple_left(state=state, data=data, genome=genome, rule='Rule5')

    return ply

def make_strategy(genome: dict) -> Callable:
    """Creates a function that is using the strategy specified by the rules"""
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        active_rows_number = data["active_rows_number"]

        # rule 1
        if active_rows_number == 1: #only one active row left
            ply = one_row_left(state=state,data=data, genome=genome) 
        
        # rule 2 or 3
        elif active_rows_number %2 == 0: # even numbers of active rows
            ply = even_rows_left(state=state, data=data, genome=genome)

        #rule 4 or 5
        else: # odd numbers of active rows
            ply = odd_number_of_rows_left(state=state, data=data, genome=genome)

        return ply

    return evolvable

#compute the fittness
def head2head(pl: dict, opponent: Callable, nim_size: int) -> int:
    """Runs a game of nim between one individual from the population and the opponent"""
    nim = Nim(nim_size)

    players = (make_strategy(pl), opponent)
    player = 0
    
    logging.debug(f"status: Initial board  -> {nim}")
    while nim:
        ply = players[player](nim)
        nim.nimming(ply)
        #logging.debug(f"status: After player {player} -> {nim}")
        player = 1 - player
    winner = 1 - player
    
    if winner == 0: # if the player (pl) wins, return 1 to calculate fitness
        logging.debug('Player won over opponent')
        return 1
    else:
        return 0

# calculate fitness for whole population
def calculate_fitness(population: list, nim_size):
    """Calculates fitness for each individual by playing 10 games against each each agent in OPPONENT"""
    NUM_MATCHES = 10
    
    for p1 in population:
        logging.debug(f"player {p1}")
        fitness = []

        for strat in OPPONENT:
            logging.debug(f"STRAT: {strat}")
            wins = 0
            for _ in range(NUM_MATCHES):
                wins += head2head(pl=p1, opponent=strat, nim_size=nim_size)
            fitness.append(wins/NUM_MATCHES)
        
        p1['fitness'] = (fitness[0], fitness[1], fitness[2])


def init_population(nim_size: int) -> list:
    """Initialize population by createing the parameters for the rules using random"""
    population = []

    max_leave = (nim_size-1)*2 # last row of the table will have nim_size*2-1 objects

    cond = POPULATION_SIZE
    
    while cond:
        individual = {'Rule1': random.randint(0,max_leave), 'Rule2': [random.randint(0,1), max_leave], 'Rule3': [random.randint(0, 1), random.randint(0, max_leave)],
        'Rule4': [random.randint(0,1), max_leave], 'Rule5': [random.randint(0,1), max_leave]}
        individual['fitness'] = ()
        population.append(individual)
        cond -= 1
        
    return population

# select k random individuals, return the one with best fitness
def tournament(population: list, nim_size: int) -> dict: 
    """Selects TOURNAMENT_SIZE amount of individuals and returns the best one by competing the fitness agains each other"""   
    contestors = random.sample(population, TOURNAMENT_SIZE)
    best_contestor = sorted(contestors, key=lambda indv: indv['fitness'], reverse=True)[0]
  
    return best_contestor
    
# take two parents and create one child
def crossover(parent1: dict, parent2: dict, mutation_prob: float) -> dict:
    """Takes two parents and creates a child where the child for each rule takes the whole rule from either parent1 or parent2 depending on a random selection"""
    
    rules_parent1 = [key for key in parent1.keys() if 'Rule' in key] # list of rules without the fitness
    
    child = {}

    for rule in rules_parent1:
        which_parent = random.randint(0,1)
        if which_parent == 0: # take rule from parent1
            child[rule] = parent1[rule]
        else:
            child[rule] = parent2[rule]
    
    child['fitness'] = ()
    rules = [key for key in child.keys() if 'Rule' in key]

    #mutation
    if random.random() < mutation_prob: # mutation is created by taking the mean value between the parents
        rule = random.choice(rules)
        r1 = parent1[rule]
        r2 = parent2[rule]

        if rule == 'Rule1': # rule 1 has one parameter
            mean = int((r1+r2)/2)
            child[rule] = mean

        else: # all other rules has a list of parameters
            mean_val_one = int((r1[0]+r2[0])/2)
            mean_val_two = int((r1[1]+r2[1])/2)
            child[rule] = [mean_val_one, mean_val_two]
    
    return child

def create_offspring(population: list, nim_size: int, mutation_prob: float) -> list:
    """Creates the offspring by taking 2 parents using tournament and then doing a crossover with these parents"""
    offspring = []
    for i in range(OFFSPRING_SIZE):
        parent1 = tournament(population=population, nim_size=nim_size) # find parent1
        parent2 = tournament(population=population, nim_size=nim_size) # find parent2

        child = crossover(parent1, parent2, mutation_prob=mutation_prob)
        
        offspring.append(child)
        
    return offspring

def get_next_generation(population: list) -> list:
    """Sort the population based on fitness return the top POPULATION_SIZE best individuals"""
    best_k_indv = sorted(population, key=lambda child: child['fitness'], reverse=True)[:POPULATION_SIZE]
    return best_k_indv


def evolution_agent(nim_size: int):
    """Agent using the evolution strategy"""
    population = init_population(nim_size=nim_size) 
    logging.debug(f"Initial pop {population}")
    
    for _ in range(GENERATIONS):
        offspring = create_offspring(population, nim_size, 0.2)
        logging.debug(f"Created Offspring {offspring}")
        calculate_fitness(population=offspring, nim_size=nim_size)
        logging.debug(f"Calculated fitness {offspring}")
        population = get_next_generation(population=offspring)
        
    best_indv = population[0]
    
    return best_indv

    