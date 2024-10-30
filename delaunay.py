from utils import angleof, is_point_in_circle, edges_to_points
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

def base_case(points):
    edges = []
    if len(points) == 2:
        edges.append(Edge(points[0], points[1]))
    elif len(points) == 3:
        edges.extend([Edge(points[0], points[1]), Edge(points[1], points[2]), Edge(points[2], points[0])])
    return edges

def lr_edge(left, right):
    left_bottom = min(left, key=lambda edge: (edge.p1.y, edge.p2.y))
    right_bottom = min(right, key=lambda edge: (edge.p1.y, edge.p2.y))
    return Edge(left_bottom.p1, right_bottom.p1)

def get_candidates(base_edge, points, is_right):
    base_point = base_edge.p2 if is_right else base_edge.p1
    reference_point = base_edge.p1 if is_right else base_edge.p2
    candidates = []
    
    for point in points:
        if point == base_point:
            continue
        
        angle = angleof(reference_point, base_point, point)
        
        if angle > 0:
            candidates.append((point, angle))
    
    candidates.sort(key=lambda x: x[1])
    return [point for point, angle in candidates]

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

def merge(left, right):
    edges = []
    base_lr_edge = lr_edge(left, right)
    edges.append(base_lr_edge)

    while True:

        left_candidate = None
        right_candidate = None
        right_candidates = get_candidates(base_lr_edge, edges_to_points(right), True)
        left_candidates = get_candidates(base_lr_edge, edges_to_points(left), False)
        
        while not right_candidate and len(right_candidates) > 0:
            if angleof(lr_edge.p1, lr_edge.p2, right_candidate) < math.pi and is_point_in_circle(base_lr_edge.p1, base_lr_edge.p2, right_candidates[0], right_candidates[1]):
                right_candidate = right_candidates[0]
            elif angleof(lr_edge, right_candidate) < math.pi:
                right_candidates.pop(0) # second holds but first doesnt, remove RR edge from potential candidates
            else:
                break # If the first criteria does not hold, we do not select a right candidate

        while not left_candidate and len(left_candidates) > 0:
            if angleof(lr_edge.p1, lr_edge.p2, left_candidate) < math.pi and is_point_in_circle(base_lr_edge.p1, base_lr_edge.p2, left_candidates[0], left_candidates[1]):
                left_candidate = left_candidates[0]
            elif angleof(lr_edge.p1, lr_edge.p2, left_candidate) < math.pi:
                left_candidates.pop(0) # second holds but first doesnt, remove LL edge from potential candidates
            else:
                break # If the first criteria does not hold, we do not select a left candidate

        if not left_candidate and not right_candidate:
            break

        # TODO: IMPLEMENT CASES WHERE ONE CANDIDATE AND BOTH CANDIDATES ARE SUBMITTED.


    return edges

def delaunay(points):
    points = sorted(points, key=lambda p: p.x)
    if len(points) <= 3:
        return base_case(points)

    midpoint = len(points) // 2
    left_points = points[:midpoint]
    right_points = points[midpoint:]

    return merge(delaunay(left_points), delaunay(right_points))
