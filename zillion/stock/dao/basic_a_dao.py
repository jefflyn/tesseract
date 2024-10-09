from zillion.stock.domain.data_object import BasicA


class BasicADAO:
    def __init__(self, session):
        self.session = session

    def get_by_code(self, code) -> BasicA:
        return self.session.query(BasicA).filter(BasicA.code == code).first()

    def get_all(self):
        return self.session.query(BasicA).all()

    def add(self, code, name, industry, list_date, total_equity, flow_equity):
        new_basic = BasicA(code=code, name=name, industry=industry, list_date=list_date,
                           total_equity=total_equity, flow_equity=flow_equity)
        self.session.add(new_basic)
        self.session.commit()
        return new_basic

    def update_name(self, code, name):
        basic = self.get_by_code(code)
        if basic:
            basic.name = name
            self.session.commit()
        return basic

    def delete(self, code):
        basic = self.get_by_code(code)
        if basic:
            self.session.delete(basic)
            self.session.commit()
        return basic
