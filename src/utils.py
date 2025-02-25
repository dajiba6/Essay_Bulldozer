import yaml
from typing import Dict
import json
import os
from datetime import datetime


def load_config(config_path: str) -> Dict:
    """加载配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_debug_log(data: Dict, debug_dir: str, filename: str):
    """保存debug日志

    Args:
        data: 要保存的数据
        debug_dir: 日志目录
        filename: 日志文件名
    """
    os.makedirs(debug_dir, exist_ok=True)
    file_path = os.path.join(debug_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_analysis_results(
    results: Dict, paper_path: str, output_dir: str = "output"
) -> str:
    """保存分析结果到输出目录

    Args:
        results: 分析结果字典
        paper_path: 原论文路径
        output_dir: 输出目录

    Returns:
        str: 保存的文件路径
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 生成输出文件名
    paper_name = os.path.splitext(os.path.basename(paper_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{paper_name}_analysis_{timestamp}.json")

    # 保存JSON格式的结果
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 生成可读性更好的Markdown格式
    md_file = os.path.join(output_dir, f"{paper_name}_analysis_{timestamp}.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# 论文分析报告\n\n")
        f.write(f"论文：{paper_name}\n")
        f.write(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for section, content in results.items():
            f.write(f"## {section}\n\n")
            f.write(f"{content}\n\n")

    return output_file
