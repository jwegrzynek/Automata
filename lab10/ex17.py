import pygame
import random
import numpy as np
from scipy.signal import convolve2d
import time

pygame.init()

# Screen resolution
res = (1000, 750)

screen = pygame.display.set_mode(res)

color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

width = screen.get_width()
height = screen.get_height()

# Font settings
smallfont = pygame.font.SysFont('Corbel', 35)

# Button texts
quit_text = smallfont.render('QUIT', True, color)
start_text = smallfont.render('START', True, color)
stop_text = smallfont.render('STOP', True, color)
clear_text = smallfont.render('CLEAR', True, color)
random_text = smallfont.render('RANDOM', True, color)
history_text = smallfont.render('HISTORY', True, color)
minus_text = smallfont.render('-', True, color)
plus_text = smallfont.render('+', True, color)

grid_size = 50
cell_size = 15
grid = np.array([[random.randint(0, 1) for _ in range(grid_size)] for _ in range(grid_size)], dtype=int)
previous_grid = np.zeros_like(grid)

# Game of Life kernel and rule
kernel = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])

game_of_life_rule = lambda n, c: (n == 3) | (np.logical_and(c, n == 2))


def update_grid(grid, rule):
    neighbors = convolve2d(grid, kernel, mode='same', boundary='wrap').astype(int)
    new_grid = np.zeros_like(grid)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            new_grid[i, j] = rule(neighbors[i, j], grid[i, j])
    return new_grid


def generate_random_grid(size):
    return np.array([[random.randint(0, 1) for _ in range(size)] for _ in range(size)], dtype=int)


# Main loop variables
running = True
simulation_running = False
history = True
last_update_time = time.time()
simulation_speed = 1.00

while running:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            running = False

        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            # Check if the click is within the grid area
            if mouse[0] < 750 and mouse[1] < 750:
                # Calculate the row and column of the clicked cell
                col = mouse[0] // cell_size
                row = mouse[1] // cell_size

                grid[row, col] = 1 - grid[row, col]

            # If the mouse is clicked on the "Quit" button, the game is terminated
            elif 800 <= mouse[0] <= 940 and 50 <= mouse[1] <= 90:
                pygame.quit()
                running = False

            # If the mouse is clicked on the "Start" button, start the simulation
            elif 800 <= mouse[0] <= 940 and 150 <= mouse[1] <= 190:
                simulation_running = True

            # If the mouse is clicked on the "Stop" button, stop the simulation
            elif 800 <= mouse[0] <= 940 and 250 <= mouse[1] <= 290:
                simulation_running = False

            # If the mouse is clicked on the "Clear" button, clear the grid
            elif 800 <= mouse[0] <= 940 and 350 <= mouse[1] <= 390:
                grid = np.zeros((grid_size, grid_size), dtype=int)
                previous_grid = np.zeros_like(grid)

            # If the mouse is clicked on the "New Config" button, generate a new random configuration
            elif 800 <= mouse[0] <= 940 and 450 <= mouse[1] <= 490:
                grid = generate_random_grid(grid_size)
                previous_grid = np.zeros_like(grid)

            # If the mouse is clicked on the "History" button, history is switched on of off
            elif 800 <= mouse[0] <= 940 and 550 <= mouse[1] <= 590:
                if history is True:
                    previous_grid = np.zeros_like(grid)
                history = not history

            # If the mouse is clicked on the "-" button, decrease the simulation speed
            elif 800 <= mouse[0] <= 860 and 650 <= mouse[1] <= 690:
                simulation_speed = max(0.25, simulation_speed - 0.25)

            # If the mouse is clicked on the "+" button, increase the simulation speed
            elif 880 <= mouse[0] <= 940 and 650 <= mouse[1] <= 690:
                simulation_speed = simulation_speed + 0.25

    screen.fill((60, 25, 60))

    # Update grid if simulation is running and the appropriate time has passed
    if simulation_running and (time.time() - last_update_time > 1 / simulation_speed):
        if history is True:
            previous_grid = grid.copy()
        grid = update_grid(grid, game_of_life_rule)
        last_update_time = time.time()

    # Draw the grid
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row, col] == 1:
                color = (255, 255, 255)
            elif previous_grid[row, col] == 1:
                color = (50, 50, 50)
            else:
                color = (0, 0, 0)
            pygame.draw.rect(screen, color, pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size))

    mouse = pygame.mouse.get_pos()

    buttons = [(835, 50, "QUIT", quit_text),
               (825, 150, "START", start_text),
               (835, 250, "STOP", stop_text),
               (825, 350, "CLEAR", clear_text),
               (805, 450, "RANDOM", random_text),
               (810, 550, "HISTORY", history_text)]

    for x, y, text, render in buttons:
        if 790 <= mouse[0] <= 960 and y <= mouse[1] <= y + 40:
            pygame.draw.rect(screen, color_light, [790, y, 170, 40])
        else:
            pygame.draw.rect(screen, color_dark, [790, y, 170, 40])
        screen.blit(render, (x, y + 5))

    # Draw speed control buttons and display current speed
    if 790 <= mouse[0] <= 840 and 650 <= mouse[1] <= 690:
        pygame.draw.rect(screen, color_light, [790, 650, 50, 40])
    else:
        pygame.draw.rect(screen, color_dark, [790, 650, 50, 40])
    screen.blit(minus_text, (810, 650))

    if 910 <= mouse[0] <= 960 and 650 <= mouse[1] <= 690:
        pygame.draw.rect(screen, color_light, [910, 650, 50, 40])
    else:
        pygame.draw.rect(screen, color_dark, [910, 650, 50, 40])
    screen.blit(plus_text, (925, 650))

    speed_text = smallfont.render(f"{simulation_speed:.2f}", True, (255, 255, 255))
    screen.blit(speed_text, (845, 650))

    pygame.display.update()
