from langchain_openai import ChatOpenAI
from config import *
import json
import datetime

# 示例代码集
with open(CODES_DATA_JSONL_PATH, 'r', encoding = 'utf-8') as f:
    all_codes = [json.loads(line) for line in f]

awful_codes = [code['source'] for code in all_codes]
fantastic_codes = [code['target'] for code in all_codes]

# print(fantastic_codes[0])
# print(awful_codes[0])

# 评分标准
with open(CRITERION_DOCUMENT_PATH, 'r', encoding = 'utf-8') as f:
    criterion = f.read()

# print(criterion)

# 提示词模版
with open(PROMPT_PATH, 'r', encoding = 'utf-8') as f:
    prompt_template = f.read()


model = ChatOpenAI(
    model = SILICONFLOW_MODEL_DEEPSEEK,
    temperature = 0,
    max_tokens = None,
    timeout = None,
    max_retries = 2,
    api_key = SILICONFLOW_API_KEY,
    base_url= SILICONFLOW_BASE_URL
)

dataset_size = 100
now = datetime.datetime.now()

for i in range(dataset_size):
    awful_code = awful_codes[i]
    prompt = prompt_template.replace("{{CRITERION}}", criterion).replace("{{SOURCE_CODE}}", awful_code)
    # print(prompt)
    response = model.invoke(prompt)
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time}]   {i+1}/{dataset_size}")
    with open(OUTPUT_RESPONSE_PATH + "/deepseek-out-v1.jsonl", 'a', encoding = 'utf-8') as f:
        f.write(response.content + "\n")


