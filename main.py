import numpy as np
from affinity_prop import *
from utils import *
import pandas as pd
import Order
from clustering import KMeans


if __name__ == "__main__":
    # 读取数据
    setOrder = []
    problemSet = pd.read_excel('Problem Set.xlsx', header=[0])
    number = "订单ID"
    bus_x = "商家经度"
    bus_y = "商家纬度"
    cust_x = "客户经度"
    cust_y = "客户纬度"
    start_time = "订单分配时间"
    end_time = "承诺送达时间"
    pickup_time = "预计取餐时间"
    cost = "订单金额"
    flag = "是否购买准时宝"
    for x in range(problemSet[number].size):
        setOrder.append(Order.Order(problemSet[number].iloc[x], problemSet[bus_x].iloc[x], problemSet[bus_y].iloc[x], problemSet[cust_x].iloc[x], 
                                    problemSet[cust_y].iloc[x], problemSet[start_time].iloc[x], problemSet[end_time].iloc[x], problemSet[pickup_time].iloc[x],
                                    problemSet[cost].iloc[x], problemSet[flag].iloc[x]))

    points = []
    for x in setOrder:
        points.append([x.bus_x, x.bus_y, x.cust_x, x.cust_y])
    
    distance = euclidean_distance(points)
    print("Starting Affinity Propagation...")
    af_prop = AffinityProp(distance)
    exemplar_indices, exemplar_assignments = af_prop.solve()
    print("The number of cluster: %s" % len(exemplar_indices))
    print("cluster center indices: %s" % (exemplar_indices))
    # print(len(exemplar_assignments))
    # print(np.unique(exemplar_assignments, return_counts=True))
    
    initial_means = []
    for index in exemplar_indices:
        initial_means.append(Order.Order(setOrder[index].number, setOrder[index].bus_x, setOrder[index].bus_y, setOrder[index].cust_x, 
                                setOrder[index].cust_y, setOrder[index].start_time, setOrder[index].end_time, 
                                setOrder[index].pickup_time, setOrder[index].cost, setOrder[index].flag))
    model = KMeans(setOrder, len(exemplar_indices), initial_means)
    clusters = model.fit()
    print("The number of cluster: %s" %len(clusters))
    for i in range(len(clusters)):
        print("Number of orders in cluster %s: %s" %(i+1, len(clusters[i])))


