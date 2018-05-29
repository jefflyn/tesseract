import matplotlib
matplotlib.use('TkAgg')
# matplotlib.rcParams['font.sans-serif'] = 'SimHei'
import matplotlib.pyplot as plt


def first_digital(x):
    # OverflowError: int too large to convert to float
    # while x >= 10:
    #     x /= 10.0
    digit = str(x)[0]
    return int(digit)


if __name__ == '__main__':
    n = 1
    frequency = [0] * 9
    for i in range(1, 10001):
        n *= i
        m = first_digital(n) - 1
        frequency[m] += 1
        # print(m)
    print(frequency)
    plt.plot(range(1, 10), frequency, 'r-', linewidth=2)
    plt.plot(range(1, 10), frequency, 'go', markersize=8)
    plt.grid(True)
    plt.show()