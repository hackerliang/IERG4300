import random
import os
from pathlib import Path

import numpy as np


def lsh(m_sig, k, r, b):
    t = (1 / b) ** (1 / r)
    print('Begin LSH with r={}, b={}, t={}'.format(r, b, t))
    # Final hash table: shape b * k
    lsh_table = {}
    randint1 = random.randint(1, 10000)
    randint2 = random.randint(1, 10000)
    # A matrix stores bucket IDs for all bands.
    bucket_band = np.zeros((len(m_sig), b))
    # Iterate by rows. Each row is one image.
    for s in range(len(m_sig)):
        sig = m_sig[s]
        for i, band in enumerate(range(b)):
            value = hash(tuple(sig[i * r:i * r + r]))
            # Hash value: bucket ID that this band falls to.
            hash_value = ((randint1 * value + randint2) % 9887) % k
            bucket_band[s][i] = hash_value
            # Add to hash table.
            if hash_value in lsh_table:
                lsh_table[hash_value] += [[s, i]]
            else:
                lsh_table[hash_value] = [[s, i]]
    return bucket_band, lsh_table


if __name__ == '__main__':
    # List all files.
    sig_list = Path('cluster_image_minhash_sig').glob('*.npy')
    for sig_matrix_path in sig_list:
        # Read signature matrix.
        sig_matrix = np.load(sig_matrix_path)
        # Perform LSH.
        bucket_band, lsh_table = lsh(sig_matrix, 10, 8, 8)
        # Save bucket band.
        np.save('{}_bucket_band'.format(os.path.basename(sig_matrix_path)[:8]), bucket_band)
