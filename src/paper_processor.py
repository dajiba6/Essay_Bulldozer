from typing import Dict
import fitz  # PyMuPDF
import re


class PaperProcessor:
    def process(self, paper_path: str) -> str:
        """处理PDF论文，返回完整文本内容"""

        doc = fitz.open(paper_path)

        # 提取所有文本
        full_text = ""
        for page in doc:
            text = page.get_text()
            # 清理文本
            text = self._clean_text(text)
            full_text += text + "\n"

        return full_text

    def _clean_text(self, text: str) -> str:
        """清理提取的文本"""
        # 移除多余的空白字符
        text = re.sub(r"\s+", " ", text)
        # 移除特殊字符
        text = re.sub(r'[^\w\s.,;:!?()[\]{}"\'`-]', "", text)
        return text.strip()
