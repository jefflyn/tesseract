a = [12.2, 32.44]
print(a[:2])
for i in range(5):
    print(i)

print(str(a))

import os

print(os.environ['PYTHONPATH'])

wave_a = {10: [(11, -8), (15, -9), (19, -11)]}
a = wave_a.get(10)

import numpy as np
avg_a = np.mean([v[1] for v in a])
min_a = np.min([v[1] for v in a])
max_a = np.max([v[1] for v in a])

print(a)
print(min_a)
print(avg_a)
print(max_a)
