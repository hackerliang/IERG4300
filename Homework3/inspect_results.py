import numpy as np

last_iter = 10

with open('centroids/centroids_{}.txt'.format(last_iter), 'r') as f:
    centroids = {}
    for line in f.readlines():
        idx, centroids_str = line.strip().split('\t')
        centroids[int(idx)] = [np.asarray(centroids_str.strip()[1:-1].split(', '), dtype=float), 0]

with open('train_images.txt', 'r') as f:
    data = []
    for line in f:
        data += [np.asarray(line.strip().split(','), dtype=float)]

# Compute and assign items.
# For each data point, calculate the distance between all centroids.
for item in data:
    distances = {}
    for idx, centroid_count in centroids.items():
        # Calculate L2 Norm.
        distances[idx] = np.linalg.norm(centroid_count[0] - item)
    # Get the index of the cluster with minimum distance.
    cluster_id = min(distances, key=distances.get)
    # Add to count.
    centroids[cluster_id][1] += 1

# Output.
with open('result.txt', 'w') as f:
    for key, value in centroids.items():
        # Keep 2 decimal places for the report.
        f.write('{}\t{}|{}\n'.format(key, np.around(value[0], 2).tolist(), value[1]))
