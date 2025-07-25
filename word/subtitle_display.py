import pysrt

# 加载 .srt 文件
subs = pysrt.open('demo.srt', encoding='utf-8')

# 遍历字幕条目
for sub in subs:
    # print(f"[{sub.index}] {sub.start} --> {sub.end}")
    print(sub.text)
    print()
