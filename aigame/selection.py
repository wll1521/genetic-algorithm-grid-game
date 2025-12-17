import random
import numpy as np

from .constants import TOURNAMENT_SIZE_MIN, TOURNAMENT_SIZE_MAX, GENERATIONS

# Selection Mechanisms

# Determine tournament size based on current generation (increases over generations linearly)
def adaptive_tournament_selection(population, current_generation):
    k = TOURNAMENT_SIZE_MIN + int(
        (TOURNAMENT_SIZE_MAX - TOURNAMENT_SIZE_MIN) * (current_generation / GENERATIONS)
    )
    k = min(max(k, TOURNAMENT_SIZE_MIN), TOURNAMENT_SIZE_MAX)

    candidates = random.sample(population, k)
    winner = max(candidates, key=lambda x: x.fitness)
    return winner

# Rank-based selection assigns selection probability based on rank.
# Higher-ranked agents have higher probability of being selected.
def rank_based_selection(population):
    # Sorts population by fitness in descending order
    sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)

    # Assigns ranks: 1 for best, 2 for second best, etc.
    ranks = range(1, len(sorted_population) + 1)

    # Assigns selection probabilities inversely proportional to rank
    total = sum(range(1, len(sorted_population) + 1))
    selection_probs = [(len(sorted_population) - rank + 1) / total for rank in ranks]

    # Selects one agent based on the assigned probabilities
    selected_agent = np.random.choice(sorted_population, p=selection_probs)
    return selected_agent