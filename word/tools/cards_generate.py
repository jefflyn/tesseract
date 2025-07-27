import os
import pandas as pd
import requests
from gtts import gTTS
from bs4 import BeautifulSoup

# words = ["apple", "cat", "jump", "tangible"]
# 修改为你的 CSV 文件路径
input_csv = "words.csv"
# 读取词表
df = pd.read_csv(input_csv, header=None, names=["word"])
# words = df.drop_duplicates().tolist()
words = df['word'].dropna().unique()
os.makedirs("audio", exist_ok=True)

def tts(text, filename):
    """
    mv ./**.mp3 /Users/linjingu/Library/Application\ Support/Anki2/Ryan/collection.media/
    """
    filepath = os.path.join("audio", filename)
    # filepath = "/Users/linjingu/Library/Application Support/Anki2/Ryan/collection.media/" + filename
    if not os.path.exists(filepath) and text.strip():
        tts = gTTS(text)
        tts.save(filepath)
    return f"[sound:{filename}]"

def get_meaning_and_example(word):
    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    print(url)
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    # print(soup.prettify())  # 或者
    # print("example", soup.select_one(".unx"))

    meaning = soup.select_one(".def").get_text(strip=True) if soup.select_one(".def") else ""
    example = soup.select_one(".unx").get_text(strip=True) if soup.select_one(".unx") else ""
    # 查找音标，牛津学习词典的音标通常在 <span class="phon"> 标签内
    # phonetics = soup.find_all("span", class_="phon")
    ipa = soup.select_one(".phon").get_text(strip=True) if soup.select_one(".phon") else ""
    # for phon in phonetics:
    #     print(phon.text.strip())
    return meaning, example, ipa

def dummy_image_url(word):
    return f"https://source.unsplash.com/160x160/?{word}"

from icrawler.builtin import GoogleImageCrawler
def download_google_image(word, save_dir="images"):
    os.makedirs(save_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": save_dir})
    crawler.crawl(keyword=word, max_num=1, file_idx_offset=0)
    # Rename image
    for fname in os.listdir(save_dir):
        if fname.lower().endswith(('.jpg', '.png')):
            os.rename(os.path.join(save_dir, fname), os.path.join(save_dir, f"{word}.jpg"))
            break
    print(f"Downloaded: {word}")


rows = []
total = len(words)
try:
    for word in words:
        meaning, example, ipa = get_meaning_and_example(word)
        print(word, "get_meaning_and_example:", meaning, example, ipa)
        # download_google_image(word)
        print(total - 1, word)
        total = total - 1

        image = f"<img src='{word}.jpg'>"
        sound_word = tts(word, f"{word}_sound.mp3")
        sound_meaning = tts(meaning, f"{word}_meaning.mp3")
        sound_example = tts(example, f"{word}_example.mp3")

        rows.append({
            "Word": word,
            "IPA": ipa,
            "Image": image,
            "Sound": sound_word,
            "Meaning": meaning,
            "Sound_Meaning": sound_meaning,
            "Example": example,
            "Sound_Example": sound_example
        })
except Exception as e:
    print("error", e)

df = pd.DataFrame(rows)
df.to_csv("_cards.csv", index=False, header=None, encoding="utf-8-sig")
print("已生成 anki_word_cards.csv 和音频文件夹 audio/")
