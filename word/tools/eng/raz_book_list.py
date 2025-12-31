import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

import requests

def check_robots(domain="https://www.raz-kids.com"):
    url = domain.rstrip("/") + "/robots.txt"
    r = requests.get(url, timeout=10)
    print("status:", r.status_code)
    print(r.text[:1000])  # 打印前1000字符，查看是否有禁止规则



def get_book_list():
    url = f"https://www.raz-kids.com/main/BookDetail/id/66/from/quizroom/languageId/1"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    print(soup.prettify())
    subtitle = '.bookInfo marginB2 sm subtle'
    meaning = soup.select_one(".bookInfo marginB2 sm subtle").get_text(strip=True) if soup.select_one(".bookInfo marginB2 sm subtle") else ""
    example = soup.select_one(".unx").get_text(strip=True) if soup.select_one(".unx") else ""
    print("hey:", meaning)
    return []


if __name__ == '__main__':
    check_robots("https://www.raz-kids.com")
    # get_book_list()
