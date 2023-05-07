import numpy as np
import math
from miniCG import poly

def create():
    return np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], np.float32)

def translation(m, tx, ty):
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], np.float32).dot(m)

def scale(m, sx, sy):
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], np.float32).dot(m)

def rotation(m, ang):
    ang = math.radians(ang)

    return np.array([[math.cos(ang), -math.sin(ang), 0], [math.sin(ang), math.cos(ang), 0], [0, 0, 1]], np.float32).dot(m)

def apply(p, m):
    n_p = poly.create()
    for i in range(0, p.shape[0]):
        pt = np.append(p[i, 0:2], 1)

        pt = m.dot(pt)

        n_p = poly.insert_dot(n_p, np.append(pt[0:2], p[i, 2:]))
    
    return n_p
