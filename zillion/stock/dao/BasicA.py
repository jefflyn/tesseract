from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base


class BasicA(declarative_base()):
    __tablename__ = 'basic_a'  # 这表明这个类映射到名为 'basic_a' 的表
    code = Column(String, primary_key=True)
    column_name = Column(String)

    name = ''
    industry = ''
    list_date = ''
    total_equity = 0
    flow_equity = 0

    def __init__(self, code, name, industry, list_date, total_equity, flow_equity):
        self.code = code
        self.name = name
        self.industry = industry
        self.list_date = list_date
        self.total_equity = total_equity
        self.flow_equity = flow_equity




