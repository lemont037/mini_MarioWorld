import sys
import cv2
import numpy as np
sys.path.append('..')
from miniCG import img, poly, transform, window

# Image shape
h = 500
w = 500

# Viewport and Window 01
v1 = np.array([1, 1, h/2-1, w/2-1], np.float32)
j1 = np.array([-1, -1, 1, 1], np.float32)

# Viewport and Window 02
v2 = np.array([0, w/2-1, h-1, w-1], np.float32)
j2 = np.array([-1, -1, 1, 1], np.float32)

# Viewport and Window 03
v3 = np.array([h/2-1, 1, h-1, w/2-1], np.float32)
j3 = np.array([-10, -10, 10, 10], np.float32)

# Load texture
tex = cv2.imread("../assets/cat.jpg", 0)

# Create Polygon 01
p1 = poly.create()
p1 = poly.insert_dot(p1, [-0.5, -0.5, 0, 0])
p1 = poly.insert_dot(p1, [0.5, -0.5, 1, 0])
p1 = poly.insert_dot(p1, [0.5, 0.5, 1, 1])
p1 = poly.insert_dot(p1, [-0.5, 0.5, 0, 1])

# Create Polygon 02
p2 = poly.create()
p2 = poly.insert_dot(p2, [1, -0.25, 0, 0])
p2 = poly.insert_dot(p2, [1.5, -0.25, 1, 0])
p2 = poly.insert_dot(p2, [1.5, 0.25, 1, 1])
p2 = poly.insert_dot(p2, [1, 0.25, 0, 1])

# Create transformation matrix: Rotation
m_t = transform.create()
m_t = transform.rotation(m_t, 2)

# Animation loop
# Press Esc to end animation
k = None
while(k != 27):
    # Create clean image
    m = img.create(w, h)
    
    # Map Poly 01 to Viewport 01
    pv = window.map_multi(p1, j1, v1)
    # Do Scanline
    m = img.scan_line(m, pv, tex)
    # Map Poly 02 to Viewport 01
    pv = window.map_multi(p2, j1, v1)
    # Do Scanline
    m = img.scan_line(m, pv, tex)
    # Map Poly 01 to Viewport 02
    pv = window.map_multi(p1, j2, v2)
    # Do Scanline
    m = img.scan_line(m, pv, tex)
    # Map Poly 02 to Viewport 02
    pv = window.map_multi(p2, j2, v2)
    # Do Scanline
    m = img.scan_line(m, pv, tex)
    # Map Poly 01 to Viewport 03
    pv = window.map_multi(p1, j3, v3)
    # Do Scanline
    m = img.scan_line(m, pv, tex)
    # Map Poly 02 to Viewport 03
    pv = window.map_multi(p2, j3, v3)
    # Do Scanline
    m = img.scan_line(m, pv, tex)

    # Show image generated
    cv2.imshow("Test", m)
    # Apply transformation: Rotation
    p1 = transform.apply(p1, m_t)
    # Wait 10 milsecs or capture key pressed
    k = cv2.waitKey(10)