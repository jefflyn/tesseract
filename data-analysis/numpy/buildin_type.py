D = {'x': 1, 'y': 2, 'z': 3}  # 方法一
for key in D:
    print(D[key])

for key, value in D.items():  # 方法二  
    print(key)
    print(value)

iter = iter(D.keys())
for item in iter:  # 方法三
    print(item)

for value in D.values():  # 方法四  
    print(value)



