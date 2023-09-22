import numpy as np
from generate_random_population import generate_random_population


def pairwise_distance(SPs):
    # Implement your pairwise distance calculation here
    Distance = []
    Indx = []
    for i in range(len(SPs)):
        for j in range(i+1, len(SPs)):
            point1 = np.array(SPs[i])
            point2 = np.array(SPs[j])
            distance = np.linalg.norm(point1 - point2)
            Distance.append(distance)
            Indx.append((i, j))
    return Distance, Indx
    pass


def update_clusters(C, p1, p2):
    # 创建一个元素到子集合索引的映射
    element_to_subset = {}

    for i, subset in enumerate(C):
        for element in subset:
            element_to_subset[element] = i

    p1_subset = element_to_subset.get(p1)
    p2_subset = element_to_subset.get(p2)

    if p1_subset is None and p2_subset is None:
        # 若p1和p2都不在任何子集合中，添加新子集{p1, p2}
        C.append({p1, p2})
    elif p1_subset is not None and p2_subset is None:
        # 若p1在子集中而p2不在，将p2添加到p1所在的子集
        C[p1_subset].add(p2)
    elif p1_subset is None and p2_subset is not None:
        # 若p2在子集中而p1不在，将p1添加到p2所在的子集
        C[p2_subset].add(p1)
    elif p1_subset != p2_subset:
        # 若p1和p2分别在不同的子集中，合并这两个子集
        C[p1_subset] = C[p1_subset].union(C[p2_subset])
        del C[p2_subset]

    return C


def cluster_algorithm(SPs, Dmax=100):
    C = []
    Distance, Indx = pairwise_distance(SPs)
    for j in range(len(Distance)):
        p1, p2 = Indx[j]
        d = Distance[j]
        if d <= Dmax:
          C = update_clusters(C, p1, p2)
    Num = [num for num in range(len(SPs)) if num not in C]
    MinC = len(C)
    if MinC < 2:
        for num in Num:
            C.append({num})
    return C


if __name__ == "__main__":
    SPs = generate_random_population(100, 1000, 1000)
    Distance, Indx = pairwise_distance(SPs)
    clusters = cluster_algorithm(SPs)
    print(clusters)
