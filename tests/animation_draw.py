import sys
import cv2
sys.path.append('..')
from miniCG import img, poly, transform

# Image's shape
h = 400
w = 400

# Create clean image
#m = img.create(w, h)
#m = img.strt_line(m, 100, 100, 200, 200, 150)
#m = img.strt_line_dda(m, 250, 250, 450, 450, 150)

# Create polygon
p = poly.create()
p = poly.insert_dot(p, [160, 160, 0, 0])
p = poly.insert_dot(p, [240, 160, 1, 0])
p = poly.insert_dot(p, [240, 240, 1, 1])
p = poly.insert_dot(p, [160, 240, 0, 1])

# m = img.scan_line(m, p, tex)
# cv2.imshow("Test", m)
# cv2.waitKey(0)

# Create transformation matrix: Rotation
m_t = transform.create()
m_t = transform.translation(m_t, -200, -200)
m_t = transform.rotation(m_t, 2)
m_t = transform.translation(m_t, 200, 200)

# Animation loop
# Press Esc to end animation
k = None
while(k != 27):
    # Create clean image
    m = img.create(w, h)
    # Do Scanline
    m = poly.draw(m, p, 255)
    # Show image generated
    cv2.imshow("Test", m)
    # Wait 10 milsecs or capture key pressed
    k = cv2.waitKey(10)
    # Apply transformation: Rotation
    p = transform.apply(p, m_t)