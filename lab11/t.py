import numpy as np


# def get_neighborhood(matrix, row, col, wind_direction=None):
#     rows, cols = matrix.shape
#     neighborhood = []
#     is_fire = False
#     is_fire_windside = False
#
#     directions = ((-1, -1), (-1, 0), (-1, 1),
#                   (0, -1), (0, 1),
#                   (1, -1), (1, 0), (1, 1))
#
#     wind_factor = {
#         'left': (0, -1),  # Increase probability for left neighbors
#         'right': (0, 1),  # Increase probability for right neighbors
#         'up': (-1, 0),  # Increase probability for upper neighbors
#         'down': (1, 0)  # Increase probability for lower neighbors
#     }
#
#     for dr, dc in directions:
#         r, c = row + dr, col + dc
#         if 0 <= r < rows and 0 <= c < cols:
#             prob_modifier = 0
#             if matrix[r, c] == 2:
#                 if wind_direction in ('left', 'right'):
#                     _, wind_dc = wind_factor[wind_direction]
#                     if dc == wind_dc:
#                         prob_modifier = 1
#                 elif wind_direction in ('up', 'down'):
#                     wind_dr, _ = wind_factor[wind_direction]
#                     if dr == wind_dr:
#                         prob_modifier = 1
#
#             neighborhood.append((matrix[r, c], prob_modifier))
#
#     return tuple(elem[0] for elem in neighborhood), tuple(elem[1] for elem in neighborhood)

def get_neighborhood_wind(matrix, row, col, wind_direction=None):
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


m = np.array([
    [2, 1, 1],
    [2, 1, 1],
    [1, 0, 1]
])

print(get_neighborhood_wind(m, 1, 1, 'right'))
#
# import time
#
# start = time.time()
# for _ in range(200 * 200):
#     get_neighborhood_wind(m, 1, 1, 'left')
# stop = time.time()
#
# print(stop - start)
#
# start = time.time()
# for _ in range(200 * 200):
#     get_neighborhood(m, 1, 1)
# stop = time.time()
#
# print(stop - start)
