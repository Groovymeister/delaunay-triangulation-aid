from utils import angleof, is_point_in_circle

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

def get_candidate(base_edge, edges, right):
    pass

def is_delaunay(base_edge, candidate, triangulation):
    for edge in triangulation:
        if is_point_in_circle(base_edge.p1, base_edge.p2, candidate, edge.p2 if edge.p1 == candidate else edge.p1):
            return False
    return True

def remove_edges_with_point(triangulation, point):
    return [edge for edge in triangulation if edge.p1 != point and edge.p2 != point]

def merge(left, right):
    edges = []
    base_lr_edge = lr_edge(left, right)
    edges.append(base_lr_edge)

    

    return edges

def delaunay(points):
    points = sorted(points, key=lambda p: p.x)
    if len(points) <= 3:
        return base_case(points)

    midpoint = len(points) // 2
    left_points = points[:midpoint]
    right_points = points[midpoint:]

    return merge(delaunay(left_points), delaunay(right_points))
