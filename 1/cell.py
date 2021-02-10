# 分裂
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
        self.before_a = self.now_a
        self.before_b = self.now_b
        return [self.now_a, self.now_b]


class Cell:
    def __init__(self, link_cells):
        self.energy = 0.35
        self.energy_max = 3  # 一分三合理么？ 0.35+0.35+2
        self.link_cells = link_cells

    def run(self):
        # for cell in self.link_cells:
        #     print(cell["strength"])
        if sum([cell["strength"] for cell in self.link_cells]) > 0.7:
            self._update_link()
        for cell in self.link_cells:
            state = cell["cell"].run()
            if state:
                cell["count"] += cell["strength"]
                self.energy -= cell["strength"]
        self._check_energy()
        # 前向传播（能量不足？）10:1等比例往下拆连接强度。
        if sum([cell["count"] for cell in self.link_cells]) > 0.7:
            self.energy -= 1
            if self.energy >= 1:
                self._update_strength(1)
            else:
                self._update_strength(self.energy)
            return True
        return False

    def _check_energy(self):
        if self.energy < 0:
            for cell in self.link_cells:

                cell["strength"] += (self.energy) / (10 * len(self.link_cells))
                self._check_link()

    def _check_link(self):
        for cell in self.link_cells:
            if cell["strength"] < 0:
                for cell_ in cell["cell"].link_cells:
                    self.link_cells.append(cell_)
                self.energy += cell["cell"].energy
                self.energy += 10 * cell["strength"]
                self.link_cells.remove(cell)
                self._check_energy()

    def eat(self, add_enargy):
        # 补齐能量 广度优先遍历
        if self.energy_max - self.energy <= add_enargy:
            add_enargy -= self.energy_max - self.energy
            self.energy = self.energy_max
        else:
            self.energy = add_enargy
            add_enargy = 0
        return [add_enargy, self.link_cells]

    def _update_strength(self, add_energy):
        # 将输进来的能量按激活比例转化到每个项上去。
        sum_count = sum([cell["count"] for cell in self.link_cells])
        for cell in self.link_cells:
            cell["strength"] += cell["count"] * add_energy / (10 * sum_count)
        # 置零
        for cell in self.link_cells:
            cell["count"] = 0

    def _update_link(self):
        if len(self.link_cells) > 2:
            self.energy -= 2.7
            self._check_energy()
            strength_sum = 0
            up_links = []
            down_links = []
            for cell in self.link_cells:
                if strength_sum < 0.35:
                    up_links.append(cell)
                else:
                    down_links.append(cell)
                strength_sum += cell["strength"]
            cell_up = Cell(up_links)
            cell_down = Cell(down_links)
            self.link_cells = [{"cell": cell_up, "strength": 0.1, "count": 0}, {"cell": cell_down, "strength": 0.1, "count": 0}]
        if len(self.link_cells) == 2:
            self.energy -= 2.7
            self._check_energy()
            up_links = []
            down_links = []
            up_links.append(self.link_cells[0])
            down_links.append(self.link_cells[1])
            cell_up = Cell(up_links)
            cell_down = Cell(down_links)
            self.link_cells = [{"cell": cell_up, "strength": 0.1, "count": 0}, {"cell": cell_down, "strength": 0.1, "count": 0}]
        if len(self.link_cells) == 1:
            self.energy -= 1.35
            self._check_energy()
            up_links = self.link_cells
            cell_up = Cell(up_links)
            self.link_cells = [{"cell": cell_up, "strength": 0.1, "count": 0}]


class Cell_input:
    def __init__(self):
        self.link_cells = []
        self.energy = 0
        self.state = False

    def run(self):
        if self.state:
            return True
        else:
            return False

    def input_info(self, info):
        self.state = info

    def eat(self, add_enargy):
        # 补齐能量 广度优先遍历
        return [add_enargy, []]


class Cell_output:
    def __init__(self, link_cells):
        self.state = False
        self.link_cells = [cell for cell in link_cells]

    def run(self):
        for cell in self.link_cells:
            self.state = cell["cell"].run()

    def output_info(self):
        if self.state:
            return True
        else:
            return False

    def eat(self, add_enargy):
        # 补齐能量 广度优先遍历
        return [add_enargy, self.link_cells]


def eat_(energy, cells_list):
    cells = [cell for cell in cells_list]
    while cells:
        infos = cells[0]["cell"].eat(energy)
        energy = infos[0]
        for cell in infos[1]:
            cells.append(cell)
        cells.pop(0)
    return energy


main_class = Main_class()
input_cells = [{"cell": Cell_input(), "strength": 0.1, "count": 0} for i in range(2)]
output_cells = [{"cell": Cell_output([{"cell": Cell(input_cells), "strength": 0.1, "count": 0}]), "strength": 0, "count": 0} for i in range(1)]
energy_sum = 100
energy_sum = eat_(energy_sum, output_cells)
done = 0
for i in range(1000):
    state_ = main_class.run()
    print(energy_sum)
    if done:
        print("开灯！！！")
        state_[0] = 1
        main_class.before_a = 1
        main_class.before_b = 0
        main_class.num = 0
    print(state_)
    if state_[0] == 1:
        energy_sum += 4
    for i in range(2):
        input_cells[i]["cell"].input_info(state_[i])
    for i in range(1):
        output_cells[i]["cell"].run()
    for i in range(1):
        done = output_cells[i]["cell"].output_info()
    energy_sum = eat_(energy_sum, output_cells)
