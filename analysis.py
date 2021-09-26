import pandas as pd
import numpy as np
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
    for hydrogen in hydrogens:
        m = ho_o_w_h_iframes[hydrogen]
        cn.append(str(ho_o_w_h_iframes.loc[m, 'residue']))
    return len(set(cn))


