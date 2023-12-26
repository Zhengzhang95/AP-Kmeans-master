
class Parameters(object):
    def __init__(self):
        self.speed = 50  # 外卖员平均速度
        self.Fuel_consume = 200  # 单位油耗成本
        self.Penalty_ratio = [0.3, 0.35, 0.7]  # 赔付比例
        self.extra_ratio = 0.1 # 购买准时宝额外赔付比例
        self.Penalty_time = [10, 20, 30] # 超时时间
        self.diff_speed = [50, 40, 50, 30]  # 不同骑手平均速度
        self.service_level = [0.99, 0.85, 0.9, 0.8] # 不同骑手服务水平
        self.fixed_cost = [5, 3, 3, 2]  # 不同骑手启动成本
        self.capacity = 12  # 外卖车最大载重