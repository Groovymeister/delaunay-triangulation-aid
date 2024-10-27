from delaunay import Point

def main():
    num_pts = int(input("Enter the number of points: "))
    points = list()
    for _ in range(num_pts):
        pt_input = input("Enter the point: ").split()
        points.append(Point(int(pt_input[0]), int(pt_input[1])))

if __name__ == '__main__':
    main()