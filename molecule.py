import numpy as np
from scipy.spatial.distance import pdist, squareform

def distances(iframes, l, n):
    distanceframe = iframes[['x', 'y', 'z']]
    dim = 3
    positions = distanceframe.to_numpy()
    dist_nd_sq = np.zeros(n * (n-1) // 2)
    for d in range(dim):
        pos_1d = positions[:,d][:, np.newaxis]
        dist_1d = pdist(pos_1d)
        dist_1d[dist_1d > l*0.5] -= l
        dist_nd_sq += dist_1d**2

    dist_nd = squareform(np.sqrt(dist_nd_sq))

    return dist_nd

def findwaters(iframes, dist_nd):
    atom_oxygen = iframes.loc[iframes['type'] == 'O']
    atom_hydrogen = iframes.loc[iframes['type'] == 'H']
    atom_oxygen = atom_oxygen['index']

    i = 0

    for oxygen in atom_oxygen:
        hydrogen = np.where(
            (dist_nd[oxygen, ] < 1.5) &
            (dist_nd[oxygen, ] > 0.))[0]

        if len( hydrogen) == 2:
            m = (iframes['index'] == oxygen) | (iframes['index']   == hydrogen[0]) | (iframes['index'] == hydrogen[1])
            iframes.loc[m, 'mol'] = 'water'
            iframes.loc[m, 'residue'] = 'W' + str(i)


        elif len( hydrogen) == 1:

            m = (iframes['index'] == oxygen) | (iframes['index'] == hydrogen[0])

            iframes.loc[m, 'mol'] = 'hydroxide'
            iframes.loc[m, 'residue'] = 'OH' + str(i)

        i += 1


    return iframes

def angle(index_o, index_h1,  index_h2, dist_nd):
    dO_H1 = dist_nd[index_o, index_h1]
    dO_H2 = dist_nd[index_o, index_h2]
    dH1_H2 = dist_nd[index_h1, index_h2]
    return np.rad2deg(np.arccos((dO_H1**2 + dO_H2**2 - dH1_H2**2)/(2 * dO_H1 * dO_H2)))

