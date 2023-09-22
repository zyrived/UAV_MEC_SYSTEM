import numpy as np


# 设置随机种子



# 自定义装饰器
def my_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper


# 应用装饰器到生成种群的函数
@my_decorator
def generate_random_population(pop_size, Xmax, Ymax, Zmax=100, seed=42):
    # TODO 生成随机种群
    np.random.seed(seed)
    POP = []
    for _ in range(pop_size):
        # 生成随机的 X 和 Y 坐标
        X = np.random.uniform(0, Xmax)
        Y = np.random.uniform(0, Ymax)
        X_round = round(X, 1)
        Y_round = round(Y, 1)
        POP.append((X_round, Y_round, Zmax))
    return POP

if __name__ == "__main__":
    initial_POP = generate_random_population(50, 100, 100)
    print("初始种群:")
    print(initial_POP)
