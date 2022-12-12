from utils import *
from other_agents import *

OPPONENTS = [dumb, hard_coded_agent, random_agent, random_smart_agent, optimal_startegy]
#Improvement: play against more agents with wider veriety of level

class QLearner:
    REWARD = 1
    PENALTY = -1
    previous_state = None
    previous_move = None

    def __init__(self, learning_rate, discount_rate, exploration_rate):
       q = {} # structure {(state_rows: list, move: tuple (row, elem)): int, }
       self.q = q
        
       #in a deterministic environment, the optimal learning rate is 1
       #in practice, often a constant learning rate is used
       self.learning_rate = learning_rate
       
       #starting with a lower discount factor and increasing it towards its final value acelerates learning
       self.discount_rate = discount_rate
       
       #try to reduce the exploration rate while we are training the q-learner 
       self.exploration_rate = exploration_rate
    
    def clear_previous_vars(self):
      """Clears the varibles previous state"""
      self.previous_state = None
      self.previous_move = None
    
    def change_exploration_rate(self, new_exploration_rate):
      """Changes the exploration rate"""
      self.exploration_rate = new_exploration_rate

    def change_discount_rate(self, new_discount_rate):
      """Changes the discount rate"""
      self.discount_rate = new_discount_rate

    def change_learning_rate(self, new_learning_rate):
      """Changes the learning rate"""
      self.learning_rate = new_learning_rate

    def add_state_moves(self, current_state): 
      """Adds all the new states (moves) that is not in the current state given a new state. Each state gets a small random Q-value to avoid
      two states having the same q-value"""
      data = cook_status(current_state)
      possible_moves = data['possible_moves']

      for move in possible_moves:
        if (current_state.rows, move) not in self.q: #if the a possible move is not in the current explored states
          self.q[(current_state.rows, move)] = np.random.uniform(0.0,0.01) #attribute a small random value 
    
    
    def policy(self, current_state):
      """Returns the best move given a current state according to the q-learning policy"""
      data = cook_status(current_state)
      possible_moves = data['possible_moves']

      if np.random.random() > self.exploration_rate:
        #want to return the action with the biggest value
        q_val_list = [self.q[(current_state.rows, move)] for move in possible_moves] #list of the values of state and action
        max_val_index = np.argmax(q_val_list) #returns the index of the max element of the array 
        return possible_moves[max_val_index]  #returns the move with the biggest q_value

      else: #exploration
        return random.sample(possible_moves, 1)[0] #returns a random possible move - moves are in tuples
    
    def updateQ(self, current_state): #current_state: Nim
      """Updates the q-learner given a current state"""
      if not current_state: #if the game is finished
        self.q[(self.previous_state, self.previous_move)] += \
                self.learning_rate * (self.PENALTY - self.q[(self.previous_state, self.previous_move)]) 
        current_move = self.previous_state = self.previous_move = None #clear in order to prepare for the next game

      else: #if the game is not finished 
        self.add_state_moves(current_state) 
        current_move = self.policy(current_state) #gets the move that we want to use

        if self.previous_move is not None: #if it is not the first move
          next_state = deepcopy(current_state) 
          next_state.nimming(Nimply(current_move[0], current_move[1])) #get the next state applying the move (result of your move)

          reward = 0 if next_state else self.REWARD #gets the value of the reward, if it wins, reward = 1
          logging.debug(f" REWARD: {reward}")
          data = cook_status(current_state)
          possible_moves = data['possible_moves']

          maxQ = max([self.q[(current_state.rows, move)] for move in possible_moves]) #max q-value from the possible moves of the current_state

          # updates the q-value according to the q-learning algorithm
          self.q[(self.previous_state, self.previous_move)] += \
                    self.learning_rate * (reward + (self.discount_rate * maxQ) - \
                    self.q[(self.previous_state, self.previous_move)])
      

        self.previous_state, self.previous_move = current_state.rows, current_move
        logging.debug(f"current_move - game not finished: {current_move}")
      return current_move

def play_q_learning(nim_size: int, q_learner: QLearner, external_agent: Callable):
  """Plays the game of Nim once against a given opponent"""
  nim = Nim(nim_size)

  game_on = True
  is_q_learner = True #we start with q-learner

  while game_on:

    if is_q_learner: #if the current player is our q_learner
        move_params = q_learner.updateQ(nim)
        logging.debug(f" Wanted move after player = q-learner: {move_params}, State before move: {nim}")
        
        if(move_params == None): #if q_learner loses
            logging.debug(f" Q-learner lost")
            return "q_learner lost"
        
        move_to_apply = Nimply(move_params[0], move_params[1])
        logging.debug(f"move to apply: {move_to_apply}")
        nim.nimming(move_to_apply)
        
        logging.debug(f" <<NIM>> after q-learner move: {nim}")
        
        if(sum(nim.rows) == 0): #if q_learner wins
            logging.debug(f"Q-learner won")
            q_learner.clear_previous_vars()
            
            return "Q_learner won"
        
        is_q_learner = False
    
    else: #if the current player is the external agent
        move_to_apply = external_agent(nim) 
        logging.debug(f"Agent move to apply: {move_to_apply}")
        nim.nimming(move_to_apply)
        is_q_learner = True


def q_learner_strategy(nim_size) -> QLearner: #function to train the q_learner
  """The q-learner is trained by playing against opponents ranging from dumb to optimal where it trains in more
  games the better the agent is"""
  num_games = 200 #when nim_size is small
  #num_games = 50 #when nim_size = 10
  current_exploration_rate = 0.6
  q_learner_agent = QLearner(learning_rate=0.9, discount_rate=0.4, exploration_rate=current_exploration_rate)

  for opponent in OPPONENTS:

    for game in range(num_games):
        play_q_learning(nim_size, q_learner_agent, opponent)
        logging.debug(f" GAME FINISHED")
    
    current_exploration_rate -= 0.10

    if (current_exploration_rate < 0.1):
      current_exploration_rate = 0.1
    
    q_learner_agent.change_exploration_rate(current_exploration_rate)

    num_games += 2*(game+1) # the number of games increases when playing against stronger opponent

    print(f"NUM_GAMES", num_games)
  return q_learner_agent


