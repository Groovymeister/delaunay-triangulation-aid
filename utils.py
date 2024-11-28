import math
import numpy as np

def remove_edges_with_point(triangulation, point):
    return [edge for edge in triangulation if edge.p1 != point and edge.p2 != point]

def angleof(p1, p2, p3):
    dx1, dy1 = p2.x - p1.x, p2.y - p1.y
    dx2, dy2 = p3.x - p2.x, p3.y - p2.y
    return math.atan2(dy2, dx2) - math.atan2(dy1, dx1)

# Checks if point d is in circumcircle formed by points a,b,c
def is_point_in_circle(p1, p2, p3, p4):
    # Extract coordinates of points
    ax, ay = p1.x, p1.y
    bx, by = p2.x, p2.y
    cx, cy = p3.x, p3.y
    dx, dy = p4.x, p4.y
    
    # Shift the points relative to p4
    ax_, ay_ = ax - dx, ay - dy
    bx_, by_ = bx - dx, by - dy
    cx_, cy_ = cx - dx, cy - dy
    
    # Perform the calculation
    result = (
        (ax_ * ax_ + ay_ * ay_) * (bx_ * cy_ - cx_ * by_) -
        (bx_ * bx_ + by_ * by_) * (ax_ * cy_ - cx_ * ay_) +
        (cx_ * cx_ + cy_ * cy_) * (ax_ * by_ - bx_ * ay_)
    )
    
    return result > 0
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

def clockwise_angle(p1, p2, q1, q2):
    # Create vectors
    v1_x, v1_y = p2.x - p1.x, p2.y - p1.y
    v2_x, v2_y = q2.x - q1.x, q2.y - q1.y
    
    # Calculate the signed angle using atan2
    angle = math.atan2(v1_x * v2_y - v1_y * v2_x, v1_x * v2_x + v1_y * v2_y)
    
    # Convert to clockwise angle
    clockwise_angle = (2 * math.pi - angle) % (2 * math.pi)
    
    return clockwise_angle  # Returns angle in radians