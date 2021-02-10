# 暂停,显示
import random
from Cell.cell import Cell, Cell_input, Cell_output
from show.showmaker import show


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
output_cells = [{"cell": Cell_output([{"cell": Cell(input_cells), "strength": 0.1, "count": 0}]), "strength": 1, "count": 0} for i in range(1)]
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
    show(output_cells)
