import numpy as np
from scipy.spatial.distance import pdist, squareform


def distances(iframes, length, n):

    distanceframe = iframes[['x', 'y', 'z']]
    dim = 3
    positions = distanceframe.to_numpy()
    dist_nd_sq = np.zeros(n * (n-1) // 2)
    for d in range(dim):
        pos_1d = positions[:, d][:, np.newaxis]
        dist_1d = pdist(pos_1d)
        dist_1d[dist_1d > length*0.5] -= length
        dist_nd_sq += dist_1d**2

    dist_nd = squareform(np.sqrt(dist_nd_sq))

    return dist_nd


def findwaters(iframes, dist_nd, hydroxide):

    atom_oxygen = iframes.loc[iframes['type'] == 'O', 'index']
    i = 0

    for oxygen in atom_oxygen:
        hydrogen = np.where(
            (dist_nd[oxygen, ] <= 1.225) &
            (dist_nd[oxygen, ] > 0.)
        )[0]

        if len(hydrogen) == 2:
            m = (iframes['index'] == oxygen) | \
                (iframes['index'] == hydrogen[0]) | \
                (iframes['index'] == hydrogen[1])
            iframes.loc[m, 'mol'] = 'water'
            iframes.loc[m, 'residue'] = 'W' + str(i)

        elif len(hydrogen) == 1:
            m = (iframes['index'] == oxygen) | (iframes['index'] == hydrogen[0])
            iframes.loc[m, 'mol'] = 'hydroxide'
            iframes.loc[m, 'residue'] = 'OH'

        i += 1
    if len(iframes.loc[iframes['mol'] == 'hydroxide']) == 0:
        hydroxide = list(hydroxide)
        m1 = (iframes['index'] == hydroxide[0])
        m2 = (iframes['index'] == hydroxide[1])

        iframes.loc[m1, ['residue', 'mol']] = 'OH', 'hydroxide'
        iframes.loc[m2, ['residue', 'mol']] = 'OH', 'hydroxide'

    return iframes


def angle(index_o, index_h1,  index_h2, dist_nd):

    do_h1 = dist_nd[index_o, index_h1]
    do_h2 = dist_nd[index_o, index_h2]
    dh1_h2 = dist_nd[index_h1, index_h2]
    return np.rad2deg(np.arccos((do_h1**2 + do_h2**2 - dh1_h2**2)/(2 * do_h1 * do_h2)))


def zundel(iframes, dist_nd):

    atom_oxygen = iframes.loc[(
                            (iframes['mol'] == 'hydroxide') |
                            (iframes['mol'] == 'NULL')
                              ) &
                              (iframes['type'] == 'O'), 'index']
    atom_hydrogen = iframes.loc[(
                            (iframes['mol'] == 'hydroxide') |
                            (iframes['mol'] == 'NULL')
                              ) &
                              (iframes['type'] == 'H'), 'index']
    min_h = 10
    hydroxide_o = list(atom_oxygen)[0]
    hydroxide_h = list(atom_hydrogen)[0]

    for oxygen in atom_oxygen:
        a = dist_nd[oxygen, ]
        min_dist_h = np.min(a[np.nonzero(a)])

        hydrogen = np.where(
            (dist_nd[oxygen, ] == min_dist_h)
        )[0]
        if min_dist_h < min_h:
            min_h = min_dist_h
            hydroxide_h = hydrogen[0]
            hydroxide_o = oxygen

    iframes.loc[iframes['index'] == hydroxide_o, 'residue'] = 'OH'
    iframes.loc[iframes['index'] == hydroxide_h, 'residue'] = 'OH'

    zundel_o = list(atom_oxygen)
    zundel_h = list(atom_hydrogen)
    zundel_o.remove(hydroxide_o)
    zundel_h.remove(hydroxide_h)

    iframes.loc[iframes['index'] == zundel_o[0], ['residue', 'mol']] = 'WZ', 'water'

    for hydrogen in zundel_h:
        iframes.loc[iframes['index'] == hydrogen, ['residue', 'mol']] = 'WZ', 'water'

    return iframes


