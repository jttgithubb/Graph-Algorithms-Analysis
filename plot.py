import matplotlib.pyplot as plt
from pathlib import Path
from benchmark import get_data_path
import pandas as pd
import numpy as np
from math import e
from sklearn.metrics import r2_score

OKABE_COLORS = ['#000000', '#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color= OKABE_COLORS)

FIGURE_DIRECTORY = Path('figures')
FIGURE_DIRECTORY.mkdir(exist_ok= True)

def plot(title: str, figure_name: str, save: bool):
    plt.title(title)
    if save:
        plt.savefig(FIGURE_DIRECTORY / figure_name, dpi= 300)
    plt.show()

def load_data(algorithm_name: str) -> dict[int, list[float]]:
    df = pd.read_csv(get_data_path(algorithm_name), sep= ' ', header= None)
    columns = ['size', 'res']
    df.columns = columns
    data_dict = {}
    for row in df.itertuples():
        if row.size not in data_dict:
            data_dict[row.size] = []
        data_dict[row.size].append(row.res)
    return data_dict

def load_avg_data(algorithm_name: str) -> dict[int, float]:
    data_dict = load_data(algorithm_name)
    avg_data_dict = {}
    for key in data_dict.keys():
        avg_data_dict[key] = sum(data_dict[key]) / float(len(data_dict[key]))
    return avg_data_dict

def add_to_plot(algorithm_name: str, skip: int = 0, skip_end=0):
    avg_data_dict = load_avg_data(algorithm_name)
    x = np.array(list(avg_data_dict.keys()))
    y = np.array(list(avg_data_dict.values()))
    n = len(x)
    print(x)
    x = x[skip:n-skip_end]
    y = y[skip:n-skip_end]
    xlog = np.log(x)
    m, b = np.polyfit(xlog, y, 1)
    fit = np.poly1d((m, b))
    expected_y = fit(xlog)
    r2 = r2_score(y, expected_y)
    p = plt.semilogx(x, y, '.', base= 2, label= f'{algorithm_name}: $y(n) \\approx {m: .5} \\log n + {b: .5}$, $R^2 = {r2: .5}$')
    p_fit =plt.semilogx(x, expected_y, '-', base= 2, color = p[-1].get_color())
    
if __name__ == '__main__':
    plt.figure(num= 1, figsize= (10, 6), facecolor= 'w', edgecolor= 'k')

    add_to_plot('get_diameter', 0)

    plt.legend(bbox_to_anchor=(0, 1), loc= 'upper left', fontsize= 9)
    plt.xlabel('Input size: (n, # of nodes)', fontsize= 12)
    plt.ylabel('Diameter: D(n)', fontsize= 12)
    plt.title('Diameter at Different Input Sizes N', fontsize= 16)
    plt.show()