import gzip
from urllib import request

from sklearn.decomposition import PCA
import numpy as np

filename = [
    ["training_images", "train-images-idx3-ubyte.gz"],
    ["test_images", "t10k-images-idx3-ubyte.gz"],
    ["training_labels", "train-labels-idx1-ubyte.gz"],
    ["test_labels", "t10k-labels-idx1-ubyte.gz"]
]


def download_mnist():
    base_url = "http://yann.lecun.com/exdb/mnist/"
    for name in filename:
        print("Downloading " + name[1] + "...")
        request.urlretrieve(base_url + name[1], name[1])
    print("Download complete.")


def to_bit_vector(x, threshold):
    if x >= threshold:
        return 1
    else:
        return 0


def save_mnist():
    mnist = {}
    for name in filename[:2]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(
                f.read(), np.uint8, offset=16).reshape(-1, 28 * 28)
    for name in filename[-2:]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)
    # Initialize and fit PCA
    # pca = PCA(n_components=25)
    # mnist['training_images'] = pca.fit_transform(mnist['training_images'])
    # mnist['test_images'] = pca.fit_transform(mnist['test_images'])
    # Training images to bit vector. Threshold: 200
    vfunc = np.vectorize(to_bit_vector)
    training_bit_vector = vfunc(mnist['training_images'], 200)
    # Save
    np.save('training_bit_vector', training_bit_vector)
    # Save to txt files.
    # np.savetxt('train_images.txt', mnist['training_images'].astype(
    #     int), fmt='%i', delimiter=",")
    # np.savetxt('train_labels.txt', mnist['training_labels'].astype(
    #     int), fmt='%i', delimiter=",")
    # np.savetxt('test_images.txt', mnist['test_images'].astype(
    #     int), fmt='%i', delimiter=",")
    # np.savetxt('test_labels.txt', mnist['test_labels'].astype(
    #     int), fmt='%i', delimiter=",")
    print("Save complete.")


if __name__ == '__main__':
    download_mnist()
    # save_mnist()
