import gzip

import numpy as np
import pandas as pd

from sklearn.decomposition import PCA

last_iter = 20

with open('Random Seed 3/centroids/centroids_{}.txt'.format(last_iter), 'r') as f:
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
# PCA
pca = PCA(n_components=25)
mnist['test_images'] = pca.fit_transform(mnist['test_images'])
mnist['test_images'] = mnist['test_images'].reshape((10000, 25))
mnist['test_labels'] = mnist['test_labels'].reshape((10000, 1))
test_image_label = np.concatenate((mnist['test_images'], mnist['test_labels']), axis=1)

# Compute and assign items.
# For each data point, calculate the distance between all centroids.
assignments = np.zeros((10000, 1))
for i in range(len(test_image_label)):
    distances = {}
    for cluster_idx, centroid_count in centroids.items():
        # Calculate L2 Norm.
        distances[cluster_idx] = np.linalg.norm(centroid_count[0] - test_image_label[i][:-1])
    # Get the index of the cluster with minimum distance.
    cluster_id = min(distances, key=distances.get)
    assignments[i] = cluster_id
    # Add to count.
    centroids[cluster_id][1] += 1

# Concatenate cluster ids with image and label.
test_image_label_cluster = np.concatenate((test_image_label, assignments), axis=1)

# Get the majority labels for clusters.
label_cluster_id = pd.DataFrame(data={
    'ground_truth_label': test_image_label_cluster[:, [25]].flatten(),
    'assigned_cluster': test_image_label_cluster[:, [26]].flatten()
}).astype(int)
label_cluster_count = label_cluster_id.groupby(['assigned_cluster', 'ground_truth_label']).size().to_frame(
    name='label_count').reset_index()
# Find the majority labels of clusters.
majority_label = label_cluster_count.loc[
    label_cluster_count.groupby(['assigned_cluster'])['label_count'].idxmax()]
majority_label = majority_label.set_index('assigned_cluster')
majority_label = majority_label.rename(columns={'ground_truth_label': 'cluster_label'})

print(majority_label)

label_cluster_majority_label = label_cluster_id.join(majority_label, on='assigned_cluster')
label_cluster_majority_label = label_cluster_majority_label.drop(['label_count'], axis=1)


cluster_assignment_result = {}
for i in range(10):
    # No. total, No. correct
    cluster_assignment_result.setdefault(i, [0, 0])
for item in label_cluster_majority_label.iterrows():
    # Get assigned cluster
    assigned_cluster = item[1]['assigned_cluster']
    # Compare ground truth and cluster label.
    if item[1]['ground_truth_label'] == item[1]['cluster_label']:
        cluster_assignment_result[assigned_cluster][1] += 1
        cluster_assignment_result[assigned_cluster][0] += 1
    else:
        cluster_assignment_result[assigned_cluster][1] += 1

print('Cluster\tcorrect, total\t%')
for key, item in cluster_assignment_result.items():
    print('{}\t{},{}\t{}'.format(key, item[0], item[1], item[0] / item[1]))