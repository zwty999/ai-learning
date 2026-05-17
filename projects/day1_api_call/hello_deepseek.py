"""
第一个 AI 程序：调用 DeepSeek V4-Flash 实现单轮对话
日期：2026-05-16
"""

import os
from dotenv import load_dotenv
from openai import OpenAI


# ===== 1. 加载 .env 文件中的配置 =====
load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
MODEL = os.getenv("DEEPSEEK_MODEL")

if not API_KEY:
    raise ValueError("❌ 未找到 DEEPSEEK_API_KEY，请检查 .env 文件")


# ===== 2. 创建 OpenAI 客户端（指向 DeepSeek） =====
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


# ===== 3. 准备对话内容 =====
user_question = "你好，请用一句话介绍你自己"


# ===== 4. 发起 API 调用 =====
print(f"🧑 我: {user_question}")
print("🤖 DeepSeek 正在思考...\n")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": user_question}
    ],
)


# ===== 5. 解析响应 =====
ai_reply = response.choices[0].message.content


# ===== 6. 打印结果 =====
print(f"🤖 DeepSeek: {ai_reply}\n")


# ===== 7. 打印 token 用量 =====
usage = response.usage
print("=" * 50)
print(f"📊 Token 用量统计")
print(f"   输入 tokens: {usage.prompt_tokens}")
print(f"   输出 tokens: {usage.completion_tokens}")
print(f"   总计 tokens: {usage.total_tokens}")
print("=" * 50)