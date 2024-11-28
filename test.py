from utils import *
from delaunay import *

# Example usage
p1 = Point( -987, -308 )
p2 = Point( -717, -619 )
p3 = Point( -52, 255 )
p4 = Point( -835, -316 )

if is_point_in_circle(p1, p2, p3, p4):
    print("The fourth point is in the circumcircle.")
else:
    print("The fourth point is not in the circumcircle.")