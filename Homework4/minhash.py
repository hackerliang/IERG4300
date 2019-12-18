import os
from pathlib import Path

import numpy as np


def row_hash(x, randint1, randint2, prime, m):
    return ((randint1 * x + randint2) % prime) % m


def to_bit_vector(x, threshold):
    if x >= threshold:
        return 1
    else:
        return 0


def minhash(file_name, k):
    # Initialize signature matrix.
    sig = np.empty((k, 784))
    sig.fill(maxint)

    # Read in input data.
    vec = np.load(file_name)
    # Transfer to bit vector.
    vfunc = np.vectorize(to_bit_vector)
    vec = vfunc(vec, 200)
    # Iterate by row.
    for i in range(vec.shape[0]):
        # Calculate hash values for this row.
        hash_values = []
        for k in range(k):
            hash_values += [row_hash(i, randint1[k], randint2[k], prime, 784)]
        # Find 1
        for j in range(784):
            # Column j is 1
            if vec[i][j] == 1:
                # Pass all rows in signature matrix in column j.
                for k in range(k):
                    if hash_values[k] < sig[k][j]:
                        sig[k][j] = hash_values[k]
                    else:
                        continue
            else:
                continue

    # Save the signature matrix.
    np.save('{}_minhash_sig'.format(os.path.basename(file_name)[:-4]), sig)


if __name__ == '__main__':
    # Generate hash functions.
    seed1 = 10
    seed2 = 2
    minint = np.iinfo(np.int32).min
    maxint = np.iinfo(np.int32).max
    k = 64
    randint1 = np.random.RandomState(seed=seed1).randint(0, 10000, k)
    randint2 = np.random.RandomState(seed=seed2).randint(0, 10000, k)
    prime = 787
    file_list = Path('cluster_image_label').glob('*.npy')
    for file in file_list:
        minhash(file, 64)
