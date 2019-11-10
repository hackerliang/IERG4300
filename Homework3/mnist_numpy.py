import gzip
from urllib import request

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


def save_mnist():
    mnist = {}
    for name in filename[:2]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(
                f.read(), np.uint8, offset=16).reshape(-1, 28 * 28)
    for name in filename[-2:]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)
    # Save to txt files.
    np.savetxt('train_images.txt', mnist['training_images'].astype(
        int), fmt='%i', delimiter=",")
    np.savetxt('train_labels.txt', mnist['training_labels'].astype(
        int), fmt='%i', delimiter=",")
    np.savetxt('test_images.txt', mnist['test_images'].astype(
        int), fmt='%i', delimiter=",")
    np.savetxt('test_labels.txt', mnist['test_labels'].astype(
        int), fmt='%i', delimiter=",")
    print("Save complete.")


if __name__ == '__main__':
    download_mnist()
    save_mnist()
