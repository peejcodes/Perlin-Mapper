import random
import pygame
from perlin_noise import PerlinNoise
import time
import pickle
import csv
import math

class BiomeMap:
    def __init__(self, xpix, ypix):
        self.xpix = xpix
        self.ypix = ypix
        self.tile_size = 2
        self.window_width = xpix * self.tile_size * 2
        self.window_height = ypix * self.tile_size * 2
        self.half_width = self.window_width / 2
        self.half_height = self.window_height / 2
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.pic = None

    def assign_biome(self, value):
        if value < -0.35:
            return (28, 114, 114)  # Dark Blue for deep ocean
        elif value < -0.1:
            return (69, 229, 229)  # Blue for ocean
        elif -0.2 < value < -0.05:
            return (240, 228, 192)  # sand for beach
        elif value < .1:
            return (194, 178, 128)  # darker sand
        elif value < .3:
            return (18, 200, 68)  # Green for plains
        elif value < 0.5:
            return (34, 139, 34)  # Forest green for forest
        elif value < 0.7:
            return (139, 137, 137)  # Gray for mountains
        else:
            return (255, 255, 255)  # White for snowy peaks
            
            
            
            
#    def assign_biome2(self, value):
#        if value < .2:
#            return (28, 114, 114)  # Dark Blue for deep ocean
#        elif value < 0.6:
#            return (34, 139, 34)  # Forest green for forest
#        else:
#            return (255, 255, 255)  # White for snowy peaks

    def create_noise(self):
        noise1 = PerlinNoise(octaves=8, seed=random.randint(0, 9))
        noise2 = PerlinNoise(octaves=1, seed=random.randint(0, 9))
        noise3 = PerlinNoise(octaves=1, seed=random.randint(0, 9))
        noise4 = PerlinNoise(octaves=1, seed=random.randint(0, 9))
        pic = []
        for i in range(self.xpix):
            row = []
            for j in range(self.ypix):
                noise_val = noise1([i / self.xpix, j / self.ypix])
                noise_val += random.uniform(0, 3) * noise2([i / self.xpix, j / self.ypix])
                noise_val += random.uniform(0, 0.5) * noise3([i / self.xpix, j / self.ypix])
                noise_val += random.uniform(0, 0.1) * noise4([i / self.xpix, j / self.ypix])
                row.append(noise_val)
            pic.append(row)
        return pic

    def show_noise(self, x, y):
        for i in range(self.ypix):
            for j in range(self.xpix):
                value = self.pic[i][j]
                color = self.assign_biome(value)
                pygame.draw.rect(self.window, color,
                                 (j * self.tile_size + (x * self.half_width), i * self.tile_size + (y * self.half_height),
                                  self.tile_size, self.tile_size))

    def get_surrounding_tiles(self, x, y):
        surrounding_tiles = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue  # Skip the center tile (self)
                surrounding_tiles.append((i, j))
        return surrounding_tiles

    def fix_surrounding_tiles_edges(self):
        # x axis
        for i in range(0, self.xpix - 1):
            self.pic[0][i] = self.pic[1][i]
            self.pic[self.xpix - 1][i] = self.pic[self.xpix - 2][i]

        for i in range(0, self.ypix):
            self.pic[i][0] = self.pic[i][1]
            self.pic[i][self.ypix - 1] = self.pic[i][self.ypix - 2]

    def average_tiles(self):
        for i in range(1, self.xpix - 1):
            for j in range(1, self.ypix - 1):
                total = 0
                surrounding = self.get_surrounding_tiles(i, j)
                for index, tile in enumerate(surrounding):
                    total += self.pic[tile[0]][tile[1]]
                average = total / (index + 1)
                self.pic[i][j] = round(average,2)
        self.fix_surrounding_tiles_edges()

    def reset_map(self):
        self.pic = self.create_noise()
        self.average_tiles()
        self.average_tiles()
        self.average_tiles()

    def run(self):
        pygame.init()
        self.reset_map()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.show_noise(0, 0)
            self.save_pickle_noise(self.pic)
            self.load_pickle_noise(self.pic)
            pygame.display.flip()
            self.clock.tick(60)
            time.sleep(1)
            running= False
            
    def save_pickle_noise(self,noise):
        
        # Save the data to a pickle file
        with open('noise_data.pickle', 'wb') as picklefile:
            pickle.dump(noise, picklefile)
            
    def load_pickle_noise(self,noise):
        # Load the pickle file
        with open('noise_data.pickle', 'rb') as picklefile:
            data = pickle.load(picklefile)
        
        # Print the loaded data
        print(data)

   
            
            
            

# Usage
biome_map = BiomeMap(200,200)
biome_map.run()
