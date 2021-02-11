class Cell:
    def __init__(self, link_cells):
        self.state = False
        self.energy = 0.35
        self.energy_max = 3  # 一分三合理么？ 0.35+0.35+2
        self.link_cells = link_cells

    def run(self):
        # for cell in self.link_cells:
        #     print(cell["strength"])
        self.energy -= 0.01
        if sum([cell["strength"] for cell in self.link_cells]) > 0.7:
            self._update_link()
        for cell in self.link_cells:
            state = cell["cell"].ask_last_state()
            if state:
                cell["count"] += cell["strength"]
                self.energy -= cell["strength"]
        self._check_energy()
        # 前向传播（能量不足？）100:1等比例往下拆连接强度。
        if sum([cell["count"] for cell in self.link_cells]) > 0.7:
            self.energy -= 1
            if self.energy >= 1:
                self._update_strength(1)
            else:
                self._update_strength(self.energy)
            self.state = True
        else:
            self.state = False
        for cell in self.link_cells:
            state = cell["cell"].run()

    def ask_last_state(self):
        return self.state

    def _check_energy(self):
        if self.energy < 0:
            for cell in self.link_cells:
                cell["strength"] += (self.energy) / (100 * len(self.link_cells))
                self.energy = 0
                self._check_link()

    def _check_link(self):
        for cell in self.link_cells:
            if cell["strength"] < 0:
                for cell_ in cell["cell"].link_cells:
                    self.link_cells.append(cell_)
                self.energy += cell["cell"].energy
                self.energy += 100 * cell["strength"]
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
            cell["strength"] += cell["count"] * add_energy / (100 * sum_count)
        # 置零
        for cell in self.link_cells:
            cell["count"] = 0

    def _update_link(self):
        for cell in self.link_cells:
            self.energy += cell["count"]
            cell["count"] = 0
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
        pass

    def ask_last_state(self):
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