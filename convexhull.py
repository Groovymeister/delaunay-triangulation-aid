def graham_scan(points):
    # Step 1: Sort points by x, and by y as a tiebreaker
    points = sorted(points, key=lambda p: (p[0], p[1]))

    # Step 2: Build the lower hull using cross product 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Step 3: Build the upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Step 4: Combine lower and upper hulls
    # Remove the last point of each half because it's repeated
    return lower[:-1] + upper[:-1]

def cross_product(p1, p2, p3):
    # Calculate the cross product of vectors p1p2 and p1p3
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
