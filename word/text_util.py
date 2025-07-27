import re

from nlp import spacy_nlp

def text_from_file(file_name) :
    # 从文件中读取文本
    with open(file_name, 'r') as file:
        content = file.read()
    text = re.sub(r'[^\x00-\x7f]', '', content)  # 去掉非ASCII字符（中文等）
    text = re.sub(r'\d+', '', text)  # 去掉数字
    text = re.sub(r'[\s\n]+', ' ', text) # 去掉多余的空格

    return text

def contains_punctuation(word):
    # 正则表达式匹配任意标点符号
    pattern = r'[^\w\s]'
    return bool(re.search(pattern, word))

def convert_2_text(file_name) :
    # 读取文本
    # 从文件中读取文本
    with open(file_name, 'r') as file:
        text = file.read()
    # 将文本转换为小写
    # text = text.lower()

    # 转换为小写，去掉标点符号、数字和中文字符
    text = text.replace('\u00A0', ' ')
    text = re.sub(r'[^\x00-\x7f]', '', text)  # 去掉非ASCII字符（中文等）
    # text = re.sub(r'\d+', '', text)  # 去掉数字
    # text = text.translate(str.maketrans('', '', string.punctuation))  # 去掉标点符号
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


import spacy

# 加载英文模型
nlp = spacy.load("en_core_web_sm")

def extract_unique_words(text):
    doc = nlp(text)
    results = set()

    # 1. 先收集所有命名实体（专有名词），直接加入结果
    named_entities = set()
    drop_entities = set()
    for ent in doc.ents:
        print(f"{ent.text} is a {ent.label_}")
        if ent.label_ in ['GPE', 'LOC', 'LANGUAGE']:
            named_entities.add(ent.text)
        if ent.label_ in ['PERSON', 'ORG', 'PRODUCT']:
            drop_entities.add(ent.text)
    if len(named_entities) > 0 or len(drop_entities) > 0:
        for ent in named_entities:
            text = text.replace(ent, '')
        for ent in drop_entities:
            text = text.replace(ent, '')
        doc = nlp(text)
    # 2. 再收集非专有名词的普通单词
    for token in doc:

        if token.is_alpha and not token.ent_type_:  # 非实体单词
            results.add(token.text.lower())  # 小写化避免重复
        elif token.text in named_entities:
            results.add(token.text)  # 保留命名实体原样（保留大小写）

    return results



if __name__ == '__main__':
    # text = convert_2_text('test.txt')
    # word_map = spacy_nlp.get_token_map(text)
    # print(word_map)
    text = text_from_file('test.txt')
    print(extract_unique_words(text))