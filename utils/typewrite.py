import random
import time

import emoji
import pyautogui

from utils.datetime import date_util

emoji_pool = list(emoji.EMOJI_DATA.keys())

story_text = "The cars would not stop for David. The cars would not stop or Julie. The father walked into the middle of the road. Looked at the cars and yeah stop. The car is all jumped up in the air. Ran around in a circle three times and went back up the street so fast they forgot their tires. Julian and David cross the street and went into a store. The man who ran the store didn't like serving kids. They waited five minutes 10 minutes 15 minutes then David's father came in. He looked at the storekeeper and said these kids are my friends man jumped up into the air ran around the store three times and gave David and Julie three boxes of ice cream 11 bags of potato chips and 19 lifesaver all for free Julian David walked down the street and went around the bin. There were six big kids from grade 8 standing in the middle of the sidewalk. They looked at they looked and they looked at the food then one big kid reached down and grabbed a box of ice cream. David's father came around the bin. He looked at the big kids and yeah beat it. They jumped right out of their shirts. They jumped right out of their pants and ran down the street in their underwear ran after them, but she slipped and scraped her elbow David's father picked her up and held her and he put a special giant bandage on her elbow. Julie said well David, you do have a very nice father after all but he is still kind of scary. Do you think he is scary? He said David wait till you meet my grandmother."
word_list = story_text.split(" ")

for i in range(0, 3):
    emoji_txt = ''
    for j in range(0, 400):
        em = emoji_pool[random.randint(0, len(emoji_pool) - 1)]
        emoji_txt = emoji_txt + em
    # print(emoji_txt)


def write():
    text = 'zzz zzz zzz'
    size = len(word_list)
    for i in range(0, 20000):
        # 模拟键盘输入 "Hello, World!"
        text = word_list[random.randint(0, size - 1)] if i > size - 1 else word_list[i]
        pyautogui.typewrite(text)
        # pyautogui.typewrite(word_list[random.randint(0, size - 1)])
        # 等待1秒
        # time.sleep(1)
        # 模拟键盘按键，例如按下回车键🀙🀚🀚🀛
        pyautogui.press('enter')


if __name__ == '__main__':
    begin_time = time.time()
    write()
    print(date_util.now(), time.time() - begin_time)
