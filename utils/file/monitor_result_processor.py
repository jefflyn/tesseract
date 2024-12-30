import pandas as pd

from zillion.utils import db_util


def extract_numbers(s):
    current_number = ""
    for char in s:
        if char.isdigit():
            current_number += char
    return int(current_number)


if __name__ == '__main__':
    with open('result.txt', 'r') as f:
        line = f.readline()
        result_list = []
        pt = ""
        while line:
            fields = line.split("，")
            if len(fields) < 2:
                pt = extract_numbers(fields[0])
                line = f.readline()
                continue
            category = fields[0]
            result_list.append([pt, category.split("_")[0].split(". ")[1], category.split("_")[1], extract_numbers(fields[2])])
            line = f.readline()
        result_df = pd.DataFrame(result_list,
                                 columns=['pt', 'category1', 'category2', 'count'])
        print(result_df)
        db_util.to_db(result_df, 'monitor_result', if_exists='append', db_name='test')
