import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = [float(i) / 100.0 for i in range(1,300)]
    y = [math.log(i) for i in x]

    print(x)
    print(y)

    plt.plot(x, y)
    plt.show()