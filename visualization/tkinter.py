import tkinter as tk


class Questions(tk.Tk):
    def __init__(self, *args, **kw):
        super().__init__()
        self.wm_title('CSSE1001 Queue')
        self.configure(background='white')
        self.wm_minsize(1440, 776)  # 设置窗口最小化大小
        self.wm_maxsize(1440, 2800)  # 设置窗口最大化大小
        self.resizable(width=False, height=True)  # 设置窗口宽度不可变，高度可变

        self.run()
        self.refresh_data()
        self.mainloop()

    def refresh_data(self):
        # 需要刷新数据的操作
        # 代码...

        self.after(10000, self.refresh_data)  # 这里的10000单位为毫秒

    def run(self):
        pass


if __name__ == '__main__':
    question = Questions()
