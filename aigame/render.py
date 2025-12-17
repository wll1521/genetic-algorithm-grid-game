import pyxel
import random
import copy

from .constants import ACTIONS

# Render Game Function
def render_game(agent, seed, initial_items, initial_terrain, title="AI Grid Game", max_frames=None):
    Game(seed=seed, agent=agent, initial_items=initial_items, initial_terrain=initial_terrain, title=title, max_frames=max_frames)

# Game Class for Rendering
class Game:
    def __init__(self, seed=None, agent=None, initial_items=None, initial_terrain=None, title="AI Grid Game", max_frames=None):
        # Initialize game state
        if seed is not None:
            random.seed(seed)
            self.seed = seed
        else:
            self.seed = None

        self.game_won = False

        pyxel.init(160, 160, fps=5)
        pyxel.title = title

        self.grid_width = 10
        self.grid_height = 10
        self.tile_size = 16

        self.player_x = self.grid_width // 2
        self.player_y = self.grid_height // 2

        self.score = 100

        if initial_items is not None and initial_terrain is not None:
            # Use initial items and terrain
            self.items = copy.deepcopy(initial_items)
            self.terrain = initial_terrain
        else:
            self.generate_items()
            self.generate_terrain()

        self.movement_costs = {
            'normal': 1,
            'mud': 10,
            'water': 50
        }

        self.visible_tiles = set()
        self.update_visibility()

        self.agent = agent
        self.action_index = 0

        self.items_collected = 0
        self.total_movement_cost = 0

        self.max_frames = max_frames  # Number of frames to render before auto-quitting
        self.current_frame = 0

        pyxel.run(self.update, self.draw)

    def generate_items(self):
        self.items = {}
        for _ in range(5):  # Spawn only 5 items
            while True:
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                if (x, y) != (self.player_x, self.player_y) and (x, y) not in self.items:
                    self.items[(x, y)] = 'positive'  # Only positive items
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

    def reset_game(self):
        # Reset the seed
        if self.seed is not None:
            random.seed(self.seed)
        self.game_won = False
        self.player_x = self.grid_width // 2
        self.player_y = self.grid_height // 2
        self.score = 100
        self.items_collected = 0
        self.total_movement_cost = 0
        self.action_index = 0
        self.visible_tiles = set()
        self.update_visibility()

        # Regenerate items and terrain
        self.generate_items()
        self.generate_terrain()

    def check_for_replay(self):
        if pyxel.btnp(pyxel.KEY_R):  # Replay key
            self.reset_game()

    def update(self):
        self.current_frame += 1

        if self.game_won or self.score <= 0:
            self.check_for_replay()  # Listen for replay key
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            return

        if self.agent and self.action_index < len(self.agent.genome):
            action = self.agent.genome[self.action_index]
            self.move_player_action(action)
            self.action_index += 1
            self.check_win_condition()
        else:
            pass  # No more actions

        if self.max_frames is not None and self.current_frame >= self.max_frames:
            pyxel.quit()

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

    def draw(self):
        pyxel.cls(0)

        # Draw grid with terrain types
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in self.visible_tiles:
                    terrain = self.terrain.get((x, y), 'normal')
                    color = {
                        'normal': 11,  # Green
                        'mud': 4,      # Brown
                        'water': 12    # Blue
                    }[terrain]
                    pyxel.rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size, color)
                else:
                    pyxel.rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size, 0)

        # Draw items if visible
        for (x, y), item in self.items.items():
            if (x, y) in self.visible_tiles:
                pyxel.circ(x * self.tile_size + 8, y * self.tile_size + 8, 4, 14)  # Yellow

        # Draw the player
        if self.score > 0 and not self.game_won:
            pyxel.rect(self.player_x * self.tile_size, self.player_y * self.tile_size, self.tile_size, self.tile_size, 9)  # Red

        # Draw game stats
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(5, 15, f"Items Collected: {self.items_collected}", 7)
        pyxel.text(5, 25, f"Movement Cost: {self.total_movement_cost}", 7)
        if self.agent and self.agent.fitness is not None:
            pyxel.text(5, 35, f"Fitness: {self.agent.fitness:.2f}", 7)

        # Game Over and Win Screens
        if self.score <= 0:
            pyxel.text(50, 80, "Game Over!", pyxel.frame_count % 16)
            pyxel.text(40, 90, "Press 'R' to Replay", 8)
            pyxel.text(40, 100, "Press 'Q' to Quit", 8)
        elif self.game_won:
            pyxel.text(50, 80, "You Win!", pyxel.frame_count % 16)
            pyxel.text(40, 90, "Press 'R' to Replay", 8)
            pyxel.text(40, 100, "Press 'Q' to Quit", 8)