import math
import sys
import csv

coordinates = []
dist_matrix = []
file_name = sys.argv[1]
print(file_name)


def distEuclidean(x1, y1, x2, y2):
    xdiff = x1 - x2
    ydiff = y1 - y2
    return math.sqrt(xdiff * xdiff + ydiff * ydiff)


def readTspfile(filename):
    f = open(filename, 'r')

    line = f.readline()

    while (line.find("EDGE_WEIGHT_TYPE")) == -1:
        line = f.readline()
    if line.find("EUC_2D") == -1 or line.find("ATT") == -1:
        dist_function = distEuclidean
    else:
        print("cannot deal with this type of input")
        raise Exception

    while line.find("NODE_COORD_SECTION") == -1:
        line = f.readline()

    while True:
        line = f.readline()
        if line.find('EOF') != -1:
            break

        print(line)
        (i, x, y) = line.split()
        x = float(x)
        y = float(y)
        coordinates.append([x, y])
    f.close()


readTspfile(file_name)
len_coordinate = len(coordinates)
dist_matrix = [[0.0 for col in range(len_coordinate)] for row in range(len_coordinate)]
visited = [False] * len_coordinate
for i in range(len(coordinates)):
    for j in range(len(coordinates)):
        # print(i, j)
        dist_matrix[i][j] = distEuclidean(coordinates[i][0], coordinates[i][1], coordinates[j][0], coordinates[j][1])


def calculateTourLength(dist_matrix, tour_sequence):
    dist = dist_matrix[tour_sequence[-1]][tour_sequence[0]]
    for i in range(1, len(tour_sequence)):
        dist += dist_matrix[tour_sequence[i - 1]][tour_sequence[i]]
    return dist


def makeClosestDistMatrix(dist_matrix, num):
    result = []
    for i in range(num):
        one_dist = [(dist_matrix[i, j], j) for j in range(num) if j != i]
        result.append(one_dist)
    return result


def findUnvistedNearest(here, unvisited, dist_matrix):
    to = unvisited[0]
    min_dist = dist_matrix[here][to]
    for i in unvisited[1:]:
        if dist_matrix[here][i] < min_dist:
            min_dist = dist_matrix[here][i]
            to = i
    return to


def NearestNeighbor(num_total_city, start, dist_matrix):
    unvisited = [i for i in range(num_total_city)]

    unvisited.remove(start)
    here = start
    tour_sequence = [start]
    while unvisited != []:
        to = findUnvistedNearest(here, unvisited, dist_matrix)
        tour_sequence.append(to)
        unvisited.remove(to)
        here = to
    return tour_sequence


tour_sequence = NearestNeighbor(len_coordinate, 0, dist_matrix)

print(calculateTourLength(dist_matrix, tour_sequence))

for i in range(len(tour_sequence)):
    tour_sequence[i] += 1
# print(tour_sequence)

with open('solution.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    writer.writerow(tour_sequence)
