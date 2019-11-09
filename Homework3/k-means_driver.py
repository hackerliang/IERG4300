import os

import numpy as np


def generate_random_centroids():
    # Generate random centroids.
    random_centroids = np.random.randint(0, 255, size=(10, 784), dtype=int)
    # Save to txt
    np.savetxt('centroids.txt', random_centroids.astype(int), fmt='%i', delimiter=',')


def run_mapper():
    COMMAND = """
    hadoop jar 
    """
    pass


def run_reducer():
    pass


def iteration(num_iterations):
    pass


if __name__ == '__main__':
    generate_random_centroids()
