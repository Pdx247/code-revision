from langchain_openai import ChatOpenAI
from config import *
import json
import datetime

# 示例代码集
with open(CODES_DATA_JSONL_PATH, 'r', encoding = 'utf-8') as f:
    all_codes = [json.loads(line) for line in f]

dsrc_codes = [code['source'] for code in all_codes]
src_codes = [code['target'] for code in all_codes]

# print(fantastic_codes[0])
# print(awful_codes[0])

# print(criterion)

# 提示词模版
with open(PROMPT_LLM4DE_PATH, 'r', encoding = 'utf-8') as f:
    prompt_template = f.read()


model = ChatOpenAI(
    model = SILICONFLOW_MODEL_QWEN,
    temperature = 0,
    max_tokens = None,
    timeout = None,
    max_retries = 2,
    api_key = SILICONFLOW_API_KEY,
    base_url= SILICONFLOW_BASE_URL
)

dataset_size = 10
now = datetime.datetime.now()

for i in range(dataset_size):
    src_code = src_codes[i]
    dsrc_code = dsrc_codes[i]
    prompt = prompt_template.replace("[SRC]", src_code).replace("[DSRC]", dsrc_code)
    # print(prompt)
    response = model.invoke(prompt)
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time}]   {i+1}/{dataset_size}")
    with open(OUTPUT_RESPONSE_PATH + "/qwen-out-v1-llm4de.md", 'a', encoding = 'utf-8') as f:
        f.write(f"[task {i}] \n\n" + response.content + "\n")


