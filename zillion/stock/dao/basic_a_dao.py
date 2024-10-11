from zillion.stock.domain.data_object import BasicA


class BasicADAO:
    def __init__(self, session):
        self.session = session

    def get_by_code(self, code) -> BasicA:
        return self.session.query(BasicA).filter(BasicA.code == code).first()

    def get_all(self):
        return self.session.query(BasicA).all()

    def add(self, code, name, industry, list_date, total_equity, flow_equity, total_cap, flow_cap):
        new_basic = BasicA(code=code, name=name, industry=industry, list_date=list_date,
                           total_equity=total_equity, flow_equity=flow_equity, total_capital=total_cap, flow_capital=flow_cap)
        self.session.add(new_basic)
        self.session.commit()
        return new_basic

    def update(self, code, name, total_cap, flow_cap):
        basic = self.get_by_code(code)
        if basic:
            basic.name = name
            basic.total_capital = total_cap
            basic.flow_capital = flow_cap
            self.session.commit()
        return basic

    def delete(self, code):
        basic = self.get_by_code(code)
        if basic:
            self.session.delete(basic)
            self.session.commit()
        return basic
