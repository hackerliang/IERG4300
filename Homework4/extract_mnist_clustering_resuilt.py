import gzip

import numpy as np

with open('centroids_20.txt', 'r') as f:
    centroids = {}
    for line in f.readlines():
        cluster_idx, centroids_str = line.strip().split('\t')
        centroids[int(cluster_idx)] = [np.asarray(centroids_str.strip()
                                                  [1:-1].split(', '), dtype=float), 0]

# Load MNIST training set & labels.
filename = [
    ["training_images", "train-images-idx3-ubyte.gz"],
    ["test_images", "t10k-images-idx3-ubyte.gz"],
    ["training_labels", "train-labels-idx1-ubyte.gz"],
    ["test_labels", "t10k-labels-idx1-ubyte.gz"]
]
mnist = {}
for name in filename[:2]:
    with gzip.open(name[1], 'rb') as f:
        mnist[name[0]] = np.frombuffer(
            f.read(), np.uint8, offset=16).reshape(-1, 28 * 28)
for name in filename[-2:]:
    with gzip.open(name[1], 'rb') as f:
        mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)

# Concatenate images and labels.
mnist['training_images'] = mnist['training_images'].reshape((60000, 784))
mnist['training_labels'] = mnist['training_labels'].reshape((60000, 1))
train_image_label = np.concatenate((mnist['training_images'], mnist['training_labels']), axis=1)

# Compute and assign items.
# For each data point, calculate the distance between all centroids.
assignments = np.zeros((60000, 1))
for i in range(len(train_image_label)):
    distances = {}
    for cluster_idx, centroid_count in centroids.items():
        # Calculate L2 Norm.
        distances[cluster_idx] = np.linalg.norm(centroid_count[0] - train_image_label[i][:-1])
    # Get the index of the cluster with minimum distance.
    cluster_id = min(distances, key=distances.get)
    assignments[i] = cluster_id
    # Add to count.
    centroids[cluster_id][1] += 1

# Concatenate cluster ids with image and label.
train_image_label_cluster = np.concatenate((train_image_label, assignments), axis=1)

# Select and save arrays for every clusters.
for i in range(10):
    cluster_image_label = train_image_label_cluster[train_image_label_cluster[:, 785] == i]
    np.save('cluster{}_image_label'.format(i), cluster_image_label)