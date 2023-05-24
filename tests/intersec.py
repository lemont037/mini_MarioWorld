import sys
import numpy as np
sys.path.append('..')
from miniCG import poly, clipping

# Create polygon
p = poly.create()
p = poly.insert_dot(p, [160, 130, 0, 0])
p = poly.insert_dot(p, [240, 160, 1, 0])

intersec_p = clipping.intersec(axis_x=170, seg=p)

if ((intersec_p != clipping.invalid_point).any()):
    print(f"Intersec point: {intersec_p}")
else:
    print("No intersection.")