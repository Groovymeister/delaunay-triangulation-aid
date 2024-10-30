from delaunay import Point, delaunay
import sys

def main():
    points = list()
    with open(sys.argv[1], 'r') as file:
        num_pts = int(file.readline().strip())
        for _ in range(num_pts):
            x, y = map(int, file.readline().strip().split())
            points.append(Point(x, y))
    delaunay_triangulation = delaunay(points)
    print(delaunay_triangulation)

if __name__ == '__main__':
    main()