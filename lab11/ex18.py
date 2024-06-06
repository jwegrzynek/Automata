import numpy as np
from scipy.signal import convolve2d
import random


def generate_random_grid(size, tree_prob):
    return np.array(
        [[np.random.choice([0, 1], p=[1 - tree_prob, tree_prob]) for _ in range(size)] for _ in range(size)], dtype=int)


grid = generate_random_grid(10, 0.8)
print(grid)


# Define the kernel
kernel = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])


def update_grid(grid, f, p):
    # Calculate the number of neighbors for each cell
    neighbors = convolve2d(grid, kernel, mode='same', boundary='wrap').astype(int)
    # Initialize the new grid
    new_grid = grid.copy()
    # Iterate over each cell in the grid
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            # Apply the Forest Fire Model rule
            if grid[i, j] == 1 and random.random() < f:
                new_grid[i, j] = 2
            if grid[i, j] == 0 and random.random() < p:
                new_grid[i, j] = 1

    return new_grid


print(update_grid(grid,0.1, 0.1))

neighbors = convolve2d(grid, kernel, mode='same', boundary='wrap').astype(int)
print(neighbors)