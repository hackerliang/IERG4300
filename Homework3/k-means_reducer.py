#!/usr/bin/python3

import fileinput

import numpy as np

lines = fileinput.input()

clusters = {}

for line in lines:
    cluster_id, partial_sum_count = line.strip().split('\t')
    partial_sum, count = partial_sum_count.split('|')
    partial_sum = np.asarray(partial_sum[1:-1].split(','), dtype=float)
    count = int(count)
    cluster_id = int(cluster_id)
    # Assign partial sums and counts.
    if cluster_id not in clusters:
        clusters[cluster_id] = [partial_sum, count]
    else:
        clusters[cluster_id] = [np.add(partial_sum, clusters[cluster_id][0]), clusters[cluster_id] + count]

# Calculate new centroids.
for key, value in clusters.items():
    # Numpy 1.7+: return 0 when divided by zero.
    clusters[key] = np.true_divide(value[0], value[1], out=np.zeros_like(value[0]), where=value[1]!=0)

# Print
for key, value in clusters.items():
    print('{}\t{}'.format(key, str(value.tolist())[1:-1]))
