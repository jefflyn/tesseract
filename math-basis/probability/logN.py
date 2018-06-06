import matplotlib
matplotlib.use('TkAgg')
# matplotlib.rcParams['font.sans-serif'] = 'SimHei'
import matplotlib.pyplot as plt
import numpy as np




if __name__ == '__main__':
    x_values = []
    y_values = []
    for i in range(1, 101):
        x_values.append(i)
        y = np.log10(i)
        y_values.append(y)
    plt.plot(x_values, y_values, 'r-', linewidth=2)
    plt.grid(True)
    plt.show()