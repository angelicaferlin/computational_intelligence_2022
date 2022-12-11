from utils import *
from other_agents import *
from genetic_algorithm import *
from reinforcement_learning_agent import *
from min_max_agent import *

NIM_SIZE = 5

def play_nim(agent1: Callable, opponent: Callable):
    """Plays one game of nime where
    player 0 = agent1
    player 1 = opponent"""
    nim = Nim(NIM_SIZE)
    logging.debug(f"status: Initial board  -> {nim}")
    print(f"status: Initial board  -> {nim}")
    
    strategy = (agent1, opponent)
    player = 0

    while nim:
        ply = strategy[player](nim)
        nim.nimming(ply)
        
        logging.debug(f"status: After player {player} -> {nim}")
        print(f"status: After player {player} -> {nim}")
        player = 1 - player
    winner = 1 - player
    logging.info(f"status: Player {winner} won!")
    print(f"status: Player {winner} won!")


def play_nim_with_q_learner(q_learner: QLearner, opponent: Callable):
    """Plays a game of nim with q-learner against opponent"""
    result = play_q_learning(NIM_SIZE, q_learner, opponent)
    print(result)

# Create nim
state = Nim(NIM_SIZE)

# Taslk 3.1 - hardcoded agent usin nim-sum and fixed rules
# Expert Agent (nim-sum) plays against dumb, random and then optimal opponent
play_nim(nim_sum_strategy, dumb)
print("Expert agent played against dumb agent")

play_nim(nim_sum_strategy, random_agent)
print("Expert agent played against the random agent")

play_nim(nim_sum_strategy, optimal_startegy)
print("Expert agent played against optimal agent")

# Hard coded agent plays against dumb, random and optimal
play_nim(hard_coded_agent, dumb)
print("Hard-coded agent played against dumb agent")

play_nim(nim_sum_strategy, random_agent)
print("Hard-coded agent played against the random agent")

play_nim(nim_sum_strategy, optimal_startegy)
print("Hard-coded agent played against optimal agent")


# Task 3.2 - An agent using evolved rules
# Create evoultion agent
evolution_strategy = make_strategy(evolution_agent(NIM_SIZE))

play_nim(evolution_strategy, dumb)
print("Evolved agent played against dumb agent")

play_nim(evolution_strategy, random_agent)
print("Evolved agent played against the random agent")

play_nim(evolution_strategy, optimal_startegy)
print("Evolved agent played against optimal agent")


# Task 3.3 - An agent using minmax
NIM_SIZE = 3 # using size 3 since the agent is slow 
play_nim(min_max_agent, dumb)
print("Min-max agent played against dumb agent")

play_nim(min_max_agent, random_agent)
print("Min-max agent played against the random agent")

play_nim(min_max_agent, optimal_startegy)
print("Min-max agent played against optimal agent")

# Task 3.4 - An agent using reinforcement learning (Q-learning)
NIM_SIZE = 4
# Create q-learning agent
q_learner_strategy = q_learner_strategy(NIM_SIZE)

play_nim_with_q_learner(q_learner_strategy, dumb)
print("Q-learner agent played against dumb agent")

play_nim_with_q_learner(q_learner_strategy, random_agent)
print("Q-learner agent played against the random agent")

play_nim_with_q_learner(q_learner_strategy, optimal_startegy)
print("Q-learner agent played against optimal agent")


