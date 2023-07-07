import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg

def generatePgColormap(cm_name):
    pltMap = plt.get_cmap(cm_name)
    colors = pltMap.colors
    colors = [c + [1.] for c in colors]
    positions = np.linspace(0, 1, len(colors))
    pgMap = pg.ColorMap(positions, colors)

    return pgMap


def customColormap():
    colors_ = [(i, i, i) for i in range(84, 255)]
    pos = np.linspace(0, 1, len(colors_))

    return colors_, pos