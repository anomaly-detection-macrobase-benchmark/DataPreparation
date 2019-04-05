import datetime
import itertools
import os

import matplotlib.pyplot as plt


def color_cycle():
    return itertools.cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])


def marker_cycle():
    return itertools.cycle(('+', '.', 'o', '*', 'v', 's', 'd', 'p'))


def save_plot(fig, name, dir, name_format='{dt}_{suptitle}_{name}', image_format='png'):
    fig.savefig(os.path.join(dir, name_format.format(
        dt=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        name=name,
        suptitle=fig._suptitle.get_text())) + '.' + image_format)
