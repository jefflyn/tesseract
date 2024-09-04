
# 从文件中读取文本
with open('temp.txt', 'r') as file:
    lines = file.readlines()
    total = 0
    for line in lines:
        clean_line = line.rstrip('\n')
        txt_arr = clean_line.split('符合条件数量=')
        if len(txt_arr) > 1:
            part2 = txt_arr[len(txt_arr) - 1]
            total = total + int(part2)
            print(part2)
    print(total)

