import random
import time

import emoji
import pyautogui

from utils.datetime import date_util

emoji_pool = list(emoji.EMOJI_DATA.keys())
for i in range(0, 3):
    emoji_txt = ''
    for j in range(0, 400):
        em = emoji_pool[random.randint(0, len(emoji_pool) - 1)]
        emoji_txt = emoji_txt + em
    # print(emoji_txt)


def write():
    text = 'zzz zzz zzz'
    for i in range(0, 200):
        # 模拟键盘输入 "Hello, World!"
        pyautogui.typewrite(text)
        # 等待1秒
        # time.sleep(1)
        # 模拟键盘按键，例如按下回车键🀙🀚🀚🀛
        pyautogui.press('enter')


if __name__ == '__main__':
    begin_time = time.time()
    write()
    print(date_util.now(), time.time() - begin_time)
