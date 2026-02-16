import numpy as np

def compute_distance_matrix(coords):
    # (N, 1, 2) - (1, N, 2) -> (N, N, 2)
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    # sum((N, N, 2)**2, axis=2) -> (N, N)
    dist = np.sqrt(np.sum(diff**2, axis=-1))
    return dist
