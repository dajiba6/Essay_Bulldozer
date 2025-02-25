from typing import Dict, List
import yaml
from .openai_client import OpenAIClient
from .paper_processor import PaperProcessor
from .utils import load_config, save_debug_log
import os
from datetime import datetime


class PaperAnalysisAgent:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.openai_client = OpenAIClient(self.config["openai"])
        self.paper_processor = PaperProcessor()
        self.debug_enabled = self.config.get("debug", {}).get("enabled", False)
        self.debug_dir = self.config.get("debug", {}).get("log_dir", "debug_logs")
        self.current_debug_data = {}

    async def analyze_paper(self, paper_path: str) -> Dict:
        """分析论文并返回结果"""
        # 初始化新的debug数据
        if self.debug_enabled:
            self.current_debug_data = {
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "paper_path": paper_path,
                "full_text": "",
                "analysis_process": [],
            }

        # 处理PDF文件，获取完整文本
        full_text = self.paper_processor.process(paper_path)

        if self.debug_enabled:
            self.current_debug_data["full_text"] = full_text

        # 分段分析
        results = {}

        for section in self.config["analysis"]["sections"]:
            # 使用配置文件中的prompt
            prompt = self.config["analysis"]["prompts"].get(section)
            if prompt:
                results[section] = await self._analyze_section(
                    full_text, section, prompt
                )

        # 生成总结
        if "summary" in self.config["analysis"]["prompts"]:
            results["summary"] = await self._analyze_section(
                full_text, "summary", self.config["analysis"]["prompts"]["summary"]
            )

        # 保存debug信息
        if self.debug_enabled:
            timestamp = self.current_debug_data["timestamp"]
            paper_name = os.path.splitext(os.path.basename(paper_path))[0]
            save_debug_log(
                self.current_debug_data,
                self.debug_dir,
                f"{paper_name}_debug_{timestamp}.json",
            )

        return results

    async def _analyze_section(
        self, full_text: str, section_name: str, prompt: str
    ) -> str:
        """分析特定章节

        Args:
            full_text: 论文完整文本
            section_name: 章节名称
            prompt: 分析提示词
        """
        # 组合通用prompt和具体章节的prompt
        common_prompt = self.config["analysis"].get("common_prompt", "")
        combined_prompt = f"{common_prompt}\n\n{prompt}"

        if self.debug_enabled:
            debug_entry = {
                "operation": f"section_analysis_{section_name}",
                "prompt": combined_prompt,
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            }
            self.current_debug_data["analysis_process"].append(debug_entry)

        response = await self.openai_client.complete(combined_prompt, full_text)
        return response
