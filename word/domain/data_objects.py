from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

# 创建声明基类
Base = declarative_base()


class Vocabulary(Base):
    '''
    vocabulary 表对应的 SQLAlchemy 模型 e.g. vocabulary_xxx
    '''
    __tablename__ = 'vocabulary'
    # 表字段
    word = Column(String, primary_key=True)
    lemma = Column(String)
    pos = Column(String)
    synsets = Column(String)
    update_time = Column(DateTime)

    def __repr__(self):
        return f"<Vocabulary(word={self.word})>"

    def __init__(self, word, lemma, pos, synsets, update_time):
        self.word = word
        self.lemma = lemma
        self.pos = pos
        self.synsets = synsets
        self.update_time = update_time
