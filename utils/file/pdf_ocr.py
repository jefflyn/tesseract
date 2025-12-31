import os
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from paddleocr import PaddleOCR
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm

from pdf2image import convert_from_path
# import os
#
# # 自动获取当前 conda 环境的 bin 路径
# poppler_path = os.path.join(os.environ["CONDA_PREFIX"], "bin")
#
# pages = convert_from_path(
#     "test.pdf",
#     poppler_path=poppler_path
# )
#
# print("Converted pages:", len(pages))

# -------------------------------------------------------------
# 工具：判断 PDF 是否已有文本层
# -------------------------------------------------------------
def pdf_has_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            if page.extract_text() and page.extract_text().strip():
                return True
        return False
    except:
        return False


# -------------------------------------------------------------
# 工具：图像倾斜矫正（deskew）
# -------------------------------------------------------------
def deskew_image(pil_image):
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2GRAY)
    img = cv2.bitwise_not(img)

    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = 90 + angle

    M = cv2.getRotationMatrix2D((img.shape[1] / 2, img.shape[0] / 2), angle, 1.0)
    img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]),
                         flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return img


# -------------------------------------------------------------
# 单页 OCR 处理
# -------------------------------------------------------------
def process_page(args):
    img, page_num, ocr = args

    # 倾斜矫正
    deskewed = deskew_image(img)
    final_img = deskewed

    # OCR 识别
    result = ocr.ocr(final_img)

    return final_img, result, page_num


# -------------------------------------------------------------
# 将多页写入可搜索 PDF
# -------------------------------------------------------------
def build_searchable_pdf(results, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)

    for final_img, result, page_num in sorted(results, key=lambda x: x[2]):
        # 绘制原图
        img_path = f"temp_{page_num}.png"
        cv2.imwrite(img_path, final_img)
        c.drawImage(img_path, 0, 0, width=612, height=792)

        # 隐藏文字层
        c.setFillColorRGB(0, 0, 0, alpha=0.01)

        for line in result:
            for box, (text, confidence) in line:
                x = box[0][0]
                y = box[0][1]
                c.drawString(x, 792 - y, text)

        c.showPage()
        os.remove(img_path)

    c.save()


# -------------------------------------------------------------
# PDF 处理主体（含书签复制）
# -------------------------------------------------------------
def process_pdf(input_pdf, output_pdf, ocr):
    print(f"⚡ 正在处理：{input_pdf}")

    # 如果已有文字层 → 跳过
    if pdf_has_text(input_pdf):
        print("✔ 检测到已有可搜索文本层，跳过")
        return

    # PDF 转图片
    images = convert_from_path(input_pdf, dpi=300)

    # 多线程处理每一页
    tasks = [(img, idx, ocr) for idx, img in enumerate(images)]
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(tqdm(executor.map(process_page, tasks),
                            total=len(tasks), desc="页面 OCR 中"))

    # 生成可搜索 PDF
    temp_pdf = output_pdf.replace(".pdf", "_temp.pdf")
    build_searchable_pdf(results, temp_pdf)

    # 保留书签
    write = PdfWriter()
    reader = PdfReader(input_pdf)
    ocr_reader = PdfReader(temp_pdf)

    for page in ocr_reader.pages:
        write.add_page(page)

    # 复制书签
    try:
        if reader.outline:
            write.add_outline_item("Original Bookmarks", 0)
    except:
        pass

    with open(output_pdf, "wb") as f:
        write.write(f)

    os.remove(temp_pdf)
    print("✔ 输出可搜索 PDF →", output_pdf)


# -------------------------------------------------------------
# 批量处理整个文件夹
# -------------------------------------------------------------
def batch_process(folder):
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 自动旋转 + 中文识别

    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]

    for pdf in pdf_files:
        input_pdf = os.path.join(folder, pdf)
        output_pdf = os.path.join(folder, "OCR_" + pdf)

        process_pdf(input_pdf, output_pdf, ocr)


def process(input_pdf):
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 自动旋转 + 中文识别
    output_pdf = input_pdf.replace(".pdf", "_OCR.pdf")
    process_pdf(input_pdf, output_pdf, ocr)


if __name__ == '__main__':
    # 用户入口
    # batch_process("/Users/yourname/pdf_folder")
    process("/Users/linjingu/Documents/Ryan/English/RAZ/合集/K_v.pdf")