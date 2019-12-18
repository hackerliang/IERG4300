import os
from pathlib import Path

import numpy as np


def to_bit_vector(x, threshold):
    if x >= threshold:
        return 1
    else:
        return 0


def minhash(file_name, k):
    # Read in input data.
    vec = np.load(file_name)
    # Initialize signature matrix.
    sig = np.empty((vec.shape[0], k))
    sig.fill(maxint)
    masks = (np.random.RandomState(seed=10).randint(minint, maxint, k))
    hashes = np.empty(k, dtype=np.int64)
    hashes.fill(maxint)
    # Iterate by row.
    for i in range(vec.shape[0]):
        hashes = np.empty(k, dtype=np.int64)
        hashes.fill(maxint)
        for j in range(784):
            current_hash = np.bitwise_xor(masks, hash(vec[i][j]))
            hashes = np.minimum(current_hash, hashes)
        sig[i][:] = hashes

    # Save the signature matrix.
    np.save('{}_minhash_sig'.format(os.path.basename(file_name)[:-4]), sig)


if __name__ == '__main__':
    # Generate hash functions.
    minint = np.iinfo(np.int32).min
    maxint = np.iinfo(np.int32).max
    file_list = Path('cluster_image_label').glob('*.npy')
    for file in file_list:
        minhash(file, 64)
