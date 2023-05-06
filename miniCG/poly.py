import numpy as np

def create():
    return np.array([], np.float32)

def insert_dot(pol, dot):
    return np.array(pol.tolist() + [dot], np.float32)

def intersec(scan, seg):
    pi = seg[0]
    pf = seg[1]

    y = scan

    # If it's a horizontal segment, there's no intersection
    if (pi[1] == pf[1]):
        return np.array([-1, 0, 0, 0], np.float32)
    
    # Swap to guarantee initial dot over
    if (pi[1] > pf[1]):
        pi, pf = pf, pi

    # Calculating t
    t = (y - pi[1])/(pf[1]-pi[1])

    # Calculating x
    if (t > 0 and t <= 1):
        x = pi[0] + t*(pf[0]-pi[0])
        
        tx = pi[2] + t*(pf[2]-pi[2])
        ty = pi[3] + t*(pf[3]-pi[3])

        return np.array([x, y, tx, ty], np.float32)
    
    # No intersection
    return np.array([-1, 0, 0, 0], np.float32)