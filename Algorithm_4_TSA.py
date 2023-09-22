import numpy as np
from generate_random_population import generate_random_population
import time


def evaluate_solution(sol, pop):
    # Implement your solution evaluation method here
    total_distance = 0
    for i in range(len(sol) - 1):
        start_point = sol[i]
        end_point = sol[i + 1]
        distance = np.linalg.norm(np.array(pop[start_point]) - np.array(pop[end_point]))
        total_distance += distance
    return total_distance
pass

def apply_operator(sol, operator):
    # Implement your operator application method here
    temp = sol.copy()
    if operator == 'Swap':
        # Select two distinct indices randomly
        idx1, idx2 = np.random.choice(len(temp), size=2, replace=False)
        # Swap the values at the selected indices
        temp[idx1], temp[idx2] = temp[idx2], temp[idx1]

    elif operator == 'Reversion':
        # Select a sub-route randomly (start and end indices)
        start_idx, end_idx = np.random.choice(len(temp), size=2, replace=False)
        if start_idx > end_idx:
            start_idx, end_idx = end_idx, start_idx
        # Reverse the order of the selected sub-route
        temp[start_idx:end_idx + 1] = temp[start_idx:end_idx + 1][::-1]

    elif operator == 'Insertion':
        # Select an index randomly to insert an SP
        insert_idx = np.random.randint(len(temp))
        # Select an SP randomly to insert
        sp_to_insert = np.random.choice(temp)
        # Insert the selected SP at the chosen index
        temp = np.insert(temp, insert_idx, sp_to_insert)

    return temp
    pass

def tabu_search_algorithm(C, MaxIT, POP):
    # 搜索的候选集Q 最大迭代次数 MaxIT 输入聚类集合C, 禁忌长度Lt和紧禁忌列表TL。
    Q = []

    for j in range(len(C)):
        ## ____________________________________初始化阶段__________________________________________
        AL = ['Swap', 'Reversion', 'Insertion']     # 创建操作列表
                                # 为 Swap、Reversion 和 Insertion 操作创建操作列表 AL
        nA = len(AL)            # 计算操作数量： 计算操作列表的长度，存储在 nA 中。
        Lt = round(0.5 * nA)    # 将禁忌长度 Lt 设置为操作数量的一半（向下取整）
        TL = np.zeros(nA)       # 将禁忌列表 TL 初始化为全零数组
        Cj = C[j]               # 选择聚类： 从聚类集合 C 中选择当前的聚类 Cj。
        Sol = list(Cj)          # 随机生成初始解: 使用 np.random.shuffle 随机打乱当前聚类 Cj 中的元素顺序，
        np.random.shuffle(Sol)  # 得到一个初始解 Sol。
        Cost = evaluate_solution(Sol, POP)  # 调用 evaluate_solution 方法评估初始解 Sol 的成本。
                                            # 初始化最佳解和成本: 将当前解 Sol 设为最佳解 BestSol，
                                            # 将其成本设为最佳成本 BestCost
        Best = {'best_sol' : Sol, 'best_cost': Cost}


        ## ___________________________________迭代搜索______________________________________________
        for it in range(MaxIT):             # 迭代搜索： 迭代 MaxIT 次搜索。
            bestnewCost = float('inf')      # 初始化最佳新成本： 将 bestnewCost 初始化为正无穷。
            bestnewSoLN = []
            BestSolN_iteration = []
            BestCost_iteration = []
            for i in range(nA):             # 循环遍历操作： 遍历每个操作 AL[i]，其中 i 是操作索引。
                if TL[i] == 0:              # 检查禁忌状态： 如果操作 i 不在禁忌状态（TL[i] == 0），执行以下操作：
                    SolN = apply_operator(Sol, AL[i])       # 调用 apply_operator 方法，使用操作 AL[i]，生成新的解 SolN
                    CostN = evaluate_solution(SolN, POP)    # 评估新解： 调用 evaluate_solution 方法评估新解 SolN 的成本。
                    BestSolN_iteration.append(SolN)
                    BestCost_iteration.append(CostN)        # 更新最佳新解和成本：
                    if CostN <= bestnewCost:                # 如果新解的成本 CostN 小于等于当前的最佳新成本 bestnewCost
                        bestnewCost = CostN                 # 将新解设为最佳新解 BestSolN，并更新最佳新成本 BestnewCost
                        bestnewSoLN = SolN

            for i in range(nA):                             # 更新禁忌列表： 遍历每个操作 AL[i]，更新禁忌列表 TL。
                if i == np.argmin(BestCost_iteration):
                    TL[i] = Lt
                else:
                    TL[i] = max(TL[i] - 1, 0)
            if bestnewCost <= Best['best_cost']:            # 判断是否更新最佳解： 如果最佳新成本 BestnewCost 小于等于当前的最佳成本
                Best['best_sol'] = bestnewSoLN
                Best['best_cost'] = bestnewCost
        Q.append(Best['best_sol'])
    return Q

if __name__ == "__main__":

    POP = generate_random_population(100, 1000, 1000)
    C = [{35, 67, 6, 70, 75, 77, 52, 58},
         {65, 71, 8, 9, 10, 11, 76, 13, 14, 15, 20, 85, 86, 23, 87, 24, 30, 94, 32, 97, 42, 51, 62},
         {99, 17, 56, 25, 26, 91}, {39, 72, 41, 18, 83, 54, 55, 90, 61},
         {88, 73, 19, 81}, {92, 22, 79}, {66, 2, 7, 74, 28, 29},
         {33, 34, 3, 36, 5, 45, 16, 82, 21, 95},
         {96, 1, 4, 37, 68, 40, 43, 44, 78, 46, 47, 59, 93},
         {64, 50, 84}, {98, 57, 27, 60, 63}]

    start_time = time.time()
    Q = tabu_search_algorithm(C, 30, POP)
    end_time = time.time()

    runtime = end_time - start_time
    print("Algorithm runtime:", runtime, "seconds")