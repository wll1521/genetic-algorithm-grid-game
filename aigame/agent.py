import random

from .constants import GENOME_LENGTH

# Agent is created with random genome
class Agent:
    def __init__(self, genome=None):
        if genome is None:
            self.genome = [random.randint(0, 3) for _ in range(GENOME_LENGTH)]
        else:
            self.genome = genome
        self.fitness = None
        self.items_collected = 0
        self.total_movement_cost = 0
        self.positions_visited = set()
        self.position_visit_counts = {}
        self.actions_taken = 0  # For potential future use