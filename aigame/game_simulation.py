import random
import copy

from .constants import ACTIONS

class GameSimulation:
    def __init__(self, seed=None, initial_items=None, initial_terrain=None):
        if seed is not None:
            random.seed(seed)
            self.seed = seed
        else:
            self.seed = None

        self.grid_width = 10
        self.grid_height = 10

        self.player_x = self.grid_width // 2
        self.player_y = self.grid_height // 2

        self.score = 100

        if initial_items is not None and initial_terrain is not None:
            self.initial_items = initial_items
            self.initial_terrain = initial_terrain
        else:
            # Generate items and terrain
            self.generate_items()
            self.generate_terrain()
            self.initial_items = copy.deepcopy(self.items)
            self.initial_terrain = copy.deepcopy(self.terrain)

        # Going into water is bad. Kept high cost
        self.movement_costs = {
            'normal': 1,
            'mud': 10,
            'water': 50
        }

        self.visible_tiles = set()
        self.update_visibility()

        self.game_won = False

        # Tracking variables
        self.total_movement_cost = 0
        self.items_collected = 0
        self.positions_visited = set()  # For advanced fitness
        self.positions_visited.add((self.player_x, self.player_y))
        self.position_visit_counts = {(self.player_x, self.player_y): 1}  # Starting position visited once

    def generate_items(self):
        self.items = {}
        for _ in range(5):  # Spawn only 5 items
            while True:
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                if (x, y) != (self.player_x, self.player_y) and (x, y) not in self.items:
                    self.items[(x, y)] = 'positive'  # Only positive items for positive points
                    break

    def generate_terrain(self):
        self.terrain = {}
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                terrain_type = random.choices(
                    ['normal', 'mud', 'water'],
                    weights=[0.7, 0.2, 0.1],
                    k=1
                )[0]
                self.terrain[(x, y)] = terrain_type

    def update_visibility(self):
        x, y = self.player_x, self.player_y
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                    self.visible_tiles.add((nx, ny))

    def simulate(self, agent):
        # Resets game state for each simulation
        self.player_x = self.grid_width // 2
        self.player_y = self.grid_height // 2
        self.score = 100
        self.visible_tiles = set()
        self.update_visibility()
        self.game_won = False

        # Resets tracking variables
        self.total_movement_cost = 0
        self.items_collected = 0
        self.positions_visited = set()
        self.positions_visited.add((self.player_x, self.player_y))
        self.position_visit_counts = {(self.player_x, self.player_y): 1}  # Starting position visited once

        # Resets items and terrain to initial state
        self.items = copy.deepcopy(self.initial_items)
        self.terrain = self.initial_terrain  # Terrain doesn't change during the game

        for action in agent.genome:
            if self.score <= 0 or self.game_won:
                break
            self.move_player_action(action)
            self.check_win_condition()
            if self.game_won:
                break

        agent.fitness = self.calculate_fitness()
        agent.items_collected = self.items_collected
        agent.total_movement_cost = self.total_movement_cost

    def move_player_action(self, action):
        dx, dy = ACTIONS.get(action, (0, 0))
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
            # Get the terrain of the new tile
            terrain = self.terrain.get((new_x, new_y), 'normal')
            # Get the movement cost
            cost = self.movement_costs.get(terrain, 1)
            # Deduct the cost from the score
            self.score -= cost
            # Accumulate movement cost
            self.total_movement_cost += cost
            # Update player's position
            self.player_x = new_x
            self.player_y = new_y
            self.check_for_items()
            self.update_visibility()
            if self.score <= 0:
                self.score = 0

            # Update visit counts
            pos = (new_x, new_y)
            if pos in self.position_visit_counts:
                self.position_visit_counts[pos] += 1
            else:
                self.position_visit_counts[pos] = 1
            self.positions_visited.add(pos)  # Only needs to be added once

    def check_for_items(self):
        if (self.player_x, self.player_y) in self.items:
            item = self.items.pop((self.player_x, self.player_y))
            if item == 'positive':
                self.score += 15
                self.items_collected += 1

    def check_win_condition(self):
        all_items_collected = len(self.items) == 0
        all_tiles_explored = len(self.visible_tiles) == self.grid_width * self.grid_height
        if all_items_collected and all_tiles_explored:
            self.game_won = True

    def calculate_fitness(self):
        items_collected = self.items_collected
        total_movement_cost = self.total_movement_cost
        score = self.score
        uncollected_items = 5 - items_collected  # Assumes 5 items

        # Other metrics for exploration and backtracking
        unique_positions = len(self.positions_visited)
        total_positions_visited = sum(self.position_visit_counts.values())
        revisits = total_positions_visited - unique_positions  # Number of times positions were revisited

        # Fitness calculation
        fitness = (
            (items_collected * 300)              # Reward for collecting items / default 300
            - (total_movement_cost * 2)        # Penalize movement cost / default 2
            + (score * 1.5)                         # Include remaining score / default 1.5
            - (uncollected_items * 150)           # Penalize uncollected items / default 150
            + (unique_positions * 15)             # Reward for exploring unique tiles / default 15
            - (revisits * 10)                      # Penalize for backtracking / default 10
        )

        return fitness