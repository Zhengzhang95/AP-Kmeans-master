import random
import math
import numpy as np
import matplotlib.pyplot as plt
import csv
import Order

class KMeans:
    def __init__(self, geo_locs, k, initial):
        self.geo_locations = geo_locs
        self.k = k
        self.clusters = None
        self.means = []
        self.initial = initial

    def next_random(self, index, points, clusters):
        # This method returns the next random node
        # Pick the next node that has the maximum distance from other nodes
        dist = {}
        for point_1 in points:
            # Compute the distance of this node from all other points in the cluster
            for cluster in clusters.values():
                point_2 = cluster[0]
                if point_1 not in dist:
                    dist[point_1] = 0.5 * math.sqrt((point_1.bus_x - point_2.bus_x) ** 2 + (point_1.bus_y - point_2.bus_y) ** 2) 
                    + 0.5 * math.sqrt((point_1.cust_x - point_2.cust_x) ** 2 + (point_1.cust_y - point_2.cust_y) ** 2)
                else:
                    dist[point_1] += 0.5 * math.sqrt((point_1.bus_x - point_2.bus_x) ** 2 + (point_1.bus_y - point_2.bus_y) ** 2) 
                    + 0.5 * math.sqrt((point_1.cust_x - point_2.cust_x) ** 2 + (point_1.cust_y - point_2.cust_y) ** 2)
        # Now let's return the point that has the maximum distance from previous nodes
        max_point = max(dist, key=dist.get)
        return max_point

    def initial_means(self, points):
        # Compute the initial means
        # Pick the first node at random
        # point_ = random.choice(points)
        # clusters = {0: [point_]}
        # points.remove(point_)
        # # Now let's pick k-1 more random points
        # for i in range(1, self.k):
        #     point_ = self.next_random(i, points, clusters)
        #     clusters[i] = [point_]
        #     points.remove(point_)
        clusters = {}
        for i in range(self.k):
            clusters[i] = [self.initial[i]]
        # Compute mean of clusters
        self.means = self.compute_means(clusters)

    def compute_means(self, clusters):
        means = []
        for cluster in clusters.values():
            mean_point = Order.Order(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            cnt = 0.0
            for point in cluster:
                mean_point.bus_x += point.bus_x
                mean_point.bus_y += point.bus_y
                mean_point.cust_x += point.cust_x
                mean_point.cust_y += point.cust_y
                cnt += 1.0
            mean_point.bus_x /= cnt
            mean_point.bus_y /= cnt
            mean_point.cust_x /= cnt
            mean_point.cust_y /= cnt
            means.append(mean_point)
        return means

    def assign_points(self, points):
        # Assign nodes to the cluster with the smallest mean
        clusters = {}
        for point in points:
            dist = []
            # Find the best cluster for this node
            for mean in self.means:
                dist.append(0.5 * math.sqrt((point.bus_x - mean.bus_x) ** 2 + (point.bus_y - mean.bus_y) ** 2) 
                    + 0.5 * math.sqrt((point.cust_x - mean.cust_x) ** 2 + (point.cust_y - mean.cust_y) ** 2))
            # Let's find the smallest mean
            index = dist.index(min(dist))
            clusters.setdefault(index, []).append(point)
        return clusters

    def update_means(self, means, threshold):
        # Compare current means with the previous ones to see if we have to stop
        for mean_1, mean_2 in zip(self.means, means):
            if (0.5 * math.sqrt((mean_1.bus_x - mean_2.bus_x) ** 2 + (mean_1.bus_y - mean_2.bus_y) ** 2) 
                    + 0.5 * math.sqrt((mean_1.cust_x - mean_2.cust_x) ** 2 + (mean_1.cust_y - mean_2.cust_y) ** 2)) > threshold:
                return False
        return True

    def save(self, filename="output.csv"):
        # Save clusters into a CSV file
        with open(filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['number', 'business_x', 'business_y', 'customer_x', 'customer_y', 'start_time', 'end_time', 'pickup_time', 'cluster_id'])
            for cluster_id, cluster in enumerate(self.clusters.values()):
                for point in cluster:
                    writer.writerow([point.number, point.bus_x, point.bus_y, point.cust_x, point.cust_y, point.start_time, point.end_time, point.pickup_time, cluster_id])


    def fit(self, plot_flag = False):
        # Run k-means algorithm
        if len(self.geo_locations) < self.k:
            return -1   # Error
        points_ = self.geo_locations.copy()
        # Compute the initial means
        self.initial_means(points_)
        stop = False
        iterations = 1
        print("Starting K-Means...")
        while not stop:
            # Assignment step: assign each node to the cluster with the closest mean
            points_ = self.geo_locations.copy()
            clusters = self.assign_points(points_)
            means = self.compute_means(clusters)
            stop = self.update_means(means, 0.01)
            if not stop:
                self.means = means
            iterations += 1
        print(f"K-Means completed in {iterations} iterations.")
        self.clusters = clusters
        # Plot cluster for evaluation
        if plot_flag:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            markers = ['o', 'd', 'x', 'h', 'H', 7, 4, 5, 6, '8', 'p', ',', '+', '.', 's', '*', 3, 0, 1, 2]
            colors = ['r', 'k', 'b', [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
            for cluster_id, cluster in enumerate(clusters.values()):
                bus_x = []  
                bus_y = []
                cust_x = []
                cust_y = []
                for point in cluster:
                    bus_x.append(point.bus_x)
                    bus_y.append(point.bus_y)
                    cust_x.append(point.cust_x)
                    cust_y.append(point.cust_y)
                ax.scatter(bus_x, bus_y, s=20, c=colors[cluster_id % len(colors)], marker=markers[cluster_id % len(markers)])
                ax.scatter(cust_x, cust_y, s=20, c=colors[cluster_id % len(colors)], marker=markers[cluster_id % len(markers)])
            plt.show()
        self.save()
        return self.clusters
