import numpy as np
import matplotlib.pyplot as plt

class PerlinNoiseGenerator:
    """
    A Perlin noise generator to create 2D Perlin noise.

    Methods:
        generate_noise(width, height):
            Static method to generate random gradients and permutation table.
            
        smoothstep(t):
            Static method that applies a smoothstep function to the input value t.

        interpolate(x, y, t):
            Static method that performs linear interpolation between two values x and y using t.

        perlin_noise(width, height, zoom, octaves):
            Generates 2D Perlin noise using the given parameters.
    """
    
    @staticmethod
    def generate_noise(width, height):
        """
        Generates random gradients and a permutation table for Perlin noise.

        Parameters:
            width (int): The width of the generated noise grid.
            height (int): The height of the generated noise grid.

        Returns:
            tuple: A tuple containing the generated gradients and permutation table.
                gradients (numpy.ndarray): 3D array representing random gradients for each point.
                permutation (numpy.ndarray): 2D array representing a permutation table.
        """
        gradients = np.random.randn(width, height, 2)
        permutation = np.arange(width * height)
        np.random.shuffle(permutation)
        permutation = np.resize(permutation, (width, height))
        return gradients, permutation

    @staticmethod
    def smoothstep(t):
        """
        Applies a smoothstep function to the input value t.

        Parameters:
            t (float): The input value.

        Returns:
            float: The result of the smoothstep function applied to t.
        """
        return t * t * (3 - 2 * t)

    @staticmethod
    def interpolate(x, y, t):
        """
        Performs linear interpolation between two values x and y using t.

        Parameters:
            x (float): The first value for interpolation.
            y (float): The second value for interpolation.
            t (float): The interpolation parameter, usually in the range [0, 1].

        Returns:
            float: The interpolated value between x and y based on t.
        """
        ft = PerlinNoiseGenerator.smoothstep(t)
        return x + ft * (y - x)

    @staticmethod
    def perlin_noise(width, height, zoom, octaves):
        """
        Generates 2D Perlin noise using the given parameters.

        Parameters:
            width (int): The width of the generated noise grid.
            height (int): The height of the generated noise grid.
            zoom (float): The zoom factor for the noise generation.
            octaves (int): The number of octaves used to create the noise.

        Returns:
            numpy.ndarray: The 2D array representing the generated Perlin noise.
        """
        gradients, permutation = PerlinNoiseGenerator.generate_noise(width, height)
        noise = np.zeros((width, height))

        for i in range(width):
            for j in range(height):
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

                    blend_x = PerlinNoiseGenerator.interpolate(dot00, dot10, xf)
                    blend_y = PerlinNoiseGenerator.interpolate(dot01, dot11, xf)
                    noise_value += PerlinNoiseGenerator.interpolate(blend_x, blend_y, yf) * amplitude

                    amplitude *= 0.5
                    frequency *= 2.0

                noise[i, j] = (noise_value + 1) / 2

        return noise

class PerlinNoise3DVisualizer:
    """
    A 3D Perlin noise visualizer using Matplotlib.

    Attributes:
        width (int): The width of the 3D noise grid.
        height (int): The height of the 3D noise grid.
        zlevel (int): The number of z-levels in the 3D noise.
        voxelarray (numpy.ndarray): The 3D array representing the voxelized 3D Perlin noise.
    """

    def __init__(self, width, height, zlevel, zoom, octaves):
        """
        Initialize the 3D Perlin noise visualizer.

        Parameters:
            width (int): The width of the 3D noise grid.
            height (int): The height of the 3D noise grid.
            zlevel (int): The number of z-levels in the 3D noise.
            zoom (float): The zoom factor for the noise generation.
            octaves (int): The number of octaves used to create the noise.
        """
        self.width = width
        self.height = height
        self.zlevel = zlevel
        self.zoom = zoom
        self.octaves = octaves
        self.voxelarray = self.generate_voxel_array()

    def generate_voxel_array(self):
        """
        Generate the 3D voxel array using Perlin noise.

        Returns:
            numpy.ndarray: The 3D array representing the voxelized 3D Perlin noise.
        """
        noise_2d = np.round(PerlinNoiseGenerator.perlin_noise(self.width, self.height, self.zoom, self.octaves),
                            decimals=2)

        threed = np.zeros((self.width, self.height, self.zlevel))

        for i in range(self.width):
            for j in range(self.height):
                for z in range(self.zlevel):
                    if z < int(noise_2d[i, j] * self.zlevel - 1):
                        threed[i, j, z] = 1
                    else:
                        threed[i, j, z] = 0
        

        return threed

    def plot_3d_voxel(self):
        """
        Plot the 3D voxel visualization using Matplotlib.
        """
        voxelarray = self.voxelarray
        colors = np.empty(voxelarray.shape, dtype=object)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(voxelarray, facecolors="white", edgecolor='k')

        plt.show()

def main(width, height, zlevel, zoom, octaves):
    # Zoom adjusts the zoom for the desired level of detail
    # Octaves adjusts the number of octaves for increased detail

    visualizer = PerlinNoise3DVisualizer(width, height, zlevel, zoom, octaves)
    visualizer.plot_3d_voxel()

if __name__ == "__main__":
    width = 50
    height = 50
    zlevel = 50
    zoom = 18
    octaves = 3
    main( width, height, zlevel, zoom, octaves)
