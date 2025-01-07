# 转换为小写，去掉标点符号，并拆分成单词列表

from nlp import spacy_nlp
from nlp.nltk_wordnet import get_synset
from word import text_util
from word.service.vocabulary_service import upsert_vocabulary
from zillion.utils import db_util

# 建立数据库连接
db = db_util.get_db("app")
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

text = text_util.convert_2_text('add_word.txt')
word_map = spacy_nlp.get_token_map(text)
print('total words:', len(word_map.keys()))

for word in word_map.keys():
    word_token = word_map[word]
    upsert_vocabulary(word, word_token['lemma'], word_token['pos'], get_synset(word))
