# 转换为小写，去掉标点符号，并拆分成单词列表

from googletrans import Translator

from nlp import spacy_nlp
from nlp.nltk_wordnet import get_synset
from utils.datetime import date_util
from word import text_util
from word.service.vocabulary_service import upsert_vocabulary
from zillion.utils import db_util

# 建立数据库连接
db = db_util.get_db("app")
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

# 初始化翻译器
translator = Translator()

text = text_util.convert_2_text('data_ryan.txt')

word_map = spacy_nlp.get_token_map(text)
print('total words:', len(word_map.keys()))

for word in word_map.keys():
    word_token = word_map[word]
    upsert_vocabulary(word, word_token['lemma'], word_token['pos'], get_synset(word))
    if word_token['pos'] == 'PUNCT':
        print(word, '标点符号跳过')
        continue
    df = db_util.read_sql('app', 'SELECT * FROM vocabulary_ryan WHERE word = :wd', params={'wd': word})
    if df is None or df.empty:
        sql = ("INSERT INTO vocabulary_ryan(word, count_times, update_time) VALUES ('%s', %d,'%s')"
               % (word, 1, date_util.now()))
    else:
        cnt = df.at[0, 'count_times']
        sql = "UPDATE vocabulary_ryan SET count_times=%d, update_time='%s' WHERE WORD='%s'" % (cnt + 1, date_util.now(), word)
    print(sql)
    cursor.execute(sql)
    db.commit()
