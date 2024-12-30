from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import declarative_base

# 创建声明基类
Base = declarative_base()


class BasicA(Base):
    '''
    basic_a 表对应的 SQLAlchemy 模型
    '''
    __tablename__ = 'basic_a'
    # 表字段
    code = Column(String, primary_key=True)
    name = Column(String)
    industry = Column(String)
    list_date = Column(String)
    total_equity = Column(BigInteger)
    flow_equity = Column(BigInteger)
    total_capital = Column(BigInteger)
    flow_capital = Column(BigInteger)

    def __repr__(self):
        return f"<BasicA(code={self.code}, name={self.name})>"

    def __init__(self, code, name, industry, list_date, total_equity, flow_equity, total_cap, flow_cap):
        self.code = code
        self.name = name
        self.industry = industry
        self.list_date = list_date
        self.total_equity = total_equity
        self.flow_equity = flow_equity
        self.total_capital = total_cap
        self.flow_capital = flow_cap
