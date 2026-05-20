"""
Day 2 - Step 2-5: 第一个 Agent（带工具）
让大模型学会调用"计算器"和"获取当前时间"工具
"""

import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent

load_dotenv()


# ===== 1. 创建模型 =====
model = ChatDeepSeek(
    model=os.getenv("DEEPSEEK_MODEL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base=os.getenv("DEEPSEEK_BASE_URL"),
    extra_body={"thinking": {"type": "disabled"}},
)


# ===== 2. 定义工具（就是普通 Python 函数！）=====
# ⭐ 关键：函数的【文档字符串】就是给 AI 看的"工具说明书"
#    AI 靠 docstring 判断"什么时候该用这个工具"

def calculator(expression: str) -> str:
    """计算一个数学表达式并返回结果。
    
    输入应该是一个合法的 Python 数学表达式字符串，
    例如 "123 * 456" 或 "(25 + 17) * 3"。
    """
    try:
        # 注意：eval 有安全风险，仅用于学习 Demo
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算出错：{e}"


def get_current_time(query: str = "") -> str:
    """获取当前的日期和时间。
    
    当用户询问现在几点、今天是什么日期时使用此工具。
    """
    now = datetime.now()
    return f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"


# ===== 3. 创建 Agent =====
agent = create_agent(
    model=model,
    tools=[calculator, get_current_time],   # 把工具列表传进去
    system_prompt="你是一个能调用工具的智能助手。遇到计算或时间问题时，主动使用对应的工具，不要自己瞎猜。",
)


# ===== 4. 测试 Agent =====
def ask_agent(question: str):
    """向 agent 提问并打印完整过程"""
    print("=" * 60)
    print(f"🧑 用户：{question}")
    print("=" * 60)
    
    # agent 的输入格式：{"messages": [{"role": "user", "content": "..."}]}
    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    
    # result["messages"] 是完整的对话历史（含工具调用过程）
    # 最后一条是 AI 的最终回答
    final_message = result["messages"][-1]
    print(f"🤖 AI 最终回答：{final_message.content}\n")
    
    # 打印中间过程（看 Agent 调用了哪些工具）
    print("🔍 Agent 执行过程：")
    for msg in result["messages"]:
        msg_type = type(msg).__name__
        if msg_type == "HumanMessage":
            print(f"   [用户] {msg.content}")
        elif msg_type == "AIMessage":
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"   [AI决定调用工具] {tc['name']}({tc['args']})")
            if msg.content:
                print(f"   [AI回复] {msg.content}")
        elif msg_type == "ToolMessage":
            print(f"   [工具返回] {msg.content}")
    print()


# ===== 5. 跑三个测试 =====
ask_agent("现在几点了？")
ask_agent("帮我算一下 (25 + 17) * 3 等于多少？")
ask_agent("你好，介绍一下你自己")  # 这个不需要工具，看 Agent 会不会"不调用工具"