import itertools
import matplotlib.pyplot as plt


def color_cycle():
    return itertools.cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])


def marker_cycle():
    return itertools.cycle(('+', '.', 'o', '*', 'v', 's', 'd', 'p'))
