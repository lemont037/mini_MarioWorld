import time
import cv2
from miniCG import img, poly, transform

h = 100
w = 100

m = img.create(w, h)
#m = img.strt_line(m, 100, 100, 200, 200, 150)
#m = img.strt_line_dda(m, 250, 250, 450, 450, 150)

tex = cv2.imread("cat.jpg")
tex = cv2.cvtColor(tex, cv2.COLOR_RGB2GRAY)

p = poly.create()
p = poly.insert_dot(p, [40, 40, 0, 0])
p = poly.insert_dot(p, [60, 40, 1, 0])
p = poly.insert_dot(p, [60, 60, 1, 1])
p = poly.insert_dot(p, [40, 60, 0, 1])

# m = img.scan_line(m, p, tex)
# cv2.imshow("Test", m)
# cv2.waitKey(0)

m_t = transform.create()
m_t = transform.translation(m_t, -50, -50)
m_t = transform.rotation(m_t, 2)
m_t = transform.translation(m_t, 50, 50)

while(True):
    m = img.create(w, h)
    m = img.scan_line(m, p, tex)
    cv2.imshow("Test", m)
    cv2.waitKey(0)
    p = transform.apply(p, m_t)