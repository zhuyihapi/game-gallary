from email import message
import os
from openai import OpenAI
from datetime import datetime
from pprint import pprint
import json

current_month = datetime.now().strftime("%B %Y")
print(current_month)
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="a",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    # qwen-max qwen-plus qwen-turbo
    model="qwen-max",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    extra_body={"enable_search": True, "type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": f"You are a helpful web search assistant. "
            f"Search the internet for the ten most anticipated and highest-rated video games "
            f"that were **released exclusively in {current_month}**. "
            f"Only include games that have been officially released in this month. "
            f"Provide their exact official names and release dates. "
            f"Ensure the information is up-to-date and accurately reflects current gaming trends. "
            f"Return the result strictly in the following JSON format: "
            f'{{"games": [{{"name": "<exact official name>", "release_date": "<release date>"}}, ...]}} '
            f"Do not include any additional text or explanations—only return the JSON object.",
        }
    ],
)

# print(completion.model_dump_json())

response_content = json.loads(completion.model_dump_json())["choices"][0]["message"][
    "content"
]
pprint(json.loads(response_content))
