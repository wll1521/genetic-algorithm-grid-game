import random

from .constants import GENOME_LENGTH

# Crossover Operators: Corssover between two genomes
def two_point_crossover(genome1, genome2):
    if GENOME_LENGTH < 3:
        # Ensure there are at least two crossover points
        return genome1.copy()
    point1 = random.randint(1, GENOME_LENGTH - 2)
    point2 = random.randint(point1 + 1, GENOME_LENGTH - 1)
    child_genome = genome1[:point1] + genome2[point1:point2] + genome1[point2:]
    return child_genome

# Mutation Operators: swaps two genes within probability
def swap_mutation(genome, mutation_rate):
    genome = genome.copy()  # To avoid modifying the original genome
    for i in range(len(genome)):
        if random.random() < mutation_rate:
            swap_idx = random.randint(0, len(genome) - 1)
            genome[i], genome[swap_idx] = genome[swap_idx], genome[i]
    return genome