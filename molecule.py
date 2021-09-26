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


def findwaters(iframes, dist_nd):

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
            iframes.loc[m, 'residue'] = 'OH' + str(i)
        else:
            print(iframes.i)
            print(len(hydrogen))
        i += 1

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
            hydroxide_h = hydrogen
            hydroxide_o = oxygen

    iframes.loc[iframes['index'] == hydroxide_o, 'residue'] = 'hydroxide'
    iframes.loc[iframes['index'] == hydroxide_h, 'residue'] = 'hydroxide'

    zundel_o = list(atom_oxygen).pop(hydroxide_o)
    zundel_h = list(atom_hydrogen).pop(hydroxide_h)

    for oxygen in zundel_o:
        iframes.loc[iframes['index'] == oxygen, ['residue', 'mol']] = 'water', 'WZ'

    for hydrogen in zundel_h:
        iframes.loc[iframes['index'] == hydrogen, ['residue', 'mol']] = 'water', 'WZ'

    return iframes


