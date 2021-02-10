# [{"cell": cell_up, "strength": 0.1, "count": 0}, {"cell": cell_down, "strength": 0.1, "count": 0}]

import matplotlib.pyplot as plt
import time


def show(output_lists):
    lists_cells = [output_lists]
    i = 0
    while lists_cells:
        j = 0
        k = 0
        list_ = []
        for list_cells in lists_cells:
            energy = sum([cell["count"] for cell in list_cells])
            for cell in list_cells:
                print(cell)
                if energy >= 0.5:
                    plt.plot([j, k], [i, i + 1], 'ro-', linewidth=cell["strength"])  # red - r, green - g, blue - b
                elif energy >= 0.3:
                    plt.plot([j, k], [i, i + 1], 'go-', linewidth=cell["strength"])  # red - r, green - g, blue - b
                else:
                    plt.plot([j, k], [i, i + 1], 'bo-', linewidth=cell["strength"])  # red - r, green - g, blue - b
                k += 1
                list_.append(cell["cell"].link_cells)
            j += 1
        lists_cells = list_
        i += 1
    plt.show()
    time.sleep(1)
