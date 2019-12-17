import numpy as np

# Generate hash functions.
seed1 = 10
seed2 = 2
minint = np.iinfo(np.int32).min
maxint = np.iinfo(np.int32).max

k = 64
randint1 = np.random.RandomState(seed=seed1).randint(0, 10000, k)
randint2 = np.random.RandomState(seed=seed2).randint(0, 10000, k)
prime = 787


def row_hash(x, randint1, randint2, prime, m):
    return ((randint1 * x + randint2) % prime) % m


# Initialize signature matrix.
sig = np.empty((k, 784))
sig.fill(maxint)

# Read in input data.
mnist_train_bit_vec = np.load('training_bit_vector.npy')
# Iterate by row.
for i in range(mnist_train_bit_vec.shape[0]):
    # Calculate hash values for this row.
    hash_values = []
    for k in range(k):
        hash_values += [row_hash(i, randint1[k], randint2[k], prime, 784)]
    # Find 1
    for j in range(784):
        # Column j is 1
        if mnist_train_bit_vec[i][j] == 1:
            # Pass all rows in signature matrix in column j.
            for k in range(k):
                if hash_values[k] < sig[k][j]:
                    sig[k][j] = hash_values[k]
                else:
                    continue
        else:
            continue

# Save the signature matrix.
np.save('mnist_train_minhash_sig', sig)
