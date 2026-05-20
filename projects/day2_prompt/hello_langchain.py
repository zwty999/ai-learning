"""
Day 2 - Step 2: LangChain 1.x Hello World
对比 Day 1 的"裸调用 OpenAI SDK"和"LangChain 优雅写法"
"""

import os
from dotenv import load_dotenv

# LangChain 核心导入
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


# ===== 1. 创建 ChatModel（统一接口，无需关心底层 HTTP）=====
model = ChatDeepSeek(
    model=os.getenv("DEEPSEEK_MODEL"),   # deepseek-v4-flash
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base=os.getenv("DEEPSEEK_BASE_URL"),
)


# ===== 2. 构造消息（用类，类型安全）=====
messages = [
    SystemMessage(content="你是一个友好、简洁的 Python 教学助手。"),
    HumanMessage(content="什么是装饰器？请用一句话回答。"),
]


# ===== 3. 一句话调用 =====
print("🤖 正在调用 DeepSeek V4-Flash...\n")
response = model.invoke(messages)


# ===== 4. 解析响应（直接 .content，不再嵌套）=====
print("📝 AI 回复：")
print(response.content)
print()

# ===== 5. 也能看到 token 用量（标准化字段）=====
print("=" * 50)
print("📊 Token 用量")
if hasattr(response, "usage_metadata") and response.usage_metadata:
    usage = response.usage_metadata
    print(f"   输入: {usage.get('input_tokens')} tokens")
    print(f"   输出: {usage.get('output_tokens')} tokens")
    print(f"   总计: {usage.get('total_tokens')} tokens")
print("=" * 50)