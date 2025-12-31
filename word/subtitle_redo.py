import os

import pysrt


def merge_srt_files(folder_path, output_file):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹 {folder_path} 不存在")
        return

    # 打开输出文件以写入模式
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 遍历文件夹中的所有文件
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.srt') and filename.startswith('1'):
                outfile.write('<div style="text-align: center;">')
                outfile.write('<h3>  ' + filename + '</h3>')
                file_path = os.path.join(folder_path, filename)
                try:
                    # with open(file_path, 'r', encoding='utf-8') as infile:
                    subs = pysrt.open(file_path, encoding='utf-8')
                    # content = infile.read()
                    for sub in subs:
                        # print(f"[{sub.index}] {sub.start} --> {sub.end}")
                        # print(sub.text)
                        # print()
                        outfile.write('  ' + sub.text + '<br>')
                    print(f"已处理文件: {filename}")
                except Exception as e:
                    print(f"读取文件 {filename} 时出错: {e}")
                outfile.write('</table></div>')

# 示例用法
folder_path = '/Users/linjingu/Movies/King of The Hill/'  # 替换为你的文件夹路径
output_file = 'S01.html'  # 输出文件名
merge_srt_files(folder_path, output_file)


