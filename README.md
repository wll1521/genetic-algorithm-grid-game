# Genetic Algorithm Grid Game

This project implements a genetic algorithm to evolve an intelligent agent that navigates a 10x10 grid-based game that I originally made for manual player input control. The agent now learns to collect items while minimizing movement costs across varied terrain (normal, mud, water) on its own. It uses evolutionary techniques like adaptive tournament selection, two-point crossover, swap mutation, elitism, and immigration to optimize performance. The simulation includes fitness tracking for exploration and backtracking, with visualization via Matplotlib plots and real-time rendering using the Pyxel engine.

The goal is to demonstrate how genetic algorithms can solve pathfinding and resource management problems in a simple game environment. It's ideal for educational purposes, AI experimentation, or as a starting point for more complex evolutionary computing projects.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wll1521/genetic-algorithm-grid-game.git
   cd genetic-algorithm-grid-game

2. Create and activate a virtual environment (recommended):
   ```bash
    python -m venv venv
    venv\Scripts\activate #For Windows OS
   
3. Install dependencies:
    ```bash
    pip install -r requirements.txt

## Run

    ```bash
    python -m main


# Dependencies
- pyxel: For game rendering.
- matplotlib: For plotting fitness and exploration data.
- numpy: For numerical operations in selection mechanisms.

# Notes

I was originally limited by hardware restrictions when this was made, so feel free to increase population / generation sizing along with other constraints.
