import numpy as np
import math

def euclidean_distance(data):
    
    N = len(data)
    distance = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            distance[i][j] = 0.5 * math.sqrt((data[i][0] - data[j][0]) ** 2 + (data[i][1] - data[i][1]) ** 2) 
            + 0.5 * math.sqrt((data[i][2] - data[j][2]) ** 2 + (data[i][3] - data[i][3]) ** 2)

    return distance
