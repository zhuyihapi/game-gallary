import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="heihehi", 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    
)
completion = client.chat.completions.create(
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    extra_body={"enable_search": True},
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '请在互联网搜索怪猎荒野的英文名字和发售时间'}],
    )
    
print(completion.model_dump_json())