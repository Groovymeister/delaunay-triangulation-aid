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

def merge(left, right):
    pass

def delaunay(points):
    points = sorted(points, key=lambda p: p.x)
    if len(points) <= 3:
        return base_case(points)

    midpoint = len(points) // 2
    left_points = points[:midpoint]
    right_points = points[midpoint:]

    return merge(delaunay(left_points), delaunay(right_points))