import sys
import cv2
import numpy as np
sys.path.append('..')
from miniCG import img, poly, transform, window, clipping

# Image shape
h = 372
w = 1227

# Viewport and Window 01
v1 = np.array([0, 0, w/2, h], np.float32)
j1 = np.array([0, 0, w/3.5, h], np.float32)

# Viewport and Window 02
v2 = np.array([w/4-w/8-10, 10, (w/2)-10, (h/4)+10], np.float32)
j2 = np.array([0, 0, w, h], np.float32)

# Load tex_bgture
tex_bg = cv2.imread("./assets/super_mario_world.jpg")
tex_mario = cv2.imread("./assets/mario.png")

bg = poly.create()
bg = poly.insert_dot(bg, [0, 0, 0, 0])
bg = poly.insert_dot(bg, [w, 0, 1, 0])
bg = poly.insert_dot(bg, [w, h, 1, 1])
bg = poly.insert_dot(bg, [0, h, 0, 1])

map_border = poly.create()
map_border = poly.insert_dot(map_border, [0, 0])
map_border = poly.insert_dot(map_border, [w, 0])
map_border = poly.insert_dot(map_border, [w, h])
map_border = poly.insert_dot(map_border, [0, h])

# Mario
mario = poly.create()
mario = poly.insert_dot(mario, [10, (h-h/10)-37, 0, 0])
mario = poly.insert_dot(mario, [(w/50), (h-h/10)-37, 1, 0])
mario = poly.insert_dot(mario, [(w/50), h-37, 1, 1])
mario = poly.insert_dot(mario, [10, h-37, 0, 1])

j_m = np.array([0, 0, w*1.5, h*1.5], np.float32)

# Create transformation matrix: Translation
m_t = transform.create()
m_t = transform.translation(m_t, 10, 0)

p = poly.create()
p = poly.insert_dot(p, [280, 230, [255, 0, 0]])
p = poly.insert_dot(p, [360, 230, [0, 255, 0]])
p = poly.insert_dot(p, [360, 310, [0, 0, 255]])
p = poly.insert_dot(p, [280, 310, [255, 255, 255]])

center_circle_radius = 3

circle1_center_x = 0 + 170
circle1_center_y = h-50
circle1_radius = 15
center_circle1_points = poly.draw_circulo(circle1_center_x, circle1_center_y, center_circle_radius)
circle1_points = poly.draw_circulo(circle1_center_x, circle1_center_y, circle1_radius)

circle2_center_x = w-1 - 10
circle2_center_y = h *1.5
circle2_radius = 15
center_circle2_points = poly.draw_circulo(circle2_center_x, circle2_center_y, center_circle_radius)
circle2_points = poly.draw_circulo(circle2_center_x, circle2_center_y, circle2_radius)

ellipse1_center_x = 0 + 170
ellipse1_center_y = h-150
ellipse1_radius_x = 20
ellipse1_radius_y = 30
ellipse1_points = poly.draw_elipse(ellipse1_center_x, ellipse1_center_y, ellipse1_radius_x, ellipse1_radius_y)

ellipse2_center_x = 0 + 170
ellipse2_center_y = h+75
ellipse2_radius_x = 40
ellipse2_radius_y = 60
ellipse2_points = poly.draw_elipse(ellipse2_center_x, ellipse2_center_y, ellipse2_radius_x, ellipse2_radius_y)


square_01 = poly.create()
square_01 = poly.insert_dot(square_01, [10, 10, [255, 0, 0]])
square_01 = poly.insert_dot(square_01, [20, 10, [0, 255, 0]])
square_01 = poly.insert_dot(square_01, [20, 20, [0, 0, 255]])
square_01 = poly.insert_dot(square_01, [10, 20, [255, 255, 255]])

square_02 = poly.create()
square_02 = poly.insert_dot(square_02, [10, 10, [255, 0, 0]])
square_02 = poly.insert_dot(square_02, [20, 10, [0, 255, 0]])
square_02 = poly.insert_dot(square_02, [20, 20, [0, 0, 255]])
square_02 = poly.insert_dot(square_02, [10, 20, [255, 255, 255]])

m_r = transform.create()
m_r = transform.translation(m_r, -170, -(h+75))
m_r = transform.rotation(m_r, 2)
m_r = transform.translation(m_r, 170, h+75)

# Animation loop
# Press Esc to end animation
k = None
# Screen 01
while(k != 27):
    # Create clean image
    m = img.create_rgb(w//2, h)

    m = img.scan_line_rgb(m, p)

    m = img.strt_line(m, 150, 100, 250, 200, 150)
    m = img.strt_line_dda(m, 200, 100, 100, 200, 150)
    
    m = poly.set_circulo(m, circle1_points, 0, 0, 255)
    m = poly.set_circulo(m, circle2_points, 255, 0, 0)

    m = poly.set_circulo(m, center_circle1_points, 255, 255, 255)
    m = poly.set_circulo(m, center_circle2_points, 255, 255, 255)

    # Adiciona as elipses à imagem animada
    m = poly.set_elipse(m, ellipse1_points, 0, 255, 0)  
    m = poly.set_elipse(m, ellipse2_points, 255, 0, 255)   

    # Show image generated
    cv2.imshow("mini-Mario", m)
    # Apply transformation: Rotation
    ellipse2_points = transform.apply(ellipse2_points, m_r)
    # Wait 10 milsecs or capture key pressed
    k = cv2.waitKey(1)

k = None

while(k != 27):
    # Create clean image
    m = img.create_rgb(w//2, h)

    pv = clipping.apply(j1, bg)
    pv = window.map_multi(pv, j1, v1)
    m = img.scan_line(m, pv, tex_bg)
    
    pv = window.map_multi(bg, j2, v2)
    m = img.scan_line(m, pv, tex_bg)
    
    pv = window.map_multi(map_border, j2, v2)
    m = poly.draw(m, pv, 255)

    pv = clipping.apply(j1, mario)
    pv = window.map_multi(pv, j1, v1)
    if (len(pv) != 0):
        m = img.scan_line(m, pv, tex_mario)
    
    pv = clipping.apply(j2, mario)
    pv = window.map_multi(pv, j2, v2)
    if (len(pv) != 0):
        m = img.scan_line(m, pv, tex_mario)
    else:
        break
    # Show image generated
    cv2.imshow("mini-Mario", m)
    # Apply transformation: Rotation
    mario = transform.apply(mario, m_t)
    # Wait 10 milsecs or capture key pressed
    k = cv2.waitKey(1)