# [{"cell": cell_up, "strength": 0.1, "count": 0}, {"cell": cell_down, "strength": 0.1, "count": 0}]

import matplotlib.pyplot as plt


def show(output_lists, energy_sum):
    plt.title(energy_sum, fontsize=12, color='r')
    lists_cells = [output_lists]
    i = 0
    while lists_cells:
        j = 0
        k = 0
        list_ = []
        for list_cells in lists_cells:
            for cell in list_cells:
                energy = sum([cell_up["count"] for cell_up in cell["cell"].link_cells])
                for cell_up in cell["cell"].link_cells:
                    print(cell_up)
                    if energy >= 0.5:
                        plt.plot([j, k], [i, i + 1], 'ro-', linewidth=cell_up["strength"]*10)  # red - r, green - g, blue - b
                    elif energy >= 0.3:
                        plt.plot([j, k], [i, i + 1], 'go-', linewidth=cell_up["strength"]*10)  # red - r, green - g, blue - b
                    else:
                        plt.plot([j, k], [i, i + 1], 'bo-', linewidth=cell_up["strength"]*10)  # red - r, green - g, blue - b
                    k += 1
                list_.append(cell["cell"].link_cells)
                j += 1
        lists_cells = list_
        i += 1
    plt.pause(0.1)
    plt.clf()
    # plt.close()
