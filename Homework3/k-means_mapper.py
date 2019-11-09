#!/usr/bin/python3

import fileinput
import os

import numpy as np

# Read a file for the centroids.
# One line one centroid. Each centroid is constructed by 784 dimension vector.
# Items are split by commas.
with open('centroids_{}.txt'.format(int(os.environ.get('ITER_NUM')) - 1), 'r') as f:
    centroids = {}
    for line in f.readlines():
        idx, centroids_str = line.strip().split('\t')
        centroids[int(idx)] = np.asarray(centroids_str.strip()[1:-1].split(', '), dtype=float)

# Read the input from STDIN.
# Design: each line is a 784 dimension vector, use comma to split items.
lines = fileinput.input()

data = []
for line in lines:
    data += [np.asarray(line.strip().split(','), dtype=float)]

# Partial sums.
partial_sums_counts = {}
for i in range(10):
    partial_sums_counts.setdefault(i, [np.zeros((1, 784), dtype=float), 0])

# Compute and assign items.
# For each data point, calculate the distance between all centroids.
for item in data:
    distances = {}
    for idx, centroid in centroids.items():
        # Calculate L2 Norm.
        distances[idx] = np.linalg.norm(centroid - item)
    # Get the index of the cluster with minimum distance.
    cluster_id = min(distances, key=distances.get)
    # Add to partial sum.
    partial_sums_counts[cluster_id][0] = np.add(partial_sums_counts[cluster_id][0], item)
    # Add count.
    partial_sums_counts[cluster_id][1] += 1

# Output
for key, item in partial_sums_counts.items():
    # Centroid ID \t partial sum vector | item count
    print('{}\t{}|{}'.format(key, str(item[0].tolist())[1:-1], item[1]))
