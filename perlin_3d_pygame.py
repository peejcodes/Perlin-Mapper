import numpy as np
import matplotlib.pyplot as plt

def generate_noise(width, height):
    # Generate random gradient vectors
    gradients = np.random.randn(width, height, 2)

    # Generate random permutation of indices
    permutation = np.arange(width*height)
    np.random.shuffle(permutation)

    # Reshape permutation to match the size of the noise grid
    permutation = np.resize(permutation, (width, height))

    return gradients, permutation

def smoothstep(t):
    return t * t * (3 - 2 * t)

def interpolate(x, y, t):
    ft = smoothstep(t)
    return x + ft * (y - x)

def perlin_noise(width, height, zoom, octaves):
    gradients, permutation = generate_noise(width, height)

    # Generate empty noise grid
    noise = np.zeros((width, height))

    for i in range(width):
        for j in range(height):
            amplitude = 1.0
            frequency = 1.0
            noise_value = 0.0

            for _ in range(octaves):
                # Determine the grid cell coordinates
                x0, y0 = int(i / frequency / zoom), int(j / frequency / zoom)
                x1, y1 = x0 + 1, y0 + 1

                # Determine the position within the grid cell
                xf, yf = i / frequency / zoom - x0, j / frequency / zoom - y0

                # Calculate dot products between gradients and position vectors
                dot00 = np.dot(gradients[x0, y0], [xf, yf])
                dot01 = np.dot(gradients[x0, y1], [xf, yf - 1])
                dot10 = np.dot(gradients[x1, y0], [xf - 1, yf])
                dot11 = np.dot(gradients[x1, y1], [xf - 1, yf - 1])

                # Interpolate dot products along x-axis
                blend_x = interpolate(dot00, dot10, xf)

                # Interpolate dot products along y-axis
                blend_y = interpolate(dot01, dot11, xf)

                # Interpolate final value along z-axis and add to noise value
                noise_value += interpolate(blend_x, blend_y, yf) * amplitude

                # Update amplitude and frequency for the next octave
                amplitude *= 0.5
                frequency *= 2.0

            # Store the final noise value in the grid and normalize to (0, 1) range
            noise[i, j] = (noise_value + 1) / 2

    return noise

# Generate Perlin noise maps
width, height, zlevel= 50,50,40
zoom = 20  # Adjust the zoom for the desired level of detail
octaves = 4  # Adjust the number of octaves for increased detail

world1 = np.round(perlin_noise(width, height, zoom, octaves), decimals=2)
world2 = np.round(perlin_noise(width, height, zoom * 2, octaves), decimals=2)


import sys
np.set_printoptions(threshold=sys.maxsize)


threed = np.zeros((width,height,zlevel))
#print(threed)
for i in range(width):
    for j in range(height):
        for z in range(zlevel):
            if z < int(world1[i,j]*zlevel-1):
           # z = int(world1[i,j]*19)
                threed[i,j,z] = 1
            else:
                threed[i,j,z] = 0
#print(threed)





#pygame

import numpy as np
import pygame
import sys

# Replace the following line with your actual 3D numpy array


# Constants for the Pygame window
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 2800
CELL_SIZE = 30
FPS = 60

# Constants for navigation
MIN_Z_LEVEL = 0
MAX_Z_LEVEL = threed.shape[2] - 1

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Function to draw the 3D numpy array at the current z-level
def draw_array_at_z_level(z_level):
    window.fill((255, 255, 255))  # Clear the screen
    for y in range(threed.shape[0]):
        for x in range(threed.shape[1]):
            if threed[y, x, z_level] == 1:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, (0, 0, 0), rect)
    pygame.display.flip()

# Initial z-level
current_z_level = 0
draw_array_at_z_level(current_z_level)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_z_level = min(current_z_level + 1, MAX_Z_LEVEL)
            elif event.key == pygame.K_DOWN:
                current_z_level = max(current_z_level - 1, MIN_Z_LEVEL)
            draw_array_at_z_level(current_z_level)

    clock.tick(FPS)
