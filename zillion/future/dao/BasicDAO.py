from zillion.db.DataSourceFactory import session_future
from zillion.future.domain.basic import Basic


class BasicDAO:
    def __init__(self, session):
        self.session = session

    def get_all_basic(self):
        return self.session.query(Basic).all()

    def get_basic_by_symbol(self, symbol) -> Basic:
        return self.session.query(Basic).filter(Basic.symbol == symbol).first()
    #
    # def add_user(self, name, email):
    #     new_user = User(name=name, email=email)
    #     self.session.add(new_user)
    #     self.session.commit()
    #     return new_user
    #
    # def update_user_email(self, user_id, new_email):
    #     user = self.get_user_by_id(user_id)
    #     if user:
    #         user.email = new_email
    #         self.session.commit()
    #     return user
    #
    # def delete_user(self, user_id):
    #     user = self.get_user_by_id(user_id)
    #     if user:
    #         self.session.delete(user)
    #         self.session.commit()
    #     return user

if __name__ == '__main__':
    basic = BasicDAO(session_future)
    a = basic.get_basic_by_symbol('A')
    print(a.name)