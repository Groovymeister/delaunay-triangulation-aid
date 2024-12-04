from delaunay import *
from scipy.spatial import Delaunay
import numpy as np
import sys

def main():
    points = list()
    with open(sys.argv[1], 'r') as file:
        num_pts = int(file.readline().strip())
        for _ in range(num_pts):
            x, y = map(int, file.readline().strip().split())
            points.append(Point(x, y))
    delaunay_triangulation = delaunay(points)
    print("PREDICTED")
    for edge in delaunay_triangulation:
        print(edge)
    print()
    test_triangulation = Delaunay(np.array([[p.x, p.y] for p in points]))
    simplices = test_triangulation.simplices
    edges = set()
    for simplex in simplices:
        # Extract the 3 vertex indices for the triangle
        p1_idx, p2_idx, p3_idx = simplex
        
        # Create edges for each pair of vertices (each triangle has 3 edges)
        edge1 = Edge(points[p1_idx], points[p2_idx])
        edge2 = Edge(points[p2_idx], points[p3_idx])
        edge3 = Edge(points[p3_idx], points[p1_idx])
        
        # Add the edges to the list
        edges.update([edge1, edge2, edge3])
    # print("ACTUAL")
    # for edge in edges:
    #     print(edge)

    print(f"SCIPY IMPLEMENTATION number of edges {len(edges)}")
    print(f"OUR IMPLEMENTATION number of edges {len(delaunay_triangulation)}")
    # # Check if the edges match
    if edges == delaunay_triangulation:
        print("Compared set of scipy delaunay implementation with ours, The triangulation edges match!")
    else:
        print("The edge lists do not match.")



    # # Convert edge objects to sorted tuples of indices
    # edges_indices = []
    # def get_point_index(points, point):
    #     for i, p in enumerate(points):
    #         if (p.x == point.x and p.y == point.y):
    #             return i
    #     return -1  # If not found, return -1
    # for edge in delaunay_triangulation:
    #     idx1 = get_point_index(points, edge.p1)
    #     idx2 = get_point_index(points, edge.p2)
    #     # Sort the indices to ensure consistent ordering
    #     edges_indices.append(tuple(sorted([idx1, idx2])))

    # test_triangulation = Delaunay(np.array([[p.x, p.y] for p in points]))
    # # Get the list of triangles (simplices), each defined by 3 vertex indices
    # simplices = test_triangulation.simplices
    # # Function to extract edges from simplices
    # test_edges = set()
    # for simplex in simplices:
    #     # Get the 3 edges of the triangle, using the indices of the vertices
    #     test_edges.add(frozenset([simplex[0], simplex[1]]))
    #     test_edges.add(frozenset([simplex[1], simplex[2]]))
    #     test_edges.add(frozenset([simplex[2], simplex[0]]))
    # # Convert each edge from a frozenset to a sorted tuple (for consistency)
    # test_edges = [tuple(sorted(edge)) for edge in test_edges]

    # edges_indices_set = set(edges_indices)
    # delaunay_edges_set = set(test_edges)

    # # Check if the edges match
    # if edges_indices_set == delaunay_edges_set:
    #     print("The edge lists match!")
    # else:
    #     print("The edge lists do not match.")


if __name__ == '__main__':
    main()