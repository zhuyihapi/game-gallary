import openai
from datetime import datetime
import json
from pprint import pprint

# 获取当前月份
current_month = datetime.now().strftime("%B %Y")
print(f"Current Month: {current_month}")

# 初始化 OpenAI 客户端（需要正确的 API Key）
client = openai.Client(
    api_key="aaa"
)  # 替换为你的 API Key

# 发送请求到 OpenAI API
response = client.chat.completions.create(
    model="gpt-4-turbo",  # 也可以用 gpt-4 或 gpt-3.5-turbo
    response_format={
        "type": "json_object"
    },
    messages=[
        {
            "role": "system",
            "content": (
                f"You are a helpful web search assistant. "
                f"Search the internet for the ten most anticipated and highest-rated video games "
                f"that were **released exclusively in {current_month}**. "
                f"Only include games that have been officially released in this month. "
                f"Provide their exact official names and release dates. "
                f"Ensure the information is up-to-date and accurately reflects current gaming trends. "
                f"Return the result strictly in the following JSON format: "
                f'{{"games": [{{"name": "<exact official name>", "release_date": "<release date>"}}, ...]}} '
                f"Do not include any additional text or explanations—only return the JSON object."
            ),
        }
    ],
)

# 解析 OpenAI 的 JSON 响应
response_content = response.choices[0].message.content
parsed_data = json.loads(response_content)

# 美化输出 JSON 数据
pprint(parsed_data)
