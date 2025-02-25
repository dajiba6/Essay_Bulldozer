from openai import AsyncOpenAI
from typing import Dict, Optional


class OpenAIClient:
    def __init__(self, config: Dict):
        """初始化API客户端

        Args:
            config: 配置字典，包含api_key, api_base, model等配置
        """
        self.client = AsyncOpenAI(
            api_key=config["api_key"],
            base_url=config.get("api_base", "https://api.openai.com/v1"),
            default_headers=config.get("headers", {}),
        )
        self.model = config["model"]
        self.temperature = config["temperature"]
        self.max_tokens = config.get("max_tokens")  # 可选参数

    async def complete(self, prompt: str, content: Optional[str] = None) -> str:
        """调用API获取完成结果"""
        messages = [
            {"role": "system", "content": "你是一个专业的论文分析助手。"},
            {"role": "user", "content": prompt},
        ]

        if content:
            messages.append({"role": "user", "content": content})

        # 构建API请求参数
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }

        # 可选参数
        if self.max_tokens:
            params["max_tokens"] = self.max_tokens

        try:
            response = await self.client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as e:
            # 处理API错误
            error_msg = f"API调用失败: {str(e)}"
            print(error_msg)
            raise
