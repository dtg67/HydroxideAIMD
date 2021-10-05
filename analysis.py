import pandas as pd
import numpy as np
import os
from molecule import distances


def hydroxide_o_to_water_h_frames(iframes):

    m_hydroxide_o = (iframes['mol'] == 'hydroxide') & (iframes['type'] == 'O')
    m_water_h = (iframes['mol'] == 'water') & (iframes['type'] == 'H')
    hydroxide_o = iframes.loc[m_hydroxide_o]
    water_h = iframes.loc[m_water_h]
    ho_o_w_h_iframes = [hydroxide_o, water_h]
    ho_o_w_h_iframes = pd.concat(ho_o_w_h_iframes)
    return ho_o_w_h_iframes


def hydroxide_o_to_water_h(ho_o_w_h_iframes, length):

    n = len(ho_o_w_h_iframes['index'])
    dist_nd = distances(ho_o_w_h_iframes, length, n)
    return dist_nd[0, ]


def coordination_num(ho_o_w_h_iframes, radius, dist_array):
    hydrogens = np.where(
            (dist_array <= radius) &
            (dist_array > 0.)
        )
    cn = []

    for hydrogen in hydrogens[0]:
        cn.append(str(ho_o_w_h_iframes.iloc[hydrogen].residue))

    return set(cn)


def cn2gaussian(cn, iframes, i,):
    cn = list(cn)
    cn_num = len(cn)
    cn.extend(['OH', 'WZ'])
    gauss_iframes = iframes.loc[iframes['residue'].isin(cn)]
    cn_path = 'cn_' + str(cn_num)
    gauss_iframes = gauss_iframes[['type', 'x', 'y', 'z']]
    if not os.path.exists(cn_path):
        os.makedirs(cn_path)

    file = cn_path + '/' + str(i)+'.xyz'
    gauss_iframes.to_csv(file, header = False, index = False, sep = '\t')


    return True


