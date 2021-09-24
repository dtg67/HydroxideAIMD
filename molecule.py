import numpy as np
from scipy.spatial.distance import pdist, squareform

def distances(distanceframe, l, n):
    dim = 3
    positions = distanceframe.to_numpy()
    dist_nd_sq = np.zeros(n * (n-1) // 2)
    for d in range(dim):
        pos_1d = positions[:,d][:, np.newaxis]
        dist_1d = pdist(pos_1d)
        dist_1d[dist_1d > l*0.5] -= l
        dist_nd_sq += dist_1d**2

    dist_nd = squareform(np.sqrt(dist_nd_sq))
    mindist = np.min(dist_nd[(dist_nd > 0.)])
    index = np.where(dist_nd == mindist)
    return [mindist, index[0].tolist(), dist_nd[0,]]
