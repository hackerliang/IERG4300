import numpy as np


def compare_row(arr):
    # Add sum a boolean array can get the number of true values.
    if np.sum(arr) >= 2:
        return np.array(True)
    else:
        return np.array(False)


def find_similar_items(cluster_id, major_label):
    # Load original cluster images.
    cluster_image_label = np.load('cluster_image_label\\cluster{}_image_label.npy'.format(cluster_id))
    # Load LSH buckets.
    cluster_lsh_buckets = np.load('cluster_bucket_band\\cluster{}_bucket_band.npy'.format(cluster_id))

    # Find indices of images with the major label. Ground truth labels in column 784.
    indices_major_label = np.where(cluster_image_label[:, 784] == major_label)[0]
    # Randomly select a representative.
    random_index = indices_major_label[np.random.randint(0, indices_major_label.shape[0])]
    # Extract the bucket info for the representative image.
    representative_bucket_band = cluster_lsh_buckets[random_index]

    # Find images that have at least 2 bands hashed to same buckets.
    similar_matrix = np.apply_along_axis(np.isin, 0, cluster_lsh_buckets, representative_bucket_band)
    similar_items = []
    for idx, row in enumerate(similar_matrix):
        # Sum up a boolean array can get the number of Trues.
        if np.sum(row) >= 2:
            similar_items.append(cluster_image_label[idx])
        else:
            continue
    similar_items = np.array(similar_items)

    # See the labels of these similar items.
    similar_items_labels = similar_items[:, 784]
    unique_labels, counts = np.unique(similar_items_labels, return_counts=True)
    label_counts = dict(zip(unique_labels, counts))

    # Returns: # of similar items, # of similar items with same label, accuracy.
    return len(similar_items), label_counts[major_label], label_counts[major_label] / len(similar_items)


if __name__ == '__main__':
    number_similar_items, number_same_label, acc = find_similar_items(0, 6)
    print(number_similar_items, number_same_label, acc)
