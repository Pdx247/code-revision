## Current Work
- 确定代码审查标准（criterion.md）
- 对数据集的代码进行打分
  - 打分低的添加注释增加可读性

#### 配置环境
```bash
pip install langchain langchain-openai
```

#### 配置文件
```python
SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"
SILICONFLOW_API_KEY = "your api key"
SILICONFLOW_MODEL_QWEN = "Qwen/Qwen3.6-35B-A3B"
SILICONFLOW_MODEL_DEEPSEEK = "deepseek-ai/DeepSeek-V3.2"
SILICONFLOW_MODEL_KIMI = "Pro/moonshotai/Kimi-K2.5"

CODES_DATA_JSONL_PATH = "path/to/data.jsonl"
CRITERION_DOCUMENT_PATH = "path/to/criterion.md"
PROMPT_PATH = "path/to/prompt.md"

OUTPUT_RESPONSE_PATH = "path/to/output"
```

#### 模型输出
模型输出在output文件夹下
- 模型只运行了10条
- 数据集原本的schema有source和target，source当作低分代码（awful_code），target当作高分代码（fantastic_codes）

> 一定要设置dataset_size（在main.py），不然一次性跑8w条token就炸了
