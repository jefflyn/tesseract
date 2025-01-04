from utils.datetime.date_util import now
from word.dao.vocabulary_dao import VocabularyDAO
from zillion.db.DataSourceFactory import session_app


def upsert_vocabulary(word, lemma, pos, synsets):
    vocabulary_dao = VocabularyDAO(session_app)
    vocabulary = vocabulary_dao.get(word)
    if vocabulary is None :
        vocabulary_dao.add(word, lemma, pos, synsets, now())
