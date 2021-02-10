# 初遇

import random


class Main_class:
    def __init__(self):
        self.now_a = 0
        self.now_b = 0
        self.before_a = 0
        self.before_b = 0
        self.num = 0

    def run(self):
        self.now_a = 0
        self.now_b = 0
        if random.random() > 0.5:
            self.now_a = 1
        if self.before_a == 1:
            self.now_b = 1
        if self.num < 3 and self.num > 0:
            self.num += 1
            self.now_a = 0
        elif self.num == 3:
            self.num = 0
        if self.before_b == 1:
            self.num = 1
            self.now_a = 0
        print(self.now_a, self.now_b)
        self.before_a = self.now_a
        self.before_b = self.now_b
        return [self.now_a, self.now_b]


class Cell:
    def __init__(self):
        self.energy = 0
        self.energy_max = 2
        self.link = [0.1, 0.1]
        self.link_count = [0, 0]

    def run(self, a, b, e):
        # 前向传播（能量不足？）
        if a == 1:
            self.link_count[0] += self.link[0]
            self.energy -= self.link[0]
        if b == 1:
            self.link_count[1] += self.link[1]
            self.energy -= self.link[1]
        if sum(self.link_count) > 0.7:
            print("开灯！！！！")
            print(self.link)
            print(self.link_count)
            self._update_link(e)
            return 1
        return 0

    def ask_eat(self):
        # 做统计为eat函数的能量分配做打算。
        return self.energy_max - self.energy

    def eat(self, add_enargy):
        # 补齐能量
        self.energy += add_enargy

    def _update_link(self, add_energy):
        # 将输进来的能量按激活比例转化到每个项上去。
        self.link[0] += self.link_count[0] * add_energy / sum(self.link_count)
        self.link[1] += self.link_count[1] * add_energy / sum(self.link_count)
        # 置零
        self.link_count[0] = 0
        self.link_count[1] = 0


main_class = Main_class()
cell_0 = Cell()
energy_sum = 8
cell_0.eat(2)
done = 0
for i in range(100):
    state_ = main_class.run()
    if done == 1:
        state_[0] = 1
        main_class.before_a = 1
        main_class.before_b = 0
        main_class.num = 0

    if state_[0] == 1:
        energy_sum += 4
    done = cell_0.run(state_[0], state_[1], energy_sum/200)  # 不可能一次激活使用全部能量，这个位置还有一个逻辑需要完善，激活前的所有能量加值？或者引入能量浓度的概念。
    energy_need = cell_0.ask_eat()
    if energy_sum >= energy_need:
        energy_sum -= energy_need
        cell_0.eat(energy_need)
    else:
        energy_sum = 0
        cell_0.eat(energy_sum)  # 这里的个体死亡判定还有问题，没能量了可以考虑拆解最长未使用连接。
    if energy_sum == 0:
        print("!!!!!我死了!!!!!")
        break
