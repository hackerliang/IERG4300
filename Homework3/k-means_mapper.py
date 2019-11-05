#!/usr/bin/python3

import fileinput

import numpy as np

# Read a file for the centroids.
# One line one centroid. Each centroid is constructed by 784 dimension vector.
# Items are split by commas.
with open('centroids.txt', 'r') as f:
    centroids = {}
    idx = 0
    for line in f.readlines():
        centroids[idx] = np.asarray(line.strip().split(','))
        idx += 1

# Read the input from STDIN.
# Design: each line is a 784 dimension vector, use comma to split items.
lines = fileinput.input()

data = []
for line in lines:
    data += [np.asarray(line.strip().split(','))]

# Partial sums.
partial_sums_counts = {}
for i in range(10):
    partial_sums_counts.setdefault(i, [np.zeros((784, 1)), 0])

# Compute and assign items.
# For each data point, calculate the distance between all centroids.
for item in data:
    distances = {}
    for idx, centroid in centroids.items():
        # Calculate L2 Norm.
        distances[idx] = np.linalg.norm(item - centroid)
    # Get the index of the cluster with minimum distance.
    cluster_id = min(distances, key=distances.get)
    # Add to partial sum.
    partial_sums_counts[cluster_id][0] = np.add(partial_sums_counts[cluster_id], item)
    # Add count.
    partial_sums_counts[cluster_id][1] += 1

# Output
for key, item in partial_sums_counts.items():
    # Centroid ID \t partial sum vector | item count
    print('{}\t{}|{}'.format(key, str(item[0].tolist())[1:-1], item[1]))