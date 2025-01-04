import re
import string


def convert_2_text(file_name) :
    # 读取文本
    # 从文件中读取文本
    with open(file_name, 'r') as file:
        text = file.read()
    # 将文本转换为小写
    text = text.lower()

    # 转换为小写，去掉标点符号、数字和中文字符
    text = text.replace('\u00A0', ' ')
    text = re.sub(r'[^\x00-\x7f]', '', text)  # 去掉非ASCII字符（中文等）
    text = re.sub(r'\d+', '', text)  # 去掉数字
    text = text.translate(str.maketrans('', '', string.punctuation))  # 去掉标点符号
    text = re.sub(r'\s+', ' ', text)

    return text

def get_words(text):
    # 拆分成单词列表
    words = text.split()

    # 使用集合去重
    unique_words = set(words)

    word_list = list(unique_words)
    word_list.sort()
    return word_list
