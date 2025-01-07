# 转换为小写，去掉标点符号，并拆分成单词列表

from googletrans import Translator

from nlp import spacy_nlp
from nlp.nltk_wordnet import get_synset
from utils.datetime import date_util
from word import text_util
from word.service.vocabulary_service import upsert_vocabulary
from word.text_util import get_words, contains_punctuation
from zillion.utils import db_util

# 建立数据库连接
db = db_util.get_db("app")
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

# 初始化翻译器
# translator = Translator()

def add_vocabulary():
    text = text_util.convert_2_text('word_stat_ryan.txt')
    word_map = spacy_nlp.get_token_map(text)
    print('total words:', len(word_map.keys()))

    for word in word_map.keys():
        word_token = word_map[word]
        upsert_vocabulary(word, word_token['lemma'], word_token['pos'], get_synset(word))


def ryan_data():
    text = text_util.convert_2_text('word_stat_ryan.txt')
    word_map = spacy_nlp.get_token_map(text)
    print('total words:', len(word_map.keys()))
    add_count =  0
    update_count = 0
    for word in word_map.keys():
        word_token = word_map[word]
        upsert_vocabulary(word, word_token['lemma'], word_token['pos'], get_synset(word))
        if word_token['pos'] in ['PUNCT', 'SYM', 'X'] or contains_punctuation(word):
            print(word, '标点符号或其他符号 跳过')
            continue
        df = db_util.read_sql('app', 'SELECT * FROM vocabulary_ryan WHERE word = :wd', params={'wd': word})
        if df is None or df.empty:
            create_time = date_util.now()
            sql = ("INSERT INTO vocabulary_ryan(word, count_times, create_time, update_time) VALUES ('%s', %d, '%s', '%s')"
                   % (word, 1, create_time, create_time))
            add_count = add_count + 1
        else:
            cnt = df.at[0, 'count_times']
            sql = "UPDATE vocabulary_ryan SET count_times=%d, update_time='%s' WHERE WORD='%s'" % (cnt + 1, date_util.now(), word)
            update_count  = update_count + 1
        print(sql)
        cursor.execute(sql)
        db.commit()
    print('add_count:', add_count, 'update_count:', update_count)

if __name__ == '__main__':
    ryan_data()

