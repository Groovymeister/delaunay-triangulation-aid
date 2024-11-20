# TODO Verify angle logic, ensure newly created base edge does not intersect any LL or RR edges, in case there are two points with the same lowest y value, should we select leftmost or right most point to form base LR edge or does this depend on if it is the base LR edge right point or left point

from utils import angleof, is_point_in_circle, edges_to_points
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

# base case for dividing points
def base_case(points):
    edges = []
    # if there are only two points, add an edge
    if len(points) == 2:
        edges.append(Edge(points[0], points[1]))
    # if there are three points, add edges between every two points
    elif len(points) == 3:
        edges.extend([Edge(points[0], points[1]), Edge(points[1], points[2]), Edge(points[2], points[0])])
    return edges

# select the lowest point within the left and right set of points and add edge between them to create lower base edge (tangent)

# Because p1 is always the left point on an edge, we need to figure out which point is lower first then use this to compare
def lr_edge(left_points, right_points):
    left_bottom = min(left_points, key=lambda point: (point.y, point.x))
    right_bottom = min(right_points, key=lambda point: (point.y, point.x))
    return Edge(left_bottom, right_bottom)

# candidates for triangulation are points that are connected to the base edge's left or right points in current triangulation
def get_candidates(base_edge, triangulation, is_right):
    base_point = base_edge.p2 if is_right else base_edge.p1
    reference_point = base_edge.p1 if is_right else base_edge.p2
    candidates = []
    for edge in triangulation:
        point1, point2 = edge.p1, edge.p2
        if base_point == point1:
            angle = angleof(reference_point, base_point, point1)
            candidates.append((point1, angle))
        elif base_point == point2:
            angle = angleof(reference_point, base_point, point2)
            candidates.append((point2, angle))
    
    candidates.sort(key=lambda x: x[1])
    return [point for point, angle in candidates]

# NOTES: Your implementation uses every single point within the right set of points as a possible candidate. I think the possible candidates are only the points that are connected to the base edge's left point or right point in the current triangulation. I only just commented it out incase I am wrong though

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

def criteria_met(lr_edge, pt):
    angle = angleof(lr_edge.p1, lr_edge.p2, pt)
    if not (0 < angle < math.pi):
        return False

    return True

# triangulation refers to a set of edges we already have
def merge(left_triangulation, right_triangulation):
    triangulation = left_triangulation.union(right_triangulation)
    base_lr_edge = lr_edge(edges_to_points(left_triangulation), edges_to_points(right_triangulation))
    triangulation.add(base_lr_edge)

    while True:

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
            test_angle = angleof(lr_edge.p1, lr_edge.p2, curr_poss_candidate)
            if next_poss_candidate and test_angle < math.pi and is_point_in_circle(base_lr_edge.p1, base_lr_edge.p2, curr_poss_candidate, next_poss_candidate):
                right_candidate = curr_poss_candidate
                break
            elif test_angle < math.pi:
                # first holds but second doesnt, remove RR edge from potential candidates, consider next right candidate 
                triangulation.discard(Edge(base_lr_edge.p2, curr_poss_candidate))
                right_candidates.pop(0) 
            else:
                break # If the first criteria does not hold, we do not select a right candidate

        while not left_candidate and len(left_candidates) > 0:
            curr_poss_candidate = left_candidates[0]
            next_poss_candidate = left_candidates[1] if len(left_candidates) > 1 else None
            test_angle = angleof(lr_edge.p1, lr_edge.p2, curr_poss_candidate)
            if next_poss_candidate and test_angle < math.pi and is_point_in_circle(base_lr_edge.p1, base_lr_edge.p2, curr_poss_candidate, next_poss_candidate):
                left_candidate = curr_poss_candidate
                break
            elif test_angle < math.pi:
                # first holds but second doesnt, remove RR edge from potential candidates, consider next right candidate 
                triangulation.discard(Edge(base_lr_edge.p1, curr_poss_candidate))
                left_candidates.pop(0) 
            else:
                break # If the first criteria does not hold, we do not select a left candidate
        
        # No candidates were returned, merge complete
        if not left_candidate and not right_candidate:
            break
        # Both candidates were returned, create new lr edge for candidate which forms circumcircle that does not contain other point
        elif left_candidate and right_candidate:
            if is_point_in_circle(base_lr_edge.p1, base_lr_edge.p2, right_candidate, left_candidate):
                new_lr_edge = Edge(left_candidate, base_lr_edge.p2)
            else:
                new_lr_edge = Edge(base_lr_edge.p1, right_candidate)
        # One candiate was returned, create new lr edge
        elif left_candidate or right_candidate:
            new_lr_edge = Edge(base_lr_edge.p1, right_candidate) if right_candidate else Edge(left_candidate, base_lr_edge.p2)
        else:
            raise ValueError(f"No new edge was formed")
        base_lr_edge = new_lr_edge

    return triangulation

def delaunay(points):
    points = sorted(points, key=lambda p: p.x)
    if len(points) <= 3:
        return base_case(points)

    midpoint = len(points) // 2
    left_points = points[:midpoint]
    right_points = points[midpoint:]

    return merge(delaunay(left_points), delaunay(right_points))
