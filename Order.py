

class Order(object):
    def __init__(self, number, business_x, business_y, customer_x, customer_y, 
                 start_time, end_time, pickup_time, cost, flag):
        self.number = number
        self.bus_x =business_x
        self.bus_y = business_y
        self.cust_x = customer_x
        self.cust_y = customer_y
        self.start_time = start_time
        self.end_time = end_time
        self.pickup_time = pickup_time
        self.cost = cost
        self.flag = flag