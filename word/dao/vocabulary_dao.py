from utils.datetime.date_util import now
from word.domain.data_objects import Vocabulary


class VocabularyDAO:
    def __init__(self, session):
        self.session = session

    def get(self, word) -> Vocabulary:
        return self.session.query(Vocabulary).filter(Vocabulary.word == word).first()

    def add(self, word, lemma, pos, synsets, update_time):
        voc = Vocabulary(word=word, lemma=lemma, pos=pos, synsets=synsets, update_time=update_time)
        self.session.add(voc)
        self.session.commit()
        return voc

    def update(self, word, lemma, pos, synsets):
        voc = self.get(word)
        if voc:
            voc.lemma = lemma
            voc.pos = pos
            voc.synsets = synsets
            voc.update_time = now()
            self.session.commit()
        return voc

    def delete(self, word):
        voc = self.get(word)
        if voc:
            self.session.delete(voc)
            self.session.commit()
        return voc
