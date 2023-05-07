import numpy as np
from miniCG import transform

def map_multi(p, j, v):
    xiv = v[0]
    yiv = v[1]
    xfv = v[2]
    yfv = v[3]
    xi = j[0]
    yi = j[1]
    xf = j[2]
    yf = j[3]

    a = (xfv - xiv)/(xf - xi)
    b = (yfv - yiv)/(yf - yi)

    m = np.array([[a, 0, xiv - a*xi], [0, b, yiv - b*yi], [0, 0, 1]],  np.float32)

    p = transform.apply(p, m)

    return p


def map(p, j, v):
    lv = v[0]
    av = v[1]
    xi = j[0]
    yi = j[1]
    xf = j[2]
    yf = j[3]

    m = np.array([[lv/(xf-xi), 0, (1 - xi*lv/(xf-xi))], [0, av/(yf-yi), (1 - yi*av/(yf-yi))], [0, 0, 1]], np.float32)

    return transform.apply(p, m)