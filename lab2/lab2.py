import random
import logging
from collections import namedtuple
from operator import attrgetter

def problem(N, seed=None):
    """Creates a list of lists that contains a random amount of numbers between 0 and N-1."""
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

Individual = namedtuple("Individual", ["genome", "fitness"])

def unique(solution):
    """Count the number of unique values in the solution code from https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists"""
    unique = set([item for sublist in solution for item in sublist])
    return len(unique)

def fitness(genome, N): 
    """Optimal fitness=0. A penalty is given for the number of duplicated elements and also for the number of values not covered by the solution"""
    fitness = 0
    
    #count the number of elements in the genome
    size = len([item for sublist in genome for item in sublist])
    
    unique_values = unique(genome)
    
    #the fitness relates to the total number of element in the genome devided by unique elements
    fitness = N*(size/unique_values)

    #number of values not covered by the genome
    values_left = N - unique_values

    if (values_left > 0):
        fitness = fitness + N*values_left

    return fitness

def mutation(individual, P, N):
    """Change one gene (list) inside the solution by randomly selecting one and swapping it for a new one from the original problem"""
    index = random.randrange(len(individual.genome))
    old_gene = individual.genome.pop(index)

    P_index = random.randrange(len(P))
    new_gene = P[P_index]
    
    new_genome = individual.genome + [new_gene]
    new_fitness = fitness(new_genome, N)
    
    new_individual = Individual(new_genome, new_fitness)

    return new_individual

def crossover(first_individual, second_individual, N):
    """Create two new childern from two parents by slicing them at a random place(interval)"""
    minimum_size = min(len(first_individual.genome), len(second_individual.genome))

    interval = random.randrange(minimum_size)

    first_child_genome = first_individual.genome[:interval] + second_individual.genome[interval:]
    second_child_genome = second_individual.genome[:interval] + first_individual.genome[interval:]

    first_child = Individual(first_child_genome, fitness(first_child_genome, N))
    second_child = Individual(second_child_genome, fitness(second_child_genome, N))

    return first_child, second_child

def select_parent(population, TOURNAMENT_SIZE=5):
    """Selecting a parent using a tournament where five random parents compete agains each other and the best one gets selected"""
    tournament = []

    while len(tournament) != TOURNAMENT_SIZE: 
        random_id = random.randrange(len(population))
        choosen_individual = population[random_id]
        
        tournament.append(choosen_individual)

    tournament.sort(key=attrgetter('fitness'))
    
    return tournament[0]
    

def generate_individual(P):
    """Generate a new individual by taking a random amount of lists from the original problem P"""
    individual_size = random.randrange(1, len(P))
    individual = random.sample(P, individual_size)

    return individual

def generate_population(P, POPULATION_SIZE, N):
    """Generates a random new population of size=POPULATION_SIZE"""
    population = []

    for i in range(POPULATION_SIZE):

        new_individual = generate_individual(P)

        if new_individual not in population: 
            population.append(Individual(new_individual, fitness(new_individual, N)))

    return population


def create_new_population(population, offspring, POPULATION_SIZE):
    """Creates a new population that consist of the 15 best parents and the 15 best offspring in regards to thier fitness"""
    new_population = []

    #Sorts the list from fitesst to least fit
    population.sort(key=attrgetter('fitness'))
    offspring.sort(key=attrgetter('fitness'))
    
    best_fitness = min(population[0].fitness, offspring[0].fitness)
    new_population = population[:int(POPULATION_SIZE/2)] + offspring[:int(POPULATION_SIZE/2)]
    
    return new_population, best_fitness
    


def create_offspring(population, P, N, POPULATION_SIZE):
    """Generates offspring the same size as the population. Each offspring is created by crossover and some will be mutated as well"""
    offspring = []

    for i in range(int(POPULATION_SIZE/2)):
        tournament_parent = select_parent(population)
        
        #select a parent randomly
        random_id = random.randrange(POPULATION_SIZE)
        random_parent = population[random_id]

        first_child, second_child = crossover(tournament_parent, random_parent, N)

        #small possibility that the child will be mutated
        if random.random() < 0.4:
            first_child = mutation(first_child, P, N)

        if random.random() < 0.4:
            second_child = mutation(second_child, P, N)

        offspring.append(first_child)
        offspring.append(second_child)

    return offspring

def escape_local_optima(population, P, N):
    """Creates a new population by mutating all individuals in the population"""
    new_population = []

    for i in range(len(population)):
        
        new_individual = mutation(population[i], P, N)
        new_population.append(new_individual)

    return new_population

def genetic_algorithm(P, N, generations, POPULATION_SIZE):
    """Use stady state to generate the best solution."""
    #create inital population
    population = generate_population(P,POPULATION_SIZE, N)

    
    population.sort(key=attrgetter('fitness'))
    
    #save the best fintess found so far
    current_best_fitness = population[0].fitness
    
    #used to keep track of local optima
    counter = 0

    while generations > 0:
        offspring = create_offspring(population, P, N, POPULATION_SIZE)
        population, new_best_fitness = create_new_population(population, offspring, POPULATION_SIZE)
        
        #if the solution has not improved -> potential local optima
        if (new_best_fitness == current_best_fitness):
            counter += 1
        else:
            counter = 0
            current_best_fitnes = new_best_fitness

        #If stuck in a local optima
        if (counter == 5):
            population = escape_local_optima(population, P, N)
        
        generations -= 1
    
    population.sort(key=attrgetter('fitness'))
    
    logging.info(f'Solution found: N={N}: weight={sum([len(l) for l in population[0].genome])} \n Final individual: {population[0]} \n')
    return population[0] 

logging.getLogger().setLevel(logging.INFO)
    
POPULATION_SIZE = 30
GENERATIONS = 500
SEED = 42

for N in [5, 10, 20, 100, 500, 1000]:   
    P = problem(N, SEED) 
    final_solution = genetic_algorithm(P, N, GENERATIONS, POPULATION_SIZE)
