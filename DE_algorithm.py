
# DE (Differential Evolution) 算法是一种用于全局优化的进化算法。
# 它最初由Storn和Price在1997年提出，用于解决连续参数优化问题。
# DE 算法的主要思想是通过模拟自然界中的进化过程来寻找最优解。
# 它通常用于解决没有显式数学表达式或导数的复杂优化问题。

import random

class SPDeploymentUpdater:
    def __init__(self, objective_function, initial_population, num_generations=100, F=0.5, CR=0.7):
        # 初始化类，设置算法参数和目标函数
        self.objective_function = objective_function
        self.population = initial_population
        self.num_generations = num_generations
        self.F = F
        self.CR = CR

    def de_rand_1(self, a, b, c):
        # DE/rand/1 操作，生成新个体
        new_vector = [a[j] + self.F * (b[j] - c[j]) for j in range(len(a))]
        return new_vector

    def binomial_crossover(self, target_vector, candidate_vector):
        # 二项式交叉操作，生成候选解
        candidate = []
        for j in range(len(target_vector)):
            if random.random() < self.CR or j == random.randint(0, len(target_vector) - 1):
                candidate.append(candidate_vector[j])
            else:
                candidate.append(target_vector[j])
        return candidate

    def evolve(self):
        for generation in range(self.num_generations):
            new_population = []

            for i, target_vector in enumerate(self.population):
                # 确保 a、b 和 c 与目标向量及彼此不同
                possible_vectors = [vec for vec in self.population if vec is not target_vector]
                a, b, c = random.sample(possible_vectors, 3)
                new_vector = self.de_rand_1(a, b, c)

                candidate_vector = self.binomial_crossover(target_vector, new_vector)
                target_fitness = self.objective_function(target_vector)
                candidate_fitness = self.objective_function(candidate_vector)

                if candidate_fitness <= target_fitness:
                    new_population.append(candidate_vector)
                else:
                    new_population.append(target_vector)

            # 更新种群
            self.population = new_population

        best_solution = min(self.population, key=self.objective_function)
        best_fitness = self.objective_function(best_solution)

        return best_solution, best_fitness

    def DE_evolutionary_operators(self):
        new_population = []

        for i, target_vector in enumerate(self.population):
            possible_vectors = [vec for vec in self.population if vec is not target_vector]
            a, b, c = random.sample(possible_vectors, 3)
            new_vector = self.de_rand_1(a, b, c)

            candidate_vector = self.binomial_crossover(target_vector, new_vector)
            new_population.append(candidate_vector)

        self.population = new_population
        return self.population



def evolutionary_DE(objective_function, initial_population):
    sp_updater = SPDeploymentUpdater(objective_function, initial_population)
    best_solution, best_fitness = sp_updater.evolve()
    return best_solution, best_fitness

# 示例用法
if __name__ == "__main__":
    # 定义目标函数
    def example_objective_function(solution):
        # 在这里根据问题定义目标函数，这个示例是简单的求和
        return sum(solution)
   
    # 初始化种群

    initial_population = [(374.5, 950.7, 100), (732.0, 598.7, 100), (156.0, 156.0, 100), (58.1, 866.2, 100), (601.1, 708.1, 100), (20.6, 969.9, 100), (832.4, 212.3, 100), (181.8, 183.4, 100), (304.2, 524.8, 100), (431.9, 291.2, 100), (611.9, 139.5, 100), (292.1, 366.4, 100), (456.1, 785.2, 100), (199.7, 514.2, 100), (592.4, 46.5, 100), (607.5, 170.5, 100), (65.1, 948.9, 100), (965.6, 808.4, 100), (304.6, 97.7, 100), (684.2, 440.2, 100), (122.0, 495.2, 100), (34.4, 909.3, 100), (258.8, 662.5, 100), (311.7, 520.1, 100), (546.7, 184.9, 100), (969.6, 775.1, 100), (939.5, 894.8, 100), (597.9, 921.9, 100), (88.5, 196.0, 100), (45.2, 325.3, 100), (388.7, 271.3, 100), (828.7, 356.8, 100), (280.9, 542.7, 100), (140.9, 802.2, 100), (74.6, 986.9, 100), (772.2, 198.7, 100), (5.5, 815.5, 100), (706.9, 729.0, 100), (771.3, 74.0, 100), (358.5, 115.9, 100), (863.1, 623.3, 100), (330.9, 63.6, 100), (311.0, 325.2, 100), (729.6, 637.6, 100), (887.2, 472.2, 100), (119.6, 713.2, 100), (760.8, 561.3, 100), (771.0, 493.8, 100), (522.7, 427.5, 100), (25.4, 107.9, 100), (31.4, 636.4, 100), (314.4, 508.6, 100), (907.6, 249.3, 100), (410.4, 755.6, 100), (228.8, 77.0, 100), (289.8, 161.2, 100), (929.7, 808.1, 100), (633.4, 871.5, 100), (803.7, 186.6, 100), (892.6, 539.3, 100), (807.4, 896.1, 100), (318.0, 110.1, 100), (227.9, 427.1, 100), (818.0, 860.7, 100), (7.0, 510.7, 100), (417.4, 222.1, 100), (119.9, 337.6, 100), (942.9, 323.2, 100), (518.8, 703.0, 100), (363.6, 971.8, 100), (962.4, 251.8, 100), (497.2, 300.9, 100), (284.8, 36.9, 100), (609.6, 502.7, 100), (51.5, 278.6, 100), (908.3, 239.6, 100), (144.9, 489.5, 100), (985.7, 242.1, 100), (672.1, 761.6, 100), (237.6, 728.2, 100), (367.8, 632.3, 100), (633.5, 535.8, 100), (90.3, 835.3, 100), (320.8, 186.5, 100), (40.8, 590.9, 100), (677.6, 16.6, 100), (512.1, 226.5, 100), (645.2, 174.4, 100), (690.9, 386.7, 100), (936.7, 137.5, 100), (341.1, 113.5, 100), (924.7, 877.3, 100), (257.9, 660.0, 100), (817.2, 555.2, 100), (529.7, 241.9, 100), (93.1, 897.2, 100), (900.4, 633.1, 100), (339.0, 349.2, 100), (726.0, 897.1, 100), (887.1, 779.9, 100)]
    # 创建 SPDeploymentUpdater 实例
    sp_updater = SPDeploymentUpdater(example_objective_function, initial_population)
    best_solution, best_fitness = sp_updater.evolve()

    pop_updater = sp_updater.DE_evolutionary_operators()

    print("最优解:", best_solution)
    print("最优适应度:", best_fitness)
    print("更新路径：", pop_updater)



