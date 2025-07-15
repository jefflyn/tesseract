from utils.datetime.date_util import now
from word.dao.vocabulary_dao import VocabularyDAO
from zillion.db.DataSourceFactory import session_app


def upsert_vocabulary(word, lemma, pos, synsets):
    vocabulary_dao = VocabularyDAO(session_app)
    vocabulary = vocabulary_dao.get(word)
    if vocabulary is None :
        vocabulary_dao.add(word, lemma, pos, synsets, now())

import requests

def get_word_info(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code != 200:
        print("查询失败")
        return

    data = response.json()
    for phonetic in data[0].get("phonetics", []):
        print("音标：", phonetic.get("text"))
        print("音频：", phonetic.get("audio"))

    for meaning in data[0].get("meanings", []):
        for definition in meaning.get("definitions", []):
            print("定义：", definition.get("definition"))
            example = definition.get("example")
            if example:
                print("例句：", example)


if __name__ == '__main__':
    get_word_info("dog")