"""
多轮对话 AI 助手：通过维护 messages 历史实现"对话记忆"
日期：2026-05-16
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
MODEL = os.getenv("DEEPSEEK_MODEL")

if not API_KEY:
    raise ValueError("❌ 未找到 DEEPSEEK_API_KEY，请检查 .env 文件")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ===== 核心：维护一个对话历史列表 =====
messages = [
    {
        "role": "system",
        "content": "你是一个友好、简洁的 AI 助手。回答时尽量控制在 50 字以内。"
    }
]

# ===== 累计 token 统计 =====
total_input_tokens = 0
total_output_tokens = 0
round_count = 0

print("=" * 60)
print("🤖 DeepSeek 多轮对话助手已启动")
print("💡 输入 'quit' 或 'exit' 退出程序")
print("=" * 60)

while True:
    user_input = input("\n🧑 你: ").strip()
    
    if user_input.lower() in ["quit", "exit", "退出"]:
        print("\n👋 再见！")
        break
    
    if not user_input:
        print("⚠️  请输入内容")
        continue
    
    # 把用户输入加入历史
    messages.append({"role": "user", "content": user_input})
    
    # 调用 API（传整个 messages）
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    
    ai_reply = response.choices[0].message.content
    
    # ⭐ 把 AI 回复也加入历史 ⭐
    messages.append({"role": "assistant", "content": ai_reply})
    
    print(f"🤖 AI: {ai_reply}")
    
    round_count += 1
    total_input_tokens += response.usage.prompt_tokens
    total_output_tokens += response.usage.completion_tokens
    print(f"   [本轮: 输入 {response.usage.prompt_tokens} | 输出 {response.usage.completion_tokens} tokens]")

print("\n" + "=" * 60)
print(f"📊 本次会话统计")
print(f"   总对话轮数: {round_count}")
print(f"   累计输入 tokens: {total_input_tokens}")
print(f"   累计输出 tokens: {total_output_tokens}")
print(f"   总 tokens: {total_input_tokens + total_output_tokens}")
print("=" * 60)