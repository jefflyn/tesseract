import time
import tkinter as tk
from tkinter import messagebox

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("提醒计时器")

        self.label = tk.Label(root, text="设置提醒时间（分钟）：")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.insert(0, "5")
        self.entry.pack()

        self.start_button = tk.Button(root, text="开始计时", command=self.start_timer)
        self.start_button.pack()

        self.pause_button = tk.Button(root, text="暂停计时", command=self.pause_timer)
        self.pause_button.pack()
        self.pause_button.config(state=tk.DISABLED)  # 初始状态下禁用暂停按钮

        self.reset_button = tk.Button(root, text="重新设置", command=self.reset_timer)
        self.reset_button.pack()
        self.reset_button.config(state=tk.DISABLED)  # 初始状态下禁用重新设置按钮

        self.remaining_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.remaining_label.pack()

        self.end_time = 0
        self.paused = False
        self.minutes = 0
        self.update_clock()

    def start_timer(self):
        try:
            self.minutes = int(self.entry.get())
            self.set_timer(self.minutes)
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
        except ValueError:
            messagebox.showerror("错误", "请输入一个有效的整数分钟数。")

    def set_timer(self, minutes):
        self.paused = False
        self.end_time = time.time() + minutes * 60
        self.update_clock()

    def pause_timer(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="继续计时")
        else:
            self.pause_button.config(text="暂停计时")
            self.set_timer(self.minutes)

    def reset_timer(self):
        self.paused = True
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.remaining_label.config(text="")
        # self.entry.delete(0, tk.END)

    def update_clock(self):
        if not self.paused:
            current_time = time.time()
            remaining_time = self.end_time - current_time

            if self.minutes > 0 >= remaining_time:
                self.show_reminder()
            else:
                remaining_minutes = int(remaining_time // 60)
                remaining_seconds = int(remaining_time % 60)
                self.remaining_label.config(text=f"剩余时间：{remaining_minutes:02d}:{remaining_seconds:02d}")
                self.root.after(1000, self.update_clock)  # 每秒钟更新一次

    def show_reminder(self):
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title("提醒")
        label = tk.Label(reminder_window, text=f"{self.minutes}分钟已过，提醒时间到！", font=("Helvetica", 16))
        label.pack()
        close_button = tk.Button(reminder_window, text="关闭", command=reminder_window.destroy)
        close_button.pack()

def main():
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
