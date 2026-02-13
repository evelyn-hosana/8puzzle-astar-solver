# 8-Puzzle A* Solver

A Python implementation of the A* search algorithm for solving the 8-puzzle problem. Compares two heuristics, **Misplaced Tiles (h1)** and **Manhattan Distance (h2)**, and reports optimal solution paths with search performance metrics.

## Heuristics

- **h1 – Misplaced Tiles** — Counts tiles not in their goal position (excluding the blank).
- **h2 – Manhattan Distance** — Sums each tile's horizontal and vertical distance from its goal position. Dominates h1, so A* expands fewer nodes.

The solver also checks **inversion parity** before searching to detect unsolvable puzzles.

## Usage

1. Download/clone this repository
2. Run in terminal:
```
python main.py
```

Enter states as 9 space-separated digits (0–8), where `0` is the blank tile.

```
Enter the initial state: 1 2 3 4 0 5 6 7 8
Enter the goal state: 1 2 3 4 5 6 7 8 0
```

## Project Structure

- `main.py` — User I/O, input validation, result display
- `astar.py` — A* algorithm, heuristics, neighbor generation, solvability check

## Requirements

- Python 3.x (no external dependencies)
