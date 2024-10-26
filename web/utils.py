import numpy as np # type: ignore


def cosine_distance(x1, x2):
    return np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))
