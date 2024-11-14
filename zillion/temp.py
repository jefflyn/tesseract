from numpy.random import randint


def multiple(a, b, c):
    return a * b + c


if __name__ == '__main__':
    for index in range(1, 10001):
        a = randint(100)
        b = randint(100)
        c = randint(100)
        print(str(index), str(a) + '*' + str(b) + '+' + str(c) + '=', str(multiple(a,b,c)))