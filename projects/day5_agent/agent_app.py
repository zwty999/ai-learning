"""
Day 5 - 多工具智能 Agent
集成 RAG 知识库、计算器、时间工具
Agent 根据问题自主决策调用哪个工具
"""

import os
from dotenv import load_dotenv

from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent

# 导入我们定义的工具
from agent_tools import search_knowledge_base, calculator, get_current_time

load_dotenv()


# ===== 1. 创建大模型 =====
model = ChatDeepSeek(
    model=os.getenv("DEEPSEEK_MODEL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base=os.getenv("DEEPSEEK_BASE_URL"),
    extra_body={"thinking": {"type": "disabled"}},
)


# ===== 2. 创建 Agent（把 3 个工具交给它）=====
agent = create_agent(
    model=model,
    tools=[search_knowledge_base, calculator, get_current_time],
    system_prompt="""你是一个智能客服助手。你可以使用以下工具：
1. search_knowledge_base：查询公司制度、政策、规定（退货、请假、报销、福利等）
2. calculator：进行数学计算
3. get_current_time：获取当前时间

请根据用户问题，自主判断是否需要调用工具、调用哪个工具。
如果是公司制度相关问题，必须调用知识库工具，不要凭记忆回答。
如果是闲聊或常识问题，可以直接回答。""",
)


# ===== 3. 提问函数（带过程展示）=====
def ask(question: str):
    """向 Agent 提问，并展示完整决策过程"""
    print("=" * 60)
    print(f"🧑 用户：{question}")
    print("=" * 60)

    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })

    # 展示 Agent 的工具调用过程
    print("🔍 Agent 决策过程：")
    for msg in result["messages"]:
        msg_type = type(msg).__name__
        if msg_type == "AIMessage":
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"   🛠️ 决定调用工具：{tc['name']}({tc['args']})")
        elif msg_type == "ToolMessage":
            content = msg.content.replace("\n", " ")[:60]
            print(f"   📦 工具返回：{content}...")

    # 最终回答
    final = result["messages"][-1]
    print(f"\n🤖 最终回答：{final.content}\n")


# ===== 4. 测试不同类型的问题 =====
if __name__ == "__main__":
    ask("公司的退货政策是几天？")           # 应该调用 RAG
    ask("帮我算一下 1580 * 12 等于多少？")   # 应该调用计算器
    ask("现在几点了？")                       # 应该调用时间工具
    ask("你好，你是谁？")                     # 应该不调用工具，直接答