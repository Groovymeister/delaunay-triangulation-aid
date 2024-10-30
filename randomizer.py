import random

def random_points(n):
    random.seed(9)
    with open('random_tests/' + str(n) + '.txt', 'w') as file:
        file.write(str(n) + '\n')
        for _ in range(n):
            x = random.randint(-1000000, 1000000)
            y = random.randint(-1000000, 1000000)
            file.write(str(x) + ' ' + str(y) + '\n')

def main():
    tests = (10, 100, 1000, 10000)
    # Go over each test size and generate files
    for test in tests:
        random_points(test)

if __name__ == '__main__':
    main()