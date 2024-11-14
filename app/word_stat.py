# 转换为小写，去掉标点符号，并拆分成单词列表
import re
import string

from googletrans import Translator

from utils.datetime import date_util
from zillion.utils import db_util

# 建立数据库连接
db = db_util.get_db("test")
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

# 初始化翻译器
translator = Translator()

# 读取文本
text = """
This is a sample text with several words. This text has some repeated words, and it also has unique words.
"""

# 从文件中读取文本
with open('data.txt', 'r') as file:
    text = file.read()

# 将文本转换为小写
text = text.lower()

# 转换为小写，去掉标点符号、数字和中文字符
text = text.replace('\u00A0', ' ')
text = re.sub(r'[^\x00-\x7f]', '', text)  # 去掉非ASCII字符（中文等）
text = re.sub(r'\d+', '', text)  # 去掉数字
text = text.translate(str.maketrans('', '', string.punctuation))  # 去掉标点符号

# 拆分成单词列表
words = text.split()

# 使用集合去重
unique_words = set(words)

word_list = list(unique_words)
word_list.sort()
print(word_list)

# 统计去重单词数
unique_word_count = len(unique_words)

print(f"去重单词数: {unique_word_count}")

for w in word_list:
    df = db_util.read_sql('test', 'SELECT * FROM word_stat WHERE word = :wd', params={'wd': w})
    if df is None or df.empty:
        zh_cn = translator.translate(w, src='en', dest='zh-cn').text
        print(w, zh_cn)
        sql = ("INSERT INTO word_stat(word, zh_cn, count, update_time) VALUES ('%s','%s', %d,'%s')"
               % (w, zh_cn, 1, date_util.now()))
    else:
        cnt = df.at[0, 'count']
        sql = "UPDATE word_stat SET count=%d, update_time='%s' WHERE WORD='%s'" % (cnt + 1, date_util.now(), w)
    cursor.execute(sql)

    db.commit()
