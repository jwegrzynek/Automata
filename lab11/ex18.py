import numpy as np
import random
import pygame


def generate_random_grid(size, tree_prop):
    return np.array(
        [[np.random.choice([0, 1], p=[1 - tree_prop, tree_prop]) for _ in range(size)] for _ in range(size)], dtype=int)


def get_neighborhood(matrix, row, col):
    rows, cols = matrix.shape
    neighborhood = []

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            neighborhood.append(matrix[r, c])

    return neighborhood


def update_grid(grid, f, p):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):

            if grid[i, j] == 1 and 2 in get_neighborhood(grid, i, j):
                new_grid[i, j] = 2

            elif grid[i, j] == 1 and random.random() < f:
                new_grid[i, j] = 2

            elif grid[i, j] == 0 and random.random() < p:
                new_grid[i, j] = 1

            elif grid[i, j] == 2:
                new_grid[i, j] = 0

    return new_grid


grid = generate_random_grid(10, 0.8)
print(grid)

print(update_grid(grid, 0.1, 0.1))

TREE_PROPORTION = 0.5
GROW_TREE_PROB = 0.1
FIRE_PROB = 0.1
