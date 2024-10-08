from numpy.random import randint


def multiple(a, b, c):
    return a * b + c

if __name__ == '__main__':
    for index in range(1, 100000001):
        a = randint(10)
        b = randint(10)
        c = randint(10)
        print(str(index), str(a) + '*' + str(b) + '+' + str(c) + '=', str(multiple(a,b,c)))