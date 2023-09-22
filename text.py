import numpy as np

class Evaluate:
    def __init__(self, UEs, SPs, UAv):
        # initialize parameters
        self.UEs = UEs
        self.SPs = SPs
        self.UAv = UAv
        # constant parameters
        self.H = 200
        self.beta = 2.8
        self.gamma = 1000
        self.alpha = -30
        self.B = 1e6
        self.sigma_square = -250
        self.p_hov = 1000
        self.p_ue = 1000
        self.P_fly = 1000
        self.D_i =  400
        self.velocity = 20
        self.E_M = 1
        self.num_ues = len(self.UEs)
        self.num_uav = len(self.UAv)
        self.a_ij = np.zeros((self.num_ues, self.num_uav))
        self.r_ij = np.zeros((self.num_ues, self.num_uav))
        self.pair_UEs_with_SPs()
        self.calculate_aij_s()

    def pair_UEs_with_SPs(self):
        # calculate distance between UEs and SPs
        ue_coords = np.array(self.UEs)
        sp_coords = np.array(self.SPs)[:, :2]
        self.distances = np.sqrt(np.sum((ue_coords[:, np.newaxis, :] - sp_coords) ** 2, axis=-1))
        # find the closest SP for each UE
        self.min_sp_indices = np.argmin(self.distances, axis=1)
        self.min_sp_distance = np.min(self.distances, axis=1)

    def calculate_aij_s(self):
        # calculate the pairing between UEs and UAVs
        for i, sp_index in enumerate(self.min_sp_indices):
            while np.all(self.a_ij[i, :] == 0):
                for j, uav_set in enumerate(self.UAv):
                    if sp_index in uav_set:
                        self.a_ij[i, j] = 1
                        break
                if np.any(self.a_ij[i, :] != 0):
                    break
                else:
                    # if the SP is not classified, delete it and select again
                    self.distances[i][sp_index] = float('inf')
                    sp_index = np.argmin(self.distances[i])
                    self.min_sp_indices[i] = sp_index
                    self.min_sp_distance[i] = self.distances[i][sp_index]


    def calculate_energy_fly(self, j):
        # calculate the energy consumption of the j-th UAV during flight
        T_fly = 0
        set_SPs = list(self.UAv[j])
        for s in range(len(set_SPs) - 1):
            start_point, end_point = set_SPs[s], set_SPs[s + 1]
            distance_fly = np.linalg.norm(np.array(self.SPs[start_point]) - np.array(self.SPs[end_point]))
            T_fly += distance_fly / self.velocity
        return self.p_ue * T_fly

    def calculate_energy_hov(self, j):
        # calculate the energy consumption of the j-th UAV during hovering
        T_hov = 0
        set_SPs = list(self.UAv[j])
        for s in set_SPs:
            T_hov += np.sum(self.a_ij[:, j] * self.D_i / self.r_ij[:, j])
        return self.p_hov * T_hov

    def calculate_energy(self):
        # calculate the total energy consumption
        energy = 0
        for j in range(self.num_uav):
            energy += self.calculate_energy_fly(j) + self.calculate_energy_hov(j)
        return energy

    def calculate_time(self):
        # calculate the total time consumption
        T_hov = np.sum(self.a_ij * self.D_i / self.r_ij)
        T_fly = 0
        for j in range(self.num_uav):
            set_SPs = list(self.UAv[j])
            for s in range(len(set_SPs) - 1):
                start_point, end_point = set_SPs[s], set_SPs[s + 1]
                distance_fly = np.linalg.norm(np.array(self.SPs[start_point]) - np.array(self.SPs[end_point]))
                T_fly += distance_fly / self.velocity
        return T_hov + T_fly

    def evaluate(self):
        # evaluate the total cost
        return self.gamma * self.calculate_energy() + self.calculate_time()

if __name__ == "__main__":
    UEs = [(250.9, 46.1), (676.8, 43.5), (116.4, 603.9), (190.9, 668.5), (917.4, 418.8), (332.3, 283.0), (186.3, 317.1),
           (481.2, 69.5), (705.0, 314.7), (745.3, 398.2), (608.2, 728.5), (421.8, 393.9), (232.2, 441.7),
           (373.0, 583.6), (100.0, 741.4), (83.2, 126.2), (322.9, 642.9), (999.5, 281.0), (582.2, 872.6),
           (789.3, 218.1), (346.6, 721.5), (353.9, 460.7), (244.4, 282.7), (826.3, 874.4), (142.8, 280.1),
           (525.2, 900.9), (602.5, 691.8), (282.6, 276.5), (156.3, 663.8), (942.8, 681.3), (863.0, 911.5),
           (815.3, 829.7), (27.1, 240.9), (266.3, 380.2), (479.3, 321.4), (437.1, 558.3), (393.7, 578.3),
           (378.1, 203.7), (364.2, 703.0), (737.3, 682.6), (100.2, 188.4), (515.0, 855.4), (32.6, 192.1),
           (829.6, 766.7), (526.6, 909.4), (434.9, 492.4), (483.7, 148.2), (562.7, 531.2), (885.1, 124.1),
           (58.9, 335.0), (645.1, 352.9), (361.6, 322.5), (170.1, 339.6), (563.0, 701.1), (808.9, 343.1),
           (760.2, 331.0), (249.4, 649.0), (410.4, 85.0), (586.4, 282.4), (223.0, 187.1), (983.1, 94.6), (408.9, 132.9),
           (44.4, 709.1), (856.9, 773.6), (761.2, 670.9), (92.0, 629.6), (944.2, 110.7), (149.8, 600.6), (14.6, 560.2),
           (32.2, 250.7), (290.0, 58.5), (364.1, 427.9), (231.6, 967.8), (740.3, 443.8), (497.8, 215.9), (722.0, 841.2),
           (31.3, 625.5), (891.1, 184.2), (72.5, 890.5), (528.3, 609.5), (690.6, 727.2), (625.5, 120.4), (737.9, 16.5),
           (3.3, 942.2), (568.6, 814.3), (87.9, 399.7), (564.7, 972.4), (384.4, 609.4), (91.9, 696.7), (728.8, 850.9),
           (740.8, 701.6), (145.5, 492.5), (342.3, 949.5), (202.1, 775.1), (250.1, 837.9), (438.0, 941.7),
           (660.3, 26.6), (136.2, 897.5), (287.6, 208.1), (734.3, 886.7)]
    UAv = [{0, 69}, {35, 67, 6, 70, 75, 77, 52, 58},
           {65, 71, 8, 9, 10, 11, 76, 13, 14, 15, 20, 85, 86, 23, 87, 24, 30, 94, 32, 97, 42, 51, 62}, {12, 53},
           {99, 17, 56, 25, 26, 91}, {39, 72, 41, 18, 83, 54, 55, 90, 61}, {88, 73, 19, 81}, {92, 22, 79},
           {66, 2, 7, 74, 28, 29}, {33, 34, 3, 36, 5, 45, 16, 82, 21, 95},
           {96, 1, 4, 37, 68, 40, 43, 44, 78, 46, 47, 59, 93}, {64, 50, 84}, {98, 57, 27, 60, 63}]
    SPs = [(374.5, 950.7, 100), (732.0, 598.7, 100), (156.0, 156.0, 100), (58.1, 866.2, 100), (601.1, 708.1, 100),
           (20.6, 969.9, 100), (832.4, 212.3, 100), (181.8, 183.4, 100), (304.2, 524.8, 100), (431.9, 291.2, 100),
           (611.9, 139.5, 100), (292.1, 366.4, 100), (456.1, 785.2, 100), (199.7, 514.2, 100), (592.4, 46.5, 100),
           (607.5, 170.5, 100), (65.1, 948.9, 100), (965.6, 808.4, 100), (304.6, 97.7, 100), (684.2, 440.2, 100),
           (122.0, 495.2, 100), (34.4, 909.3, 100), (258.8, 662.5, 100), (311.7, 520.1, 100), (546.7, 184.9, 100),
           (969.6, 775.1, 100), (939.5, 894.8, 100), (597.9, 921.9, 100), (88.5, 196.0, 100), (45.2, 325.3, 100),
           (388.7, 271.3, 100), (828.7, 356.8, 100), (280.9, 542.7, 100), (140.9, 802.2, 100), (74.6, 986.9, 100),
           (772.2, 198.7, 100), (5.5, 815.5, 100), (706.9, 729.0, 100), (771.3, 74.0, 100), (358.5, 115.9, 100),
           (863.1, 623.3, 100), (330.9, 63.6, 100), (311.0, 325.2, 100), (729.6, 637.6, 100), (887.2, 472.2, 100),
           (119.6, 713.2, 100), (760.8, 561.3, 100), (771.0, 493.8, 100), (522.7, 427.5, 100), (25.4, 107.9, 100),
           (31.4, 636.4, 100), (314.4, 508.6, 100), (907.6, 249.3, 100), (410.4, 755.6, 100), (228.8, 77.0, 100),
           (289.8, 161.2, 100), (929.7, 808.1, 100), (633.4, 871.5, 100), (803.7, 186.6, 100), (892.6, 539.3, 100),
           (807.4, 896.1, 100), (318.0, 110.1, 100), (227.9, 427.1, 100), (818.0, 860.7, 100), (7.0, 510.7, 100),
           (417.4, 222.1, 100), (119.9, 337.6, 100), (942.9, 323.2, 100), (518.8, 703.0, 100), (363.6, 971.8, 100),
           (962.4, 251.8, 100), (497.2, 300.9, 100), (284.8, 36.9, 100), (609.6, 502.7, 100), (51.5, 278.6, 100),
           (908.3, 239.6, 100), (144.9, 489.5, 100), (985.7, 242.1, 100), (672.1, 761.6, 100), (237.6, 728.2, 100),
           (367.8, 632.3, 100), (633.5, 535.8, 100), (90.3, 835.3, 100), (320.8, 186.5, 100), (40.8, 590.9, 100),
           (677.6, 16.6, 100), (512.1, 226.5, 100), (645.2, 174.4, 100), (690.9, 386.7, 100), (936.7, 137.5, 100),
           (341.1, 113.5, 100), (924.7, 877.3, 100), (257.9, 660.0, 100), (817.2, 555.2, 100), (529.7, 241.9, 100),
           (93.1, 897.2, 100), (900.4, 633.1, 100), (339.0, 349.2, 100), (726.0, 897.1, 100), (887.1, 779.9, 100)]

    calculate_fitness = Evaluate(UEs, SPs, UAv)
    fitness = calculate_fitness.evaluate()
    print("fitness = ", fitness)