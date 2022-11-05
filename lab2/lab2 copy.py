import logging
from collections import namedtuple
from operator import index
import random
from matplotlib import pyplot as plt

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
            for n in range(random.randint(N, N * 5))
    ]
  
SEED=42
N=[5, 10, 20, 100, 500, 1000]
GOAL_N=3
#PROBLEM_SPACE= sorted(list(set(tuple(i) for i in problem(N[GOAL_N],seed=SEED))), key= lambda a : len(a))
PROBLEM_SPACE= list(set(tuple(i) for i in problem(N[GOAL_N],seed=SEED)))
PROBLEM_SIZE = len(PROBLEM_SPACE)
POPULATION_SIZE = 150
OFFSPRING_SIZE = 100
NUM_GENERATIONS = 1000 #20*N[GOAL_N]
Individual = namedtuple("Individual", ["genome", "fitness"])
logging.getLogger().setLevel(logging.INFO)

def fitnessFunc(genome):
        # Compute in parallel the coverage and the length of the genome solution
        tuple_set = set()
        genome_lenght=0
        for index,i in enumerate(genome):
            if i==1:
                tuple_set |= set(PROBLEM_SPACE[index])
                genome_lenght+=len(PROBLEM_SPACE[index])
        genome_coverage=len(tuple_set)
        # Adding a penalty if not valid (coverage < 100%)
        malus = 0
        if genome_coverage != N[GOAL_N]:
            malus = genome_lenght
        return 3*genome_coverage - genome_lenght - malus

# Get the actual solution from the genome one
def getPhenotype(genome):
    phenotype=[]
    for index,i in enumerate(genome): 
        if i==1:
            phenotype.append(PROBLEM_SPACE[index])
    return phenotype

# Used to compute the coverage of a solution (called in the print)
def coverage(genome):
    coverage_set=set()
    for index,i in enumerate(genome): 
        if i==1:
            coverage_set|=set(PROBLEM_SPACE[index])
    return len(coverage_set)

def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)

def cross_over(g1, g2):
    cut = random.randint(0, PROBLEM_SIZE)
    son= g1[:cut] + g2[cut:]
    return mutation(son)

def mutation(g,rounds=1):
    for i in range(rounds):
        point = random.randint(0, PROBLEM_SIZE - 1)
        p=g[:point] + (1 - g[point],) + g[point + 1 :]
    return p

population = list()

for genome in [tuple([random.choice([1, 0]) for _ in range(PROBLEM_SIZE)]) for _ in range(POPULATION_SIZE)]:
    population.append(Individual(genome, fitnessFunc(genome)))

logging.debug(f"init: pop_size={len(population)}; max={max(population, key=lambda i: i.fitness)[1]}")

fitness_log = [(0, i.fitness) for i in population]

for g in range(NUM_GENERATIONS):
    offspring = list()
    for i in range(OFFSPRING_SIZE):
        if random.random() < 0.8:
            p = tournament(population)
            o = mutation(p.genome,5)
        else:
            p1 = tournament(population)
            p2 = tournament(population)
            o = cross_over(p1.genome, p2.genome)
        
        f = fitnessFunc(o)
        fitness_log.append((g + 1, f))
        offspring.append(Individual(o, f))
    population += offspring

    population = sorted(population, key=lambda i: i.fitness, reverse=True)[:POPULATION_SIZE]
for individual in population[0:10]:
    logging.info(f"FITNESS :{fitnessFunc(individual.genome)}\n COVERAGE: {coverage(individual.genome)} \n LENGHT: {sum(len(element) for element in getPhenotype(individual.genome))}")

logging.info(f"Fitness count {NUM_GENERATIONS * OFFSPRING_SIZE + POPULATION_SIZE}")

off_line = [max(f[1] for f in fitness_log if f[0] == x) / (x + 1) for x in range(NUM_GENERATIONS)]
on_line = [max(f[1] for f in fitness_log if f[0] <= x) / (x + 1) for x in range(NUM_GENERATIONS)]
gen_best = [max(f[1] for f in fitness_log if f[0] == x) for x in range(NUM_GENERATIONS)]

plt.figure(figsize=(15, 6))
plt.scatter([x for x, _ in fitness_log], [y for _, y in fitness_log], marker=".")
plt.plot([x for x, _ in enumerate(gen_best)], [y for _, y in enumerate(gen_best)])
plt.plot([x for x, _ in enumerate(on_line)], [y for _, y in enumerate(on_line)])
plt.plot([x for x, _ in enumerate(off_line)], [y for _, y in enumerate(off_line)])