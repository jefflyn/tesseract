import fitz  # PyMuPDF
import pdfplumber
from typing import Tuple, Dict, List


def analyze_pdf_structure(pdf_path: str) -> Dict:
    """
    分析PDF结构，判断是否可搜索
    """
    result = {
        "is_searchable": False,
        "has_text_layer": False,
        "is_scanned": True,
        "page_count": 0,
        "text_ratio": 0.0,
        "images_per_page": []
    }

    try:
        with fitz.open(pdf_path) as doc:
            result["page_count"] = len(doc)

            total_text_length = 0
            total_image_area = 0
            page_area = 0

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)

                # 提取文本
                text = page.get_text()
                text_length = len(text.strip())
                total_text_length += text_length

                # 检测图片
                image_list = page.get_images()
                result["images_per_page"].append(len(image_list))

                # 计算图片面积
                img_area = 0
                for img in image_list:
                    rect = page.get_image_bbox(img[7])
                    img_area += rect.width * rect.height
                total_image_area += img_area

                # 计算页面面积
                page_rect = page.rect
                page_area += page_rect.width * page_rect.height

            # 计算文本比例
            if page_area > 0:
                result["text_ratio"] = total_text_length / page_area

            # 判断是否可搜索
            result["has_text_layer"] = total_text_length > 100
            result["is_scanned"] = total_image_area > page_area * 0.5
            result["is_searchable"] = result["has_text_layer"] and not result["is_scanned"]

            return result

    except Exception as e:
        print(f"分析PDF失败: {e}")
        return result


# 使用示例
pdf_info = analyze_pdf_structure("/Users/linjingu/Documents/Ryan/English/RAZ/合集/L_h_OCR.pdf")
print(f"是否可搜索: {pdf_info['is_searchable']}")
print(f"是否有文本层: {pdf_info['has_text_layer']}")
print(f"是否为扫描件: {pdf_info['is_scanned']}")
print(f"文本比例: {pdf_info['text_ratio']:.2%}")

import ocrmypdf
import pytesseract
from PIL import Image
import fitz
import io
import os
from typing import Optional


class PDFOCRProcessor:
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        初始化OCR处理器
        """
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def ocr_pdf_with_ocrmypdf(self, input_pdf: str, output_pdf: str,
                              language: str = 'chi_sim+eng') -> bool:
        """
        使用ocrmypdf创建可搜索PDF
        """
        try:
            ocrmypdf.ocr(
                input_pdf,
                output_pdf,
                language=language,
                deskew=True,  # 自动纠偏
                clean=True,  # 清理图片
                optimize=1,  # 优化级别
                force_ocr=False,  # 只对没有文本的页面进行OCR
                skip_text=True,  # 跳过已有文本
                jobs=4  # 使用4个CPU核心
            )
            print(f"OCR完成: {output_pdf}")
            return True
        except Exception as e:
            print(f"OCR失败: {e}")
            return False

    def create_searchable_pdf_custom(self, input_pdf: str, output_pdf: str,
                                     dpi: int = 300, language: str = 'chi_sim+eng') -> bool:
        """
        自定义OCR处理流程
        """
        try:
            # 打开PDF
            doc = fitz.open(input_pdf)
            new_doc = fitz.open()

            for page_num in range(len(doc)):
                print(f"处理第 {page_num + 1}/{len(doc)} 页...")
                page = doc.load_page(page_num)

                # 检查页面是否有文本
                text = page.get_text().strip()

                if len(text) < 50:  # 如果文本很少，认为是扫描件
                    # 将页面转为图片
                    pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))

                    # 执行OCR
                    ocr_text = pytesseract.image_to_string(img, lang=language)

                    if ocr_text.strip():
                        # 创建新页面
                        new_page = new_doc.new_page(width=page.rect.width,
                                                    height=page.rect.height)

                        # 插入原图
                        new_page.insert_image(page.rect, stream=img_data)

                        # 添加透明文本层
                        new_page.insert_text(
                            (50, 50),  # 位置
                            ocr_text,
                            fontsize=1,  # 很小的字号
                            color=(0, 0, 0, 0)  # 完全透明
                        )
                else:
                    # 已有文本，直接复制页面
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

            # 保存
            new_doc.save(output_pdf)
            new_doc.close()
            doc.close()

            print(f"创建可搜索PDF完成: {output_pdf}")
            return True

        except Exception as e:
            print(f"处理失败: {e}")
            return False

    def batch_ocr_pdfs(self, input_folder: str, output_folder: str,
                       language: str = 'chi_sim+eng') -> Dict:
        """
        批量OCR处理PDF
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        results = {
            "total": 0,
            "success": 0,
            "failed": [],
            "processed": []
        }

        for filename in os.listdir(input_folder):
            if filename.lower().endswith('.pdf'):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder,
                                           f"ocr_{filename}")

                results["total"] += 1

                try:
                    success = self.ocr_pdf_with_ocrmypdf(
                        input_path, output_path, language
                    )

                    if success:
                        results["success"] += 1
                        results["processed"].append(filename)
                    else:
                        results["failed"].append(filename)

                except Exception as e:
                    print(f"处理 {filename} 失败: {e}")
                    results["failed"].append(filename)

        return results


# 使用示例
processor = PDFOCRProcessor()

# 单文件处理
processor.ocr_pdf_with_ocrmypdf("scanned.pdf", "searchable.pdf", language="chi_sim+eng")

# 批量处理
# results = processor.batch_ocr_pdfs("input_folder", "output_folder")