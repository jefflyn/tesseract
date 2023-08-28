import tkinter as tk
from tkinter import ttk

import requests
import yfinance as yf


class StockQuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("港美股实时行情查询")

        self.label = ttk.Label(root, text="输入股票代码（多只股票用逗号分隔）:")
        self.label.pack()

        self.entry = ttk.Entry(root)
        self.entry.pack()

        self.button = ttk.Button(root, text="查询", command=self.get_stock_quote)
        self.button.pack()

        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("symbol", "open", "high", "low", "close", "volume")
        self.tree.heading("symbol", text="股票代码", command=lambda: self.sort_column("symbol"))
        self.tree.heading("open", text="开盘价", command=lambda: self.sort_column("open"))
        self.tree.heading("high", text="最高价", command=lambda: self.sort_column("high"))
        self.tree.heading("low", text="最低价", command=lambda: self.sort_column("low"))
        self.tree.heading("close", text="收盘价", command=lambda: self.sort_column("close"))
        self.tree.heading("volume", text="交易量", command=lambda: self.sort_column("volume"))
        self.tree.pack()

        self.refresh()

    def get_stock_quote(self):
        stock_codes = self.entry.get().split(',')
        data = []

        for stock_code in stock_codes:
            if stock_code.startswith("HK"):
                quote = self.get_hk_stock_quote(stock_code)
            else:
                stock = yf.Ticker(stock_code)
                quote = stock.history(period="1d")

            data.extend(quote.itertuples())

        self.show_result(data)

    def get_hk_stock_quote(self, stock_code):
        # 假设使用一个示例的港股行情API，实际中需要替换为真实的API地址
        api_url = f"https://example.com/hk_stock_quote?symbol={stock_code}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return [data]  # 假设API返回的数据是一个字典，将其放入列表中
        else:
            return []

    def show_result(self, data):
        self.tree.delete(*self.tree.get_children())  # 清空现有数据

        for entry in data:
            self.tree.insert("", "end", values=(entry.Index.strftime('%Y-%m-%d'), round(entry.Open, 2),
                                                round(entry.High, 2), round(entry.Low, 2),
                                                round(entry.Close, 2), round(entry.Volume, 2)))

    def sort_column(self, col):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children("")]
        data.sort(reverse=False)  # 设置为True可实现降序排序
        for index, (val, child) in enumerate(data):
            self.tree.move(child, "", index)

    def refresh(self):
        self.get_stock_quote()
        self.root.after(3000, self.refresh)  # 每隔3秒刷新页面

if __name__ == "__main__":
    root = tk.Tk()
    app = StockQuoteApp(root)
    root.mainloop()
