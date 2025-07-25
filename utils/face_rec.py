import os
import face_recognition
import cv2
import pandas as pd
from collections import defaultdict

# 路径配置
known_dir = "known_faces"  # 已知人物人脸库
photo_dir = "photos"       # 待分析照片
result = defaultdict(dict)

# 1. 加载人脸库
known_encodings = []
known_names = []

for file in os.listdir(known_dir):
    img_path = os.path.join(known_dir, file)
    image = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(image)
    if encodings:
        known_encodings.append(encodings[0])
        known_names.append(os.path.splitext(file)[0])  # 文件名作为人物名

# 2. 遍历照片
for photo_name in os.listdir(photo_dir):
    photo_path = os.path.join(photo_dir, photo_name)
    image = face_recognition.load_image_file(photo_path)

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    seen_names = set()
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
        for i, match in enumerate(matches):
            if match:
                name = known_names[i]
                seen_names.add(name)

    # 统计每人是否出现在该图中
    for name in known_names:
        result[name][photo_name] = int(name in seen_names)

# 3. 转为 DataFrame 输出
df = pd.DataFrame(result).T  # 行为人物，列为照片
print(df)

# 可保存为 Excel 或 CSV
df.to_excel("face_count.xlsx")
