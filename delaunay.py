# TODO Verify angle logic, ensure newly created base edge does not intersect any LL or RR edges, in case there are two points with the same lowest y value, should we select leftmost or right most point to form base LR edge or does this depend on if it is the base LR edge right point or left point

from utils import *
from scipy.spatial import ConvexHull, Delaunay
import numpy as np
import math

# Point class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point( {self.x}, {self.y} )"
# Edge class
class Edge:
    def __init__(self, p1, p2):
        # Ensure p1 is always the left point on the edge
        # edge is vertical, p1 is the lower point
        if p1.x < p2.x or (p1.x == p2.x and p1.y < p2.y):
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return (self.p1 == other.p1 and self.p2 == other.p2) or (self.p1 == other.p2 and self.p2 == other.p1)

    def __repr__(self):
        return f"Edge [ {self.p1}, {self.p2} ]"

    def __hash__(self):
        return hash((self.p1, self.p2))


#  Der-Tsai Lee and Bruce J. Schachter paper titled "Two Algorithms for Constructing a Delaunay Triangulation" describes how to get the lr edge of two sets of triangulations

def get_convex_hull(points):
    if len(points) <= 2:
        return points
    # Step 1: Convert the points to a NumPy array
    points_array = np.array([[p.x, p.y] for p in points])

    # Step 2: Pass the array to ConvexHull
    hull = ConvexHull(points_array)

    # Step 3: Extract the vertices as indices
    vertex_indices = hull.vertices

    # Step 4: Convert the indices back to the original Point objects
    convex_hull_points = [points[i] for i in vertex_indices]

    return convex_hull_points

def lr_edge(left_points, right_points):
    # Start by getting left convex hull and right convex hull
    left_hull_points = get_convex_hull(left_points)
    right_hull_points = get_convex_hull(right_points)

    # identify the rightmost point in the left hull as well as the leftmost point in the right hull
    # break ties by selecting the lower point
    p1 = max(left_hull_points, key=lambda p: (p.x, -p.y))
    p2 = min(right_hull_points, key=lambda p: (p.x, p.y))
    # start the base edge by connecting these two points
    # move clockwise along left hull, if the new point forms an edge lower than previous edge, update p1, counter-clockwise along right hull, repeat same process
    while True:
        moved = False

        # Check if we can move clockwise on the left hull to improve the edge
        next_p1 = next_point_on_hull(left_hull_points, p1, clockwise=True)
        if is_lower_edge(next_p1, p2, p1, p2):
            p1 = next_p1
            moved = True

        # Check if we can move counterclockwise on the right hull to improve the edge
        next_p2 = next_point_on_hull(right_hull_points, p2, clockwise=False)
        if is_lower_edge(p1, next_p2, p1, p2):
            p2 = next_p2
            moved = True

        # Stop if neither p1 nor p2 can move
        if not moved:
            break
    return Edge(p1, p2)


def next_point_on_hull(hull_points, current_point, clockwise=True):
    # Get the next point on the convex hull in the specified direction.
    # Wraps around if the end of the hull is reached.
    
    index = hull_points.index(current_point)
    if clockwise:
        return hull_points[(index - 1) % len(hull_points)]
    else:
        return hull_points[(index + 1) % len(hull_points)]


def is_lower_edge(p1_new, p2_new, p1_old, p2_old):
    # Determine if the new edge (p1_new, p2_new) is lower than the old edge (p1_old, p2_old).
    # This is based on comparing slopes.
    # if pivot point is on the right, if new slope is higher, we return True
    # if pivot point is on the left, if new slope is lower, we return True
    if (p2_old.x - p1_old.x) == 0:
        return True
    elif (p2_new.x - p1_new.x) == 0:
        return True
    else:
        old_slope = (p2_old.y - p1_old.y)/(p2_old.x - p1_old.x)
        new_slope = (p2_new.y - p1_new.y)/(p2_new.x - p1_new.x)
    return new_slope > old_slope if p2_new == p2_old else new_slope < old_slope
        
    
# Because p1 is always the left point on an edge, we need to figure out which point is lower first then use this to compare
# def lr_edge(left_points, right_points):
#     left_bottom = min(left_points, key=lambda point: (point.y, point.x))
#     right_bottom = min(right_points, key=lambda point: (point.y, point.x))
#     return Edge(left_bottom, right_bottom)

# candidates for triangulation are points that are connected to the base edge's left or right points in current triangulation
def get_candidates(base_edge, triangulation, is_right):
    base_point = base_edge.p2 if is_right else base_edge.p1
    reference_point = base_edge.p1 if is_right else base_edge.p2
    candidates = []
    for edge in triangulation:
        point1, point2 = edge.p1, edge.p2
        if is_right:
            if base_point == point1:
                angle = clockwise_angle(base_point, reference_point, base_point, point2)
                candidates.append((point2, angle))
            elif base_point == point2:
                angle = clockwise_angle(base_point, reference_point, base_point, point1)
                candidates.append((point1, angle))
        else:
            if base_point == point1:
                angle = clockwise_angle(base_point, point2, base_point, reference_point)
                candidates.append((point2, angle))
            elif base_point == point2:
                angle = clockwise_angle(base_point, point1, base_point, reference_point)
                candidates.append((point1, angle))
    
    candidates.sort(key=lambda x: x[1])
    return [point for point, angle in candidates]

# NOTES: Your implementation uses every single point within the right/left set of points as a possible candidate. I think the possible candidates are only the points that are connected to the base edge's left point or right point in the current triangulation. I only just commented it out incase I am wrong though

# def get_candidates(base_edge, points, is_right):
#     # if candidate points are selected from right set of points, base point is the edge's right point. otherwise for left set of points
#     base_point = base_edge.p2 if is_right else base_edge.p1
#     reference_point = base_edge.p1 if is_right else base_edge.p2
#     candidates = []
    
#     # sort every point in the subuset by the angle they make with the base edge. This gives the order to select our candidate points
#     for point in points:
#         if point == base_point:
#             continue
        
#         angle = angleof(reference_point, base_point, point)
        
#         if angle > 0:
#             candidates.append((point, angle))
    
#     candidates.sort(key=lambda x: x[1])
#     return [point for point, angle in candidates]


def is_delaunay(base_edge, candidate, triangulation):
    for edge in triangulation:
        if is_point_in_circle(base_edge.p1, base_edge.p2, candidate, edge.p2 if edge.p1 == candidate else edge.p1):
            return False
    return True

# def criteria_met(lr_edge, pt):
#     angle = angleof(lr_edge.p1, lr_edge.p2, pt)
#     if not (0 < angle < math.pi):
#         return False

#     return True

# triangulation refers to a set of edges we already have
def merge(left_triangulation, right_triangulation):
    triangulation = left_triangulation.union(right_triangulation)
    base_lr_edge = lr_edge(edges_to_points(left_triangulation), edges_to_points(right_triangulation))
    triangulation.add(base_lr_edge)

    while True:
        left_removed_edges = set()
        right_removed_edges = set()
        left_candidate = None
        right_candidate = None
        right_candidates = get_candidates(base_lr_edge, right_triangulation, True)
        left_candidates = get_candidates(base_lr_edge, left_triangulation, False)
        
        
        # for every potential right candidate, ensure
        # 1. the angle it makes with the base is less than 180 
        # 2. the next potential candidate is outside the circumcircle formed with the base edge
        # ASSUMPTION: If we are looking at the final point, then we do not bother testing for if the next point is within circumcircle
        while not right_candidate and len(right_candidates) > 0:
            curr_poss_candidate = right_candidates[0]
            next_poss_candidate = right_candidates[1] if len(right_candidates) > 1 else None
            test_angle = clockwise_angle(base_lr_edge.p2, base_lr_edge.p1, base_lr_edge.p2, curr_poss_candidate)
            if next_poss_candidate and test_angle < math.pi and not is_point_in_circle(base_lr_edge.p1, base_lr_edge.p2, curr_poss_candidate, next_poss_candidate):
                right_candidate = curr_poss_candidate
                break
            elif test_angle < math.pi and not next_poss_candidate:
                right_candidate = curr_poss_candidate
            elif test_angle < math.pi:
                # first holds but second doesnt, remove RR edge from potential candidates, consider next right candidate 
                triangulation.discard(Edge(base_lr_edge.p2, curr_poss_candidate))
                right_removed_edges.add(Edge(base_lr_edge.p2, curr_poss_candidate))
                right_candidates.pop(0) 
            else:
                break # If the first criteria does not hold, we do not select a right candidate

        while not left_candidate and len(left_candidates) > 0:
            curr_poss_candidate = left_candidates[0]
            next_poss_candidate = left_candidates[1] if len(left_candidates) > 1 else None
            test_angle = clockwise_angle(base_lr_edge.p1, curr_poss_candidate, base_lr_edge.p1, base_lr_edge.p2)
            if next_poss_candidate and test_angle < math.pi and not is_point_in_circle(base_lr_edge.p1, base_lr_edge.p2, curr_poss_candidate, next_poss_candidate):
                left_candidate = curr_poss_candidate
                break
            elif test_angle < math.pi and not next_poss_candidate:
                left_candidate = curr_poss_candidate
            elif test_angle < math.pi:
                # first holds but second doesnt, remove RR edge from potential candidates, consider next right candidate 
                triangulation.discard(Edge(base_lr_edge.p1, curr_poss_candidate))
                left_removed_edges.add(Edge(base_lr_edge.p1, curr_poss_candidate))
                left_candidates.pop(0) 
            else:
                break # If the first criteria does not hold, we do not select a left candidate
        
        # No candidates were returned, merge complete
        if not left_candidate and not right_candidate:
            triangulation.update(left_removed_edges)
            triangulation.update(right_removed_edges)
            break
        # Both candidates were returned, create new lr edge for candidate which forms circumcircle that does not contain other point
        elif left_candidate and right_candidate:
            if is_point_in_circle(base_lr_edge.p1, base_lr_edge.p2, right_candidate, left_candidate):
                new_lr_edge = Edge(left_candidate, base_lr_edge.p2)
                triangulation.update(right_removed_edges)
            else:
                new_lr_edge = Edge(base_lr_edge.p1, right_candidate)
                triangulation.update(left_removed_edges)
        # One candiate was returned, create new lr edge
        elif left_candidate or right_candidate:
            new_lr_edge = Edge(base_lr_edge.p1, right_candidate) if right_candidate else Edge(left_candidate, base_lr_edge.p2)
            triangulation.update(left_removed_edges) if right_candidate else triangulation.update(right_removed_edges)
        else:
            raise ValueError(f"No new edge was formed")
        triangulation.add(new_lr_edge)
        base_lr_edge = new_lr_edge

    return triangulation

# base case for dividing points
def base_case(points):
    edges = set()
    # if there are only two points, add an edge
    if len(points) == 2:
        edges.add(Edge(points[0], points[1]))
    # if there are three points, add edges between every two points
    elif len(points) == 3:
        edges.update([Edge(points[0], points[1]), Edge(points[1], points[2]), Edge(points[2], points[0])])
    return edges

def delaunay(points):
    points = sorted(points, key=lambda p: p.x)
    if len(points) <= 3:
        return base_case(points)

    midpoint = len(points) // 2
    left_points = points[:midpoint]
    right_points = points[midpoint:]

    return merge(delaunay(left_points), delaunay(right_points))
