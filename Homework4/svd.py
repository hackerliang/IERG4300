import numpy as np

m = np.array([
    [4,5,4,4,4],
    [0,1,0,2,3],
    [2,4,0,2,0],
    [5,3,1,0,0],
    [4,5,0,0,2],
    [0,0,0,4,3],
    [2,1,0,5,5]
])

u, s, vh = np.linalg.svd(m, full_matrices=True)

print('Shapes:\nm: {}\nu: {}\ns: {}\nvh: {}'.format(m.shape, u.shape, s.shape, vh.shape))
