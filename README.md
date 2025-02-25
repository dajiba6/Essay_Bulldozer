# Essay Bulldozer 论文推土机

Essay Bulldozer 是一个基于大语言模型的论文分析工具,可以帮助研究人员快速理解和提取论文中的关键信息。该工具可以自动分析论文的不同部分(如摘要、引言、方法等),并生成结构化的分析报告。


## 安装

1. 克隆仓库
2. 安装依赖requirements.txt

## 使用方法

1. 在config文件夹中创建配置文件 `config.yaml`
2. 按照一下模板进行配置，填写待填写内容
```yaml
openai:
  api_key: "待填写"
  api_base: "待填写"
  model: "待填写"
  temperature: 0.7
  # max_tokens: 2000
  headers:
    # "Authorization": "Bearer your-api-key"
    # "Custom-Header": "value"

debug:
  enabled: false  # 是否开启debug模式
  log_dir: "debug_logs"  # debug日志保存目录

papers:
  # 可以是单个论文路径或论文路径列表
  paths:
    - "待填写"
    # - "path/to/another/paper.pdf"

analysis:
  # 通用prompt，会添加到每次调用的开头
  common_prompt: |
    注意latex格式的公式和变量用$包裹，例如：$E=mc^2$。
    请确保输出格式规范，使用markdown格式。
    请用中文回答。
  
  sections:
    - abstract
    - introduction
    - methodology
    - results
    - conclusion
  
  prompts:
    abstract: "请从论文中提取摘要部分的内容，包括研究目的、方法和主要结论。"
    introduction: "请从论文中提取引言/介绍部分的内容，包括研究背景、问题陈述和研究目标。"
    methodology: "请从论文中提取方法部分的内容，详细说明研究方法、实验设计和技术细节。"
    results: "请从论文中提取结果部分的内容，包括实验结果、数据分析和关键发现。"
    conclusion: "请从论文中提取结论部分的内容，包括主要结论、研究贡献和未来展望。"
    summary: "请总结这篇论文的主要内容，包括研究目的、方法和结论。"

```
3. 运行分析脚本:
```bash
python examples/run_analysis.py
```
4. 运行结果会保存在 `output` 文件夹中