import sys
import cv2
import numpy as np
sys.path.append('..')
from miniCG import img, poly, transform, window

# Image shape
h = 300
w = 200

# Window
j = np.array([-1, -1, 2, 1], np.float32)

# Load texture
tex = cv2.imread("../assets/cat.jpg")
tex = cv2.cvtColor(tex, cv2.COLOR_RGB2GRAY)

# Create Polygon 01
p1 = poly.create();
p1 = poly.insert_dot(p1, [-0.5, -0.5, 0, 0])
p1 = poly.insert_dot(p1, [0.5, -0.5, 1, 0])
p1 = poly.insert_dot(p1, [0.5, 0.5, 1, 1])
p1 = poly.insert_dot(p1, [-0.5, 0.5, 0, 1])

# Create Polygon 02
p2 = poly.create();
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

    # Map Poly 01 to Viewport
    pv1 = window.map(p1, j, [w, h])
    # Do Scanline
    m = img.scan_line(m, pv1, tex)

    # Map Poly 02 to Viewport
    pv2 = window.map(p2, j, [w, h])
    # Do Scanline
    m = img.scan_line(m, pv2, tex)

    # Show image generated
    cv2.imshow("Test", m)
    # Apply transformation: Rotation
    p1 = transform.apply(p1, m_t)
    # Wait 10 milsecs or capture key pressed
    k = cv2.waitKey(10)