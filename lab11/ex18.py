import numpy as np
import random
import pygame
import time


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


TREE_PROPORTION = 0.5
GROW_TREE_PROB = 0.1
FIRE_PROB = 0.1

running = True
simulation_running = False
last_update_time = time.time()
simulation_speed = 8.00
res = (800, 800)
cell_size = 4

grid = generate_random_grid(int(res[0] / cell_size), 0.8)

pygame.init()
screen = pygame.display.set_mode(res)

while running:

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulation_running = not simulation_running
            elif event.key == pygame.KEYUP:
                simulation_speed += 1.00
            elif event.key == pygame.KEYDOWN:
                simulation_speed -= 1.00

    # Update grid
    if simulation_running and (time.time() - last_update_time > 1 / simulation_speed):
        grid = update_grid(grid, 0.1, 0.1)
        last_update_time = time.time()

    # Draw grid
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 0:
                color = (0, 0, 0)
            elif grid[row, col] == 1:
                color = (34, 139, 34)
            elif grid[row, col] == 2:
                color = (136, 8, 8)
            pygame.draw.rect(screen, color, pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size))

    pygame.display.update()
