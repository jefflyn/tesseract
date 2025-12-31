import os
import re


def rename_by_order(folder_path):
    """
    基础版：批量顺序重命名
    :param folder_path: 文件夹路径
    :return:
    """
    for index, filename in enumerate(os.listdir(folder_path), start=1):
        old_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1]  # 获取扩展名
        new_filename = f"file_{index}{ext}"
        new_path = os.path.join(folder_path, new_filename)
        print(f"{filename} → {new_filename}")
        os.rename(old_path, new_path)

    print("✅ 重命名完成！")


def rename_by_rules(folder_path, param):
    """
    按规则替换字符串
    :param folder_path: 文件夹路径
    :return:
    """
    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)
        sub_str = "[" + param + "].pdf"
        new_filename = filename.replace("_", "").replace(".pdf", sub_str)
        new_path = os.path.join(folder_path, new_filename)
        print(f"{filename} → {new_filename}")
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            print("")

    print("✅ 批量清理命名完成！")


def rename_by_regex(folder_path):
    """
    正则重命名（更复杂规则）
    :param folder_path: 文件夹路径
    :return:
    """
    folder_path = "/path/to/your/folder"

    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)
        # 示例：把 "IMG_20231017.jpg" → "2023-10-17.jpg"
        new_filename = re.sub(r"IMG_(\d{4})(\d{2})(\d{2})", r"\1-\2-\3", filename)
        new_path = os.path.join(folder_path, new_filename)
        print(f"{filename} → {new_filename}")
        os.rename(old_path, new_path)

    print("✅ 正则重命名完成！")


if __name__ == '__main__':
    for l in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
        rename_by_rules("/Users/linjingu/Documents/Ryan/English/经典分级阅读RAZ点读版/RAZ绘本PDF点读版/" + l + ".PDF/", l)