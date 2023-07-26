import numpy as np
import matplotlib.pyplot as plt
import pygame
import sys

class PerlinNoiseGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @staticmethod
    def generate_noise(width, height):
        gradients = np.random.randn(width, height, 2)
        permutation = np.arange(width*height)
        np.random.shuffle(permutation)
        permutation = np.resize(permutation, (width, height))
        return gradients, permutation

    @staticmethod
    def smoothstep(t):
        return t * t * (3 - 2 * t)

    @staticmethod
    def interpolate(x, y, t):
        ft = PerlinNoiseGenerator.smoothstep(t)
        return x + ft * (y - x)

    def perlin_noise(self, zoom, octaves):
        gradients, permutation = self.generate_noise(self.width, self.height)
        noise = np.zeros((self.width, self.height))

        for i in range(self.width):
            for j in range(self.height):
                amplitude = 1.0
                frequency = 1.0
                noise_value = 0.0

                for _ in range(octaves):
                    x0, y0 = int(i / frequency / zoom), int(j / frequency / zoom)
                    x1, y1 = x0 + 1, y0 + 1
                    xf, yf = i / frequency / zoom - x0, j / frequency / zoom - y0

                    dot00 = np.dot(gradients[x0, y0], [xf, yf])
                    dot01 = np.dot(gradients[x0, y1], [xf, yf - 1])
                    dot10 = np.dot(gradients[x1, y0], [xf - 1, yf])
                    dot11 = np.dot(gradients[x1, y1], [xf - 1, yf - 1])

                    blend_x = self.interpolate(dot00, dot10, xf)
                    blend_y = self.interpolate(dot01, dot11, xf)
                    noise_value += self.interpolate(blend_x, blend_y, yf) * amplitude

                    amplitude *= 0.5
                    frequency *= 2.0

                noise[i, j] = (noise_value + 1) / 2

        return noise


class PerlinNoise3DVisualizer:
    def __init__(self, noise_3d):
        self.noise_3d = noise_3d
        self.width, self.height, self.zlevel = noise_3d.shape
        self.window_width = 1400
        self.window_height = 2800
        self.cell_size = 30
        self.min_z_level = 0
        self.max_z_level = self.zlevel - 1
        self.current_z_level = 0

    def draw_array_at_z_level(self, z_level):
        self.window.fill((255, 255, 255))
        for y in range(self.height):
            for x in range(self.width):
                if self.noise_3d[y, x, z_level] == 1:
                    rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.window, (0, 0, 0), rect)

        # Display current z level
        font = pygame.font.SysFont(None, 50)
        text1 = font.render(f"Use the arrow keys (up/down) to change z levels. Current Z-level: {z_level+1}", True, (0, 0, 0))
        self.window.blit(text1, (10, self.window_height - 1200))

        pygame.display.flip()

    def run_visualizer(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        clock = pygame.time.Clock()
        self.draw_array_at_z_level(self.current_z_level)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_z_level = min(self.current_z_level + 1, self.max_z_level)
                    elif event.key == pygame.K_DOWN:
                        self.current_z_level = max(self.current_z_level - 1, self.min_z_level)
                    self.draw_array_at_z_level(self.current_z_level)

            clock.tick(60)


def main(width, height, zlevel, zoom, octaves):
    
    perlin_gen = PerlinNoiseGenerator(width, height)
    noise_2d = np.round(perlin_gen.perlin_noise(zoom, octaves), decimals=2)

    zlevel = 40
    threed = np.zeros((width, height, zlevel))

    for i in range(width):
        for j in range(height):
            for z in range(zlevel):
                if z < int(noise_2d[i, j] * zlevel - 1):
                    threed[i, j, z] = 1
                else:
                    threed[i, j, z] = 0

    visualizer = PerlinNoise3DVisualizer(threed)
    visualizer.run_visualizer()

if __name__ == "__main__":
    width = 50
    height = 50
    zlevel = 50
    zoom = 18
    octaves = 3
    main( width, height, zlevel, zoom, octaves)