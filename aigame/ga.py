import copy
import pickle
import matplotlib.pyplot as plt
import numpy as np

from .constants import (
    GENOME_LENGTH,
    POPULATION_SIZE,
    GENERATIONS,
    INITIAL_MUTATION_RATE,
    MIN_MUTATION_RATE,
    ELITE_SIZE,
    IMMIGRATION_RATE,
    STAGNATION_THRESHOLD,
    SELECTION_METHOD
)
from .agent import Agent
from .game_simulation import GameSimulation
from .selection import adaptive_tournament_selection, rank_based_selection
from .operators import two_point_crossover, swap_mutation
from .render import render_game

def genetic_algorithm():
    global INITIAL_MUTATION_RATE 

    # Initialize population
    population = [Agent() for _ in range(POPULATION_SIZE)]
    seed = 42  # Fixed seed for consistent terrain and items

    # Generate initial items and terrain
    temp_game = GameSimulation(seed=seed)
    initial_items = temp_game.initial_items
    initial_terrain = temp_game.initial_terrain

    # Logging for visualization
    best_fitness_history = []
    avg_fitness_history = []
    worst_fitness_history = []
    unique_positions_history = []  # For plotting exploration
    revisits_history = []           # For plotting backtracking
    # actions_taken_history = []    # Not tracked currently

    # Tracking for dynamic mutation rate
    best_fitness_overall = float('-inf')
    generations_without_improvement = 0

    for generation in range(GENERATIONS):
        # Evaluates fitness for each agent
        for agent in population:
            game_sim = GameSimulation(seed=seed, initial_items=initial_items, initial_terrain=initial_terrain)
            game_sim.simulate(agent)

        # Sorts population by fitness
        population.sort(key=lambda x: x.fitness, reverse=True)
        best_agent = population[0]
        worst_agent = population[-1]
        avg_fitness = sum(agent.fitness for agent in population) / POPULATION_SIZE

        # Logs fitness and new metrics
        best_fitness_history.append(best_agent.fitness)
        avg_fitness_history.append(avg_fitness)
        worst_fitness_history.append(worst_agent.fitness)
        unique_positions_history.append(len(best_agent.positions_visited))
        revisits = sum(best_agent.position_visit_counts.values()) - len(best_agent.positions_visited)
        revisits_history.append(revisits)
        # actions_taken_history.append(best_agent.actions_taken)  # Not tracked currently

        # Prints generation statistics
        print(f"Generation {generation}, Best fitness: {best_agent.fitness:.2f}, "
              f"Average fitness: {avg_fitness:.2f}, Items Collected: {best_agent.items_collected}, "
              f"Movement Cost: {best_agent.total_movement_cost}, "
              f"Unique Positions: {len(best_agent.positions_visited)}, Revisits: {revisits}")

        # Checks for improvement
        if best_agent.fitness > best_fitness_overall:
            best_fitness_overall = best_agent.fitness
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1

        # Detects stagnation
        if generations_without_improvement >= STAGNATION_THRESHOLD:
            print(f"Stagnation detected at generation {generation}. Increasing mutation rate.")
            INITIAL_MUTATION_RATE = min(INITIAL_MUTATION_RATE * 1.5, 1.0)  # Cap mutation rate at 1.0
            generations_without_improvement = 0  # Reset counter after increasing mutation rate

        # Selection and reproduction
        next_generation = population[:ELITE_SIZE]  # Elitism: retain top agents

        while len(next_generation) < POPULATION_SIZE:
            if SELECTION_METHOD == 'adaptive_tournament':
                parent1 = adaptive_tournament_selection(population, generation)
                parent2 = adaptive_tournament_selection(population, generation)
            elif SELECTION_METHOD == 'rank_based':
                parent1 = rank_based_selection(population)
                parent2 = rank_based_selection(population)
            else:
                raise ValueError("Invalid SELECTION_METHOD. Choose 'adaptive_tournament' or 'rank_based'.")

            # Performs two-point crossover
            child_genome = two_point_crossover(parent1.genome, parent2.genome)
            # Performs swap mutation
            child_genome = swap_mutation(child_genome, INITIAL_MUTATION_RATE)
            # Creates a new agent
            next_generation.append(Agent(genome=child_genome))

        # Introduces random immigrants to maintain diversity
        num_immigrants = int(IMMIGRATION_RATE * POPULATION_SIZE)
        for _ in range(num_immigrants):
            next_generation.append(Agent())

        # Truncate to maintain population size
        population = next_generation[:POPULATION_SIZE]

        # Decrease mutation rate over generations dynamically
        INITIAL_MUTATION_RATE = max(MIN_MUTATION_RATE, INITIAL_MUTATION_RATE * 0.99) #can change to 0.999

    # After all generations are complete, output the best agent's performance
    best_agent = population[0]
    print("\nBest Agent after all generations:")
    print(f"Fitness: {best_agent.fitness:.2f}")
    print(f"Items Collected: {best_agent.items_collected}")
    print(f"Total Movement Cost: {best_agent.total_movement_cost}")
    print(f"Unique Positions: {len(best_agent.positions_visited)}")
    revisits = sum(best_agent.position_visit_counts.values()) - len(best_agent.positions_visited)
    print(f"Revisits: {revisits}")
    # print(f"Actions Taken: {best_agent.actions_taken}")  # Not tracked currently

    # Saves the best agent's genome
    with open('best_agent.pkl', 'wb') as f:
        pickle.dump(best_agent.genome, f)
    print("Best agent's genome saved to 'best_agent.pkl'.")

    # Plots fitness over generations
    plt.figure(figsize=(12, 6))
    plt.plot(best_fitness_history, label='Best Fitness', color='green')
    plt.plot(avg_fitness_history, label='Average Fitness', color='blue')
    plt.plot(worst_fitness_history, label='Worst Fitness', color='red')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over Generations')
    plt.legend()
    plt.grid(True)
    plt.savefig('fitness_over_generations.png')
    plt.show()

    # Plots exploration and backtracking over generations
    plt.figure(figsize=(12, 6))
    plt.plot(unique_positions_history, label='Unique Positions', color='purple')
    plt.plot(revisits_history, label='Revisits', color='orange')
    plt.xlabel('Generation')
    plt.ylabel('Count')
    plt.title('Exploration and Backtracking over Generations')
    plt.legend()
    plt.grid(True)
    plt.savefig('exploration_backtracking_over_generations.png')
    plt.show()

    # Renders the best agent's run
    print("\nRendering the best agent from the final generation...")
    render_game(best_agent, seed, initial_items, initial_terrain, title="Best Agent - Final Generation", max_frames=None)