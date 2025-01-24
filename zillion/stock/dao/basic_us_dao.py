from zillion.stock.db_stock import db_manager


class BasicUsDAO:
    # 构造方法（初始化方法）
    def __init__(self, code, name, selected):
        self.code = code
        self.name = name
        self.selected = selected

    # 实例方法
    def is_selected(self):
        return self.selected == 1

    @staticmethod
    def get_selected_codes():
        code_list = db_manager.query("select code from basic_us_selected where selected=1")
        return [item[0] for item in code_list]


if __name__ == '__main__':
    a = BasicUsDAO.get_selected_codes()
    print(a)