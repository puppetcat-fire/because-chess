class Cell:
    def __init__(self, link_cells, energy):
        self.energy_max = 3  # 一分三合理么？ 0.35+0.35+2
        self.survival_time = 0
        self.state = False

        
        self.energy = energy
        self.link_cells = link_cells
        # [{"cell": cell_0, "weight": 0.3, "count_after_last_activation": 3, "count_after_birth": 20},
        #  {"cell": cell_1, "weight": 0.5, "count_after_last_activation": 2, "count_after_birth": 15}]
        # count_after_birth一定小于survival_time
    def run(self):
        # 第一，活着是需要扣能量的。每个细胞能承载的信息是有限的，而更多的细胞能承载更多的信息，但是从环境中摄取的能量却是有限的，而受此影响，精简出来的结构就是确定的。
        self.energy -= 0.01
        self.survival_time += 1
        # 第二，检查是否需要新建连接？
        if sum([cell["count_after_birth"]/self.survival_time for cell in self.link_cells]) > 1:
            self._update_link()
        # 第三，前向传播？将上一轮得到数据向后传递至输出，在这里有一个延迟性，我觉得很重要，但是还没有一个比较好的系统帮我把这个延迟性的功能使用起来。
        # 并且承载信息是要消耗能量的，接收到1的信息，就需要1的能量。
        for cell in self.link_cells:
            state = cell["cell"].ask_last_state()
            if state:
                cell["count"] += cell["strength"]
                self.energy -= cell["strength"]
        # 第四，检查前向传播后的能量情况，会倾向于将当前的连接减少至断开，而确保本次信息的传输成功。但是会有一个bug，就是跟分裂的联动（0.0.3），会导致在一开始的时候无限向上分裂，然后导致能量不足，断开与输入端的连接。
        self._check_energy()
        # 第五，累加更新自己状态。
        if sum([cell["count"] for cell in self.link_cells]) > 0.7:
            self.energy -= 1
            if self.energy >= 1:
                self._update_strength(1)
            else:
                self._update_strength(self.energy)
            self.state = True
        else:
            self.state = False
        # 第六，递归调用前向细胞。
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