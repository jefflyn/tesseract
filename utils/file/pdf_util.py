import os
import pikepdf

def unlock_pdf(file_path):
    try:
        print(f"🔓 处理: {file_path}")
        # 打开 PDF（无 user password 的情况下可以直接打开）
        pdf = pikepdf.open(file_path)

        # 保存解锁版（覆盖原文件）
        pdf.save(file_path)
        pdf.close()
        print(f"✅ 已解锁: {file_path}")
    except pikepdf.PasswordError:
        print(f"❌ 文件 {file_path} 需要打开密码，无法直接解锁")


def unlock_pdfs(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            try:
                print(f"🔓 处理: {filename}")
                # 打开 PDF（无 user password 的情况下可以直接打开）
                pdf = pikepdf.open(file_path)
                new_file_path = os.path.join(folder_path, '_' + filename)
                # 保存解锁版（覆盖原文件）
                pdf.save(new_file_path)
                pdf.close()
                print(f"✅ 已解锁: {filename}")
            except pikepdf.PasswordError:
                print(f"❌ 文件 {filename} 需要打开密码，无法直接解锁")
            except Exception as e:
                print(f"❌ 处理 {filename} 出错: {e}")

# import fitz  # PyMuPDF
#
# def get_bookmarks(pdf_path):
#     doc = fitz.open(pdf_path)
#
#     # 获取书签（目录）
#     bookmarks = doc.get_toc(simple=False)
#
#     # 打印书签信息
#     for item in bookmarks:
#         level = item["level"]
#         title = item["title"]
#         page = item["page"]
#         print("  " * (level - 1) + f"- {title} (page {page})")


import PyPDF2

def get_pdf_bookmarks_with_children(pdf_path):
    def process_outline_items(items, level=0):
        bookmarks = []
        for item in items:
            if isinstance(item, list):
                # 这是一个嵌套的书签列表
                bookmarks.extend(process_outline_items(item, level + 1))
            elif isinstance(item, dict):
                # 这是一个书签项
                title = item.get('/Title', '无标题')
                page_num = reader.get_destination_page_number(item) + 1  # 转为1-based
                bookmark = {
                    'title': title,
                    'page': page_num,
                    'level': level,
                    'children': []
                }

                # 检查是否有子书签
                if '/First' in item and '/Last' in item:
                    first = item['/First']
                    last = item['/Last']
                    current = first
                    while True:
                        bookmark['children'].append({
                            'title': current.get('/Title', '无标题'),
                            'page': reader.get_destination_page_number(current) + 1,
                            'level': level + 1
                        })
                        if current == last:
                            break
                        current = current['/Next']

                bookmarks.append(bookmark)
        return bookmarks

    bookmarks = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        if reader.outline:
            bookmarks = process_outline_items(reader.outline)

    return bookmarks



# 打印书签（包括子书签）
def print_bookmarks(bookmarks, indent=0):
    for bm in bookmarks:
        # print(' ' * indent * 4 + f"{bm['title']}, 页码: {bm['page']}, 层级: {bm['level']}")
        print(' ' * indent * 4 + f"{bm['title']}")
        if bm['children']:
            print_bookmarks(bm['children'], indent + 1)





if __name__ == '__main__':
    # 处理解锁所有 PDF
    unlock_pdfs("/Users/linjingu/Documents/Ryan/English/经典分级阅读RAZ点读版/RAZ绘本PDF点读版/Z.PDF")
    # get_bookmarks("chinese.PDF")

    # 获取 PDF 书签
    # pdf_path = '/Users/linjingu/Documents/Ryan/数学/数学_笔记_OCR.pdf'
    # bookmarks = get_pdf_bookmarks_with_children(pdf_path)
    # print_bookmarks(bookmarks)

