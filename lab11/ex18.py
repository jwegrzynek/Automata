import numpy as np
import matplotlib.pyplot as plt
import random
import pygame
import time


def generate_random_grid(size, tree_prop):
    return np.array(
        [[np.random.choice([0, 1], p=[1 - tree_prop, tree_prop]) for _ in range(size)] for _ in range(size)], dtype=int)


def detect_fire(matrix, row, col, wind_direction=None):
    rows, cols = matrix.shape

    is_fire = False
    is_fire_windside = False

    directions = ((-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1))

    wind_factor = {
        'left': (0, -1),  # Increase probability for left neighbors
        'right': (0, 1),  # Increase probability for right neighbors
        'up': (-1, 0),  # Increase probability for upper neighbors
        'down': (1, 0)  # Increase probability for lower neighbors
    }

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            if matrix[r, c] == 2:
                is_fire = True
                if wind_direction in ('left', 'right'):
                    _, wind_dc = wind_factor[wind_direction]
                    if dc == wind_dc:
                        is_fire_windside = True
                        break
                elif wind_direction in ('up', 'down'):
                    wind_dr, _ = wind_factor[wind_direction]
                    if dr == wind_dr:
                        is_fire_windside = True
                        break

    return (is_fire, is_fire_windside)


def update_grid(grid, f, p, p_fire_wind_diff_side, wind_direction):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if wind_direction is None:
                if grid[i, j] == 1 and detect_fire(grid, i, j, wind_direction)[0]:
                    new_grid[i, j] = 2

                elif grid[i, j] == 1 and random.random() < f:
                    new_grid[i, j] = 2

                elif grid[i, j] == 0 and random.random() < p:
                    new_grid[i, j] = 1

                elif grid[i, j] == 2:
                    new_grid[i, j] = 0

            else:
                if grid[i, j] == 1:
                    if detect_fire(grid, i, j, wind_direction) == (True, True):
                        new_grid[i, j] = 2

                    elif detect_fire(grid, i, j, wind_direction) == (
                    True, False) and random.random() < p_fire_wind_diff_side:
                        new_grid[i, j] = 2

                    elif random.random() < f:
                        new_grid[i, j] = 2

                elif grid[i, j] == 0 and random.random() < p:
                    new_grid[i, j] = 1

                elif grid[i, j] == 2:
                    new_grid[i, j] = 0

    return new_grid


###########################################################

pygame.init()
pygame.font.init()

wind_right = pygame.image.load('wind/wind_right.png')
wind_left = pygame.image.load('wind/wind_left.png')
wind_up = pygame.image.load('wind/wind_up.png')
wind_down = pygame.image.load('wind/wind_down.png')
wind_no = pygame.image.load('./wind/wind_no.png')

font_big1 = pygame.font.SysFont('comicsansms', 55)
font_big2 = pygame.font.SysFont('comicsansms', 55)
font_small = pygame.font.SysFont('comicsansms', 35)
pause_text_w = font_big1.render('Click SPACEBAR to START', True, (255, 255, 255))
pause_text_b = font_big2.render('Click SPACEBAR to START', True, (255, 0, 0))
restart_text_w = font_big1.render('Click ENTER to RESTART', True, (255, 255, 255))
restart_text_b = font_big2.render('Click ENTER to RESTART', True, (255, 0, 0))
wind_text_w = font_small.render('Click ARROWS & DOT to change wind', True, (255, 255, 255))
wind_text_b = font_small.render('Click ARROWS & DOT to change wind', True, (255, 0, 0))

state_counts = {
    'empty': [],
    'tree': [],
    'burning': []
}

running = True
display_text = True
simulation_running = False
last_update_time = time.time()

FPS = 24.00
cell_size = 4
res = (800, 800)

screen = pygame.display.set_mode(res)
pygame.display.set_caption('Forest Fire Model')

# Setup
PLOT = False
TREE_PROPORTION = 0.3
GROW_TREE_PROB = 0.2
FIRE_PROB = 0.0001
FIRE_PROB_WIND_DIFF_SIDE = 0.1
WIND_DIRECTION = 'right'

if WIND_DIRECTION is None:
    current_image = wind_no
elif WIND_DIRECTION == 'left':
    current_image = wind_right
elif WIND_DIRECTION == 'right':
    current_image = wind_left
elif WIND_DIRECTION == 'down':
    current_image = wind_up
elif WIND_DIRECTION == 'up':
    current_image = wind_down

grid = generate_random_grid(int(res[0] / cell_size), TREE_PROPORTION)

while running:
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulation_running = not simulation_running
                display_text = not display_text
            elif event.key == pygame.K_RETURN:
                grid = generate_random_grid(int(res[0] / cell_size), TREE_PROPORTION)
            elif event.key == pygame.K_RIGHT:
                current_image = wind_right
                WIND_DIRECTION = 'left'
            elif event.key == pygame.K_LEFT:
                current_image = wind_left
                WIND_DIRECTION = 'right'
            elif event.key == pygame.K_UP:
                current_image = wind_up
                WIND_DIRECTION = 'down'
            elif event.key == pygame.K_DOWN:
                current_image = wind_down
                WIND_DIRECTION = 'up'
            elif event.key == pygame.K_PERIOD:
                current_image = wind_no
                WIND_DIRECTION = None

    if not running:
        break

    # Update grid
    if simulation_running and (time.time() - last_update_time > 1 / FPS):
        grid = update_grid(grid, FIRE_PROB, GROW_TREE_PROB, FIRE_PROB_WIND_DIFF_SIDE, WIND_DIRECTION)
        last_update_time = time.time()

        # Count states
        unique, counts = np.unique(grid, return_counts=True)
        count_dict = dict(zip(unique, counts))
        state_counts['empty'].append(count_dict.get(0, 0))
        state_counts['tree'].append(count_dict.get(1, 0))
        state_counts['burning'].append(count_dict.get(2, 0))

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

    # Display text when paused
    if display_text:
        screen.blit(pause_text_b, (47, 340))
        screen.blit(pause_text_w, (49, 342))
        screen.blit(restart_text_b, (55, 400))
        screen.blit(restart_text_w, (57, 402))
        screen.blit(wind_text_b, (70, 468))
        screen.blit(wind_text_w, (72, 470))

    # Display wind images
    if current_image:
        screen.blit(current_image, (0, 0))

    pygame.display.update()

# Plots
if PLOT:
    time_steps = range(len(state_counts['empty']))

    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, state_counts['empty'], label='Empty', color='black')
    plt.plot(time_steps, state_counts['tree'], label='Tree', color='green')
    plt.plot(time_steps, state_counts['burning'], label='Burning', color='red')
    plt.xlabel('Time step')
    plt.ylabel('Count')
    plt.title('Forest Fire Model: Cell State Counts Over Time')
    plt.legend()
    plt.show()
