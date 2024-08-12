import math
from miniCG import img
import numpy as np

def create():
    return np.array([], dtype=object)

def insert_dot(pol, dot):
    return np.array(pol.tolist() + [dot], dtype=object)

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
        
        if (len(pi) == 4):
            tx = pi[2] + t*(pf[2]-pi[2])
            ty = pi[3] + t*(pf[3]-pi[3])
            return np.array([x, y, tx, ty], np.float32)
        else:
            #print(f"t: {t}\npi[0]: {pi[1]}\n pf[0]: {pf[1]}\n----------")
            #print(t*(pf[0]-pi[0]))
            intst = color_intersec(pi, pf, t*(pf[1]-pi[1]), 0)

            return np.array([x, y, intst], dtype=object)
    
    # No intersection
    return np.array([-1, 0, 0, 0], np.float32)

def draw(buf, pol, intst):
    m = buf

    for i in range(0, pol.shape[0]-1):
        m = img.strt_line_ddaaa(m, pol[i, 0], pol[i, 1], pol[i+1, 0], pol[i+1, 1], intst)

    m = img.strt_line_ddaaa(m, pol[-1, 0], pol[-1, 1], pol[0, 0], pol[0, 1], intst)
    
    return m 

def draw_rgb(buf, pol):
    m = buf

    for i in range(0, pol.shape[0]-1):
        m = img.strt_line_ddaaa_rgb(m, pol[i, 0], pol[i, 1], pol[i+1, 0], pol[i+1, 1], pol[i, 2], pol[i+1, 2])

    m = img.strt_line_ddaaa_rgb(m, pol[-1, 0], pol[-1, 1], pol[0, 0], pol[0, 1], pol[i, 2], pol[i+1, 2])
    
    return m

def color_intersec(p1, p2, t, t_min):
    if (np.isscalar(p1[2]) and np.isscalar(p2[2])):
        if (p2[2] > p1[2]):
            color_range = abs(p2[2] - p1[2])
        else:
            color_range = abs(p1[2] - p2[2])

        color_min = np.min([p1[2], p2[2]])
        dots_range = math.sqrt(math.pow(p2[0]-p1[0], 2) + math.pow(p2[1]-p1[1], 2))
        
        intst = (((t - t_min) * color_range) / dots_range) + color_min
        
        return intst
    else:
        p1_b = [p1[0], p1[1], p1[2][0]]
        p1_g = [p1[0], p1[1], p1[2][1]]
        p1_r = [p1[0], p1[1], p1[2][2]]

        p2_b = [p2[0], p2[1], p2[2][0]]
        p2_g = [p2[0], p2[1], p2[2][1]]
        p2_r = [p2[0], p2[1], p2[2][2]]

        b = color_intersec(p1_b, p2_b, t, t_min)
        g = color_intersec(p1_g, p2_g, t, t_min)
        r = color_intersec(p1_r, p2_r, t, t_min)
        
        intst = np.array([b, g, r], np.uint8)

        return intst
    
def draw_circulo(center_x, center_y, radius):
    x = 0
    y = radius
    p = 1 - radius

    points = set()

    while x <= y:
        points.add((x + center_x, y + center_y))
        points.add((-x + center_x, y + center_y))
        points.add((x + center_x, -y + center_y))
        points.add((-x + center_x, -y + center_y))
        points.add((y + center_x, x + center_y))
        points.add((-y + center_x, x + center_y))
        points.add((y + center_x, -x + center_y))
        points.add((-y + center_x, -x + center_y))

        if p < 0:
            p += 2 * x + 3
        else:
            p += 2 * (x - y) + 5
            y -= 1

        x += 1

    return np.array(list(points), np.float32)

def set_circulo(m, p_sol, r, g, b):
    for point in p_sol:
        m = img.set_pixel(m, point[1], point[0], (r, g, b))
    return m

def draw_elipse(center_x, center_y, radius_x, radius_y):
    points = set()

    x = 0
    y = radius_y

    a_sqr = radius_x * radius_x
    b_sqr = radius_y * radius_y

    p = b_sqr - a_sqr * radius_y + 0.25 * a_sqr

    while b_sqr * x <= a_sqr * y:
        points.add((x + center_x, y + center_y))
        points.add((-x + center_x, y + center_y))
        points.add((x + center_x, -y + center_y))
        points.add((-x + center_x, -y + center_y))

        if p < 0:
            p += b_sqr * (2 * x + 3)
        else:
            p += b_sqr * (2 * x + 3) + a_sqr * (2 - 2 * y)
            y -= 1

        x += 1

    p = b_sqr * (x + 0.5) * (x + 0.5) + a_sqr * (y - 1) * (y - 1) - a_sqr * b_sqr

    while y >= 0:
        points.add((x + center_x, y + center_y))
        points.add((-x + center_x, y + center_y))
        points.add((x + center_x, -y + center_y))
        points.add((-x + center_x, -y + center_y))

        if p > 0:
            p += a_sqr * (3 - 2 * y)
        else:
            p += b_sqr * (2 * x + 2) + a_sqr * (3 - 2 * y)
            x += 1

        y -= 1

    return np.array(list(points), np.float32)

def set_elipse(m, p_elipse, r, g, b):
    for point in p_elipse:
        m = img.set_pixel(m, point[1], point[0], (r, g, b))
    return m