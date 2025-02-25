import asyncio
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import PaperAnalysisAgent
from src.utils import save_analysis_results, load_config


async def analyze_single_paper(agent, paper_path: str, output_dir: str):
    """分析单篇论文"""
    try:
        results = await agent.analyze_paper(paper_path)

        # 打印结果
        print(f"\n正在分析论文：{os.path.basename(paper_path)}")
        for section, analysis in results.items():
            print(f"\n=== {section} ===")
            print(analysis)

        # 保存结果
        saved_file = save_analysis_results(results, paper_path, output_dir)
        print(f"\n分析结果已保存到：{saved_file}")

    except Exception as e:
        print(f"分析论文 {paper_path} 时发生错误: {str(e)}")


async def main():
    # 获取配置文件路径
    config_path = os.path.join(os.path.dirname(__file__), "../config/config.yaml")
    config = load_config(config_path)

    # 初始化agent
    agent = PaperAnalysisAgent(config_path)

    # 设置输出目录
    output_dir = os.path.join(os.path.dirname(__file__), "../output")

    # 获取论文路径列表
    paper_paths = config["papers"]["paths"]
    if isinstance(paper_paths, str):
        paper_paths = [paper_paths]

    # 分析所有论文
    for paper_path in paper_paths:
        await analyze_single_paper(agent, paper_path, output_dir)


if __name__ == "__main__":
    asyncio.run(main())
