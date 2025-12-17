# Genetic Algorithm Constants

GENOME_LENGTH = 500  # Increased from 200 to allow more actions
POPULATION_SIZE = 1000 # 1000 for optimal
GENERATIONS = 110  # Increased from 50 to allow more evolution / 100 for optimal
INITIAL_MUTATION_RATE = 0.05  # Higher initial mutation rate 0.1 for optimal or .2
MIN_MUTATION_RATE = 0.001  # Minimum mutation rate after decay
ELITE_SIZE = 50  # More elite agents for hill climbing / 50 for optimal
IMMIGRATION_RATE = 0.1  # Increased immigration to maintain diversity
STAGNATION_THRESHOLD = 20  # Generations without improvement before diversity injection
TOURNAMENT_SIZE_MIN = 20  # Starting size for tournament selection
TOURNAMENT_SIZE_MAX = 70  # Max size for tournament selection

#default - 500, 400, 100, 0.3, 0.05, 5, 0.1, 10, 2, 10
#optimal - 500,1000, 110, 0.2, 0.05,50,0.01, 20, 20,70 = 2000+ fitness score


# Selection Mechanism Options
SELECTION_METHOD = 'adaptive_tournament'  # Options: 'adaptive_tournament', 'rank_based'


# Movement Actions
ACTIONS = {
    0: (0, -1),  # Up
    1: (0, 1),   # Down
    2: (-1, 0),  # Left
    3: (1, 0),   # Right
}