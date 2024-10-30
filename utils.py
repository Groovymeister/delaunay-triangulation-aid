import math

def remove_edges_with_point(triangulation, point):
    return [edge for edge in triangulation if edge.p1 != point and edge.p2 != point]

def angleof(p1, p2):
    return math.atan2(p2.y - p1.y, p2.x - p1.x)

def is_point_in_circle(a, b, c, d):
    ax, ay = a.x - d.x, a.y - d.y
    bx, by = b.x - d.x, b.y - d.y
    cx, cy = c.x - d.x, c.y - d.y

    det = (ax * (by * cy - by * cy) - bx * (ay * cy - by * cy) + cx * (ay * by - by * cy))
    return det > 0

def is_valid(base_edge, candidate, triangulation):
    for edge in triangulation:
        if is_point_in_circle(base_edge.p1, base_edge.p2, candidate, edge.p2 if edge.p1 == candidate else edge.p1):
            return False
    return True