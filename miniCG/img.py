import math
from miniCG import poly
import numpy as np

def create(w, h):
    return np.zeros((h, w), np.uint8)

def set_pixel(img, x, y, intst):
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    
    if x > img.shape[1]-1:
        x = img.shape[1]-1
    if y > img.shape[0]-1:
        y = img.shape[0]-1
    
    x, y = int(round(x)), int(round(y))

    img[y, x] = intst

    return img

def get_pixel(tex, x, y):
    if (x > 1):
        x = 1
    if (x < 0):
        x = 0
    
    if (y > 1):
        y = 1
    if (y < 0):
        y = 0
    
    x = round(x*(tex.shape[1]-1))
    y = round(y*(tex.shape[0]-1))

    return tex[y][x]

def strt_line(buf, xi, yi, xf, yf, intst):
    img = buf

    dx = xf - xi
    dy = yf - yi

    if (dx == 0 and dy == 0):
        img = set_pixel(img, xi, yi, intst)
        return img
    
    swap = False
    if abs(dy) > abs(dx):
        dx, dy = dy, dx
        xi, yi = yi, xi
        swap = True
    
    a = dy/dx

    for vx in range(0, abs(dx)):
        if (dx < 0):
            vx = -vx

        vy = a*vx
        x = round(xi + vx)
        y = round(yi + vy)

        if (swap):
            img = set_pixel(img, x, y, intst)
        else:
            img = set_pixel(img, y, x, intst)

    return img

def strt_line_dda(buf, xi, yi, xf, yf, intst):
    img = buf

    dx = xf-xi
    dy = yf-yi

    steps = abs(dx);
    if (abs(dy) > abs(dx)):
        steps = abs(dy)

    if (steps == 0):
        img = set_pixel(img, xi, yi, intst)
        return img

    steps_x = dx/steps
    steps_y = dy/steps

    for i in range(0, steps):
        x = round(xi + i*steps_x)
        y = round(yi + i*steps_y)

        img = set_pixel(img, x, y, intst)

    return img

def bresenham(buf, xi, yi, xf, yf, intst):
    img = buf

    dx = xf-xi
    dy = yf-yi

    dx2 = 2*dx
    dy2 = 2*dy

    p = -dx + dy2
    x = round(xi)
    y = round(yi)

    for i in range(0, abs(dx)):
        img = set_pixel(img, x, y, intst)

        x = x+1
        if (p >= 0):
            y += 1

            p = p-dx2+dy2
        else:
            p += dy2
    
    return img

def bresenham_circle(buf, xi, yi, xf, yf, intst):
    img = buf
    r = math.sqrt(math.pow((xf-xi), 2)-math.pow((yf-yi), 2))
    c = 2*math.pi*r

    dx = xf-xi
    dy = yf-yi

    dx2 = 2*dx
    dy2 = 2*dy

    p = math.sqrt(math.pow(r, 2)-math.pow(x, 2))
    x = 0
    y = round(r)

    for i in range(0, abs(c/8)):
        img = set_pixel(img, x, y, intst)

        x = x+1
        if (p >= 0):
            y += 1

            p = p-math.sqrt(math.pow(r, 2)-math.pow(x, 2))
        else:
            p += dy2
    
    return img

def strt_line_ddaaa(buf, xi, yi, xf, yf, intst):
    img = buf

    dx = round(xf-xi)
    dy = round(yf-yi)

    steps = abs(dx)
    if (abs(dy) > abs(dx)):
        steps = abs(dy)

    step_x = dx/steps
    step_y = dy/steps

    for i in range(0, steps):
        x = xi+i*step_x
        y = yi+i*step_y

        if (abs(round(step_x)) == 1):
            yd = y-np.floor(y)

            img = set_pixel(img, round(x), np.floor(y), round((1-yd)*intst)) 
            img = set_pixel(img, round(x), np.floor(y+1), round(yd*intst)) 
        else:
            xd = x-np.floor(x)

            img = set_pixel(img, np.floor(x), round(y), round((1-xd)*intst))
            img = set_pixel(img, np.floor(x+1), round(y), round(xd*intst))

    return img

def scan_line(buf, pol, tex):
    img = buf

    y_min = round(np.min(pol[:, 1]))
    y_max = round(np.max(pol[:, 1]))

    for y in range(y_min, y_max):
        i = np.array([], np.float32)

        pi = pol[0, :]

        for p in range(1, pol.shape[0]):
            pf = pol[p, :]

            p_int = poly.intersec(y, [pi, pf])

            if (p_int[0] >= 0):
                i = np.array(i.tolist() + [p_int], np.float32)

            pi = pf

        pf = pol[0, :]

        p_int = poly.intersec(y, [pi, pf])

        if (p_int[0] >= 0):
            i = np.array(i.tolist() + [p_int], np.float32)

        for pi in range(0, i.shape[0]-1, 2):
            p1 = i[pi, :]
            p2 = i[pi+1, :]

            x1 = p1[0]
            x2 = p2[0]

            if (x2 < x1):
                p1, p2 = p2, p1

            for xk in range(round(p1[0]), round(p2[0])):
                pc = (xk - p1[0])/(p2[0]-p1[0])

                tx = p1[2] + pc*(p2[2]-p1[2])
                ty = p1[3] + pc*(p2[3]-p1[3])
        
                intst = get_pixel(tex, tx, ty)

                img = set_pixel(img, xk, y, intst)

    return img