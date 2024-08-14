import numpy as np
from miniCG import poly

invalid_point = np.array([-1, 0, 0, 0], np.float32)

def intersec(axis_x=False, axis_y=False, seg=[]):
    if(axis_x):
        a_i = 0
        axis = axis_x
    else:
        a_i = 1
        axis = axis_y

    if (seg[0][0] < seg[1][0]):
        p_l = seg[0]
        p_r = seg[1]
    else:
        p_r = seg[0]
        p_l = seg[1]

    t = (axis - p_l[a_i])/(p_r[a_i]-p_l[a_i])

    if (t >= 0 and t <= 1):
        intersec_p = p_l[1-a_i] + t*(p_r[1-a_i]-p_l[1-a_i])

        tx = p_l[2] + t*(p_r[2]-p_l[2])
        ty = p_l[3] + t*(p_r[3]-p_l[3])

        if (axis_x):
            x, y = axis_x, intersec_p
        else:
            x, y = intersec_p, axis_y
        
        return np.array([x, y, tx, ty], np.float32)
    
    return invalid_point

def framing(edges, p1, p2):
    p = np.array([], np.float32)

    swap = False

    p_l = np.copy(p1)
    p_r = np.copy(p2)

    left_ed = edges[0]
    bottom_ed = edges[1]
    right_ed = edges[2]
    top_ed = edges[3]

    # Sort horizontaly
    if (p_r[0] < p_l[0]):
        p_l, p_r = p_r, p_l
        swap = True

    # Left Edge Test - Through
    if (p_l[0] < left_ed and p_r[0] >= left_ed):
        p_l = intersec(axis_x=left_ed, seg=[p_l, p_r])
        p = np.array(p.tolist() + [p_l], np.float32)
        p = np.array(p.tolist() + [p_r], np.float32)
    # Left Edge Test - Inside
    elif (p_l[0] >= left_ed and p_r[0] >= left_ed):
        p = np.array(p.tolist() + [p_l], np.float32)
        p = np.array(p.tolist() + [p_r], np.float32)

    # If complete horizontaly left outside, return
    if (len(p) == 0):
        return p
    
    # Right Edge Test - Through
    if (p_l[0] <= right_ed and p_r[0] > right_ed):
        p_r = intersec(axis_x=right_ed, seg=[p_l, p_r])
        p[1] = p_r
    # Right Edge Test - Outside
    elif (p_l[0] > right_ed and p_r[0] > right_ed):
        p = np.delete(p, (0,1), axis=0)
        # Complete horizontaly right outside, return
        return p
    # Complement of Left Edge Test - Inside

    # Sort verticaly
    if (p_r[1] < p_l[1]):
        p_l, p_r = p_r, p_l
        if (len(p) > 0 and swap):
            p[0], p[1] = p[1], p[0]
        swap = False

    # Top Edge Test - Through
    if (p_l[1] <= top_ed and p_r[1] > top_ed):
        p_r = intersec(axis_y=top_ed, seg=[p_l, p_r])
        p[1] = p_r
        #print(f"p: {p}")
    # Top Edge Test - Outside
    elif(p_l[1] > top_ed and p_r[1] > top_ed):
        p = np.delete(p, (0,1), axis=0)
        # Complete horizontaly right outside, return
        return p
    # Complement of Left and Right Edge Test - Inside

    # Bottom Edge Test - Throught
    if(p_l[1] < bottom_ed and p_r[1] >= bottom_ed):
        #print("Intersec bottom_ed")
        p_l = intersec(axis_y=bottom_ed, seg=[p_l, p_r])
        p[0] = p_l
    # Bottom Edge Test - Outside
    elif(p_l[1] < bottom_ed and p_r[1] < bottom_ed):
        p = np.delete(p, (0,1), axis=0)
        # Complete horizontaly right outside, return
        return p
    # Complement of Top Edge Test - Inside

    # Setting to initial order
    if (len(p) > 0 and swap):
        p[0], p[1] = p[1], p[0]
    
    return p

def apply(v, pol):

    p = poly.create()
    for i in range(0, pol.shape[0]-1):
        for dot in framing(v, pol[i], pol[i+1]):
            p = poly.insert_dot(p, dot)
    
    
    if (p.shape[0] != 0 and p.shape[1] != 0):
        p = np.delete(p, -1, 0)
    
    for dot in framing(v, pol[3], pol[2]):
        p = poly.insert_dot(p, dot)

    if (p.shape[0] != 0 and p.shape[1] != 0):
        p = np.delete(p, -1, 0)
        p = poly.insert_dot(p, p[0])
   
    return p