# Lab 3
## Colaborators and co-authors
I colaborated and wrote the code together with Leonor Gomes, Mathias Schmekel, Karl Wennerström and Erik Bengtsson.

## Other sources
A big part of the professor's code was used and inspiration was taken from it. 
[Code from professor](https://github.com/squillero/computational-intelligence/blob/master/2022-23/lab3_nim.ipynb)

# Structure of folder
Files and explanations:
- battleground.py -> the file that plays the game of nim with all the agents that were created for this lab
- other_agents.py -> contains the hardcoded-agent and expert agent for task 3.1 as well as some other agents
- utils.py -> contains the Nim-class as well as other helpfunction
- genetic_algorithm.py -> contains the evolved agent for task 3.2
- min_max_agent.py -> contains the min_max-agent
- reinforcement_learning.py -> contains the q-learning agnet
- lab3.ipynb -> was used to create 3.1 and 3.2 before refactoring the code and using the "battleground"
- q-learning.ipynb -> was used to create the q-learner, not used anymore since the "reinforcement_learning.py" took its place

## Evolutionary algorithm
### Rules
Structure of an individual:
```
indv = {'Rule1': a, 'Rule2': [b, c], 'Rule3': [d, e], 'Rule4': [f, g], 'Rule5': [h, i], 'fitness': k}
```
 Parameters:
- a, c, e, g and i = how many elems should be left in a row after the agent has played (if the parameter > elem in row -> take one elem),
- b, d, f, h = indicates which row to pick from, depending on rule.

The rules whoose parameters are evolved:
1. If only one active row left on the board, leave a number of parameters.
2. If even amount of active rows are left in the board and only one of the rows has more than 1 elem:
    - if b = 0, take from row with only one elem
    - if b = 1, leave c amounts of elem in row.
3. If even amount of active rows are left in the board and more than 2 rows have multiple elems:
    - if d = 0, leave e elem in the shortest row
    - if d = 1, leave e elem in the longest row
4. If odd amount of active rows are left in the board and only one of the rows has more than 1 elem:
    - if f = 0, take from row with only one elem
    - if f = 1, leave g amounts of elem in row.
5. If odd amount of active rows are left in the board and more than 2 rows have multiple elems:
    - if h = 0, leave i elem in the shortest row
    - if h = 1, leave i elem in the longest row <br />

### Explanation of algorithm
1. Create inital population (with POPULATION_SIZE) where each player has the same set of rules but different parameters.
2. Generate offspring where OFFSPRING_SIZE>>POPULATION_SIZE:
    - k individuals compete against each other and the fittest becomes a parent. This is done twice for two parents to be created.
    - Preform crossover between two parents and create one child. Thechild is mutated based on a probability.
3. To calculate fitness each child plays 10 games against each of the three agents, one dumb, one random and one optimal.
    - The fitness = (wins_against_optimal_agent, wins_against_random_agent, wins_against_dumb_agent)
3. The top fittest children of size POPULATION_SIZE are selected. 
4. Repeat 2-3 steps GENERATION amount of times
5. The rules of the best individuals become the stratetgy.

### Possible improvements
1. Try different rules and add more rules
2. Create an agent class that keeps track of the rules -> will probably be easier to understand the code and add/remove rules

### Min-Max
For the min-max a lot of code and inspiration was taken from this article
[Min-max article with code example](https://realpython.com/python-minimax-nim/). For some reason I don't understand, the minimax_pruning is not working. 

### An agent using reinforcement learning (Q-learning)
The reinforcement learning agent is using a q-learning algorithm where the exploration rate is decreasing during the training. The agent is trained against 5 different opponents which ranges from dumb to optimal. The structure of the q-learner is a hashmap that looks like the following:
``
{(state_rows: list, move: tuple(row, elem)): int}
´´´
The key contains the current state as a list as well as one possible move for that state, the value is then the q-value given by the q-learning algorithm. 

The Q-learner wins some games against the optimal strategy after the training. <br />
The following links where used to create this agent and the code was heavily inspired by the two code examples.
[Article](https://andrewrowell.blog/2020/05/19/q-learning-nim-with-python/) <br />
[Example of code](https://github.com/abelmariam/nimPy/blob/master/Agent.py) <br />
[Example of code](https://github.com/abelmariam/nimPy) <br />
[Wiki: q-learning](https://en.wikipedia.org/wiki/Q-learning)<br />
[Master theisis on q-learning and nim](https://www.csc.kth.se/utbildning/kth/kurser/DD143X/dkand11/Group6Lars/erik.jarleberg.report.pdf)<br />