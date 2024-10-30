import math

def remove_edges_with_point(triangulation, point):
    return [edge for edge in triangulation if edge.p1 != point and edge.p2 != point]

def angleof(p1, p2, p3):
    dx1, dy1 = p2.x - p1.x, p2.y - p1.y
    dx2, dy2 = p3.x - p2.x, p3.y - p2.y
    return math.atan2(dy2, dx2) - math.atan2(dy1, dx1)

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

def edge_to_points(edge):
    return [edge.p1, edge.p2]

def edges_to_points(edges):
    points = set()
    for edge in edges:
        points.add(edge.p1)
        points.add(edge.p2)
    return list(points)