"""
Day 5 - 智能客服 Agent Web 界面
展示 Agent 的自主决策过程（调用了哪个工具）
"""

import os
import streamlit as st
from dotenv import load_dotenv

from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from agent_tools import search_knowledge_base, calculator, get_current_time

load_dotenv()


# ===== 页面配置 =====
st.set_page_config(page_title="智能客服 Agent", page_icon="🤖", layout="wide")
st.title("🤖 智能客服 Agent")
st.caption("多工具智能体 | 自主调用：知识库检索(RAG) + 计算器 + 时间查询")


# ===== 工具中文名映射（用于界面展示）=====
TOOL_NAMES = {
    "search_knowledge_base": "🔍 知识库检索",
    "calculator": "🧮 计算器",
    "get_current_time": "⏰ 时间查询",
}


# ===== 创建 Agent（用 @st.cache_resource 缓存，避免重复创建）=====
@st.cache_resource
def get_agent():
    """创建 Agent，缓存起来不重复创建"""
    model = ChatDeepSeek(
        model=os.getenv("DEEPSEEK_MODEL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        api_base=os.getenv("DEEPSEEK_BASE_URL"),
        extra_body={"thinking": {"type": "disabled"}},
    )
    return create_agent(
        model=model,
        tools=[search_knowledge_base, calculator, get_current_time],
        system_prompt="""你是一个智能客服助手，可以使用以下工具：
1. search_knowledge_base：查询公司制度、政策（退货、请假、报销、福利等）
2. calculator：数学计算
3. get_current_time：获取当前时间

请根据问题自主判断调用哪个工具。公司制度问题必须查知识库，不要凭记忆回答。闲聊可直接回答。""",
    )


agent = get_agent()


# ===== 初始化对话历史 =====
if "messages" not in st.session_state:
    st.session_state.messages = []


# ===== 侧边栏：说明 =====
with st.sidebar:
    st.header("🛠️ Agent 能力")
    st.markdown("""
    本 Agent 可以自主调用 3 种工具：
    
    - 🔍 **知识库检索**：查公司制度政策
    - 🧮 **计算器**：数学运算
    - ⏰ **时间查询**：当前时间
    """)
    st.divider()
    st.markdown("##### 💡 试试这样问：")
    st.caption("• 退货政策是几天？\n\n• 帮我算 1580×12\n\n• 现在几点了？\n\n• 你好")
    st.divider()
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ===== 显示历史对话 =====
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # 显示工具调用标记
        if msg["role"] == "assistant" and msg.get("tools"):
            tools_str = "、".join(msg["tools"])
            st.caption(f"🛠️ 调用了：{tools_str}")
        st.write(msg["content"])


# ===== 输入框 =====
if question := st.chat_input("请输入你的问题..."):
    # 显示并保存用户问题
    with st.chat_message("user"):
        st.write(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Agent 处理
    with st.chat_message("assistant"):
        with st.spinner("Agent 思考中..."):
            result = agent.invoke({
                "messages": [{"role": "user", "content": question}]
            })

        # 提取调用了哪些工具
        used_tools = []
        for msg in result["messages"]:
            if type(msg).__name__ == "AIMessage":
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tool_name = TOOL_NAMES.get(tc["name"], tc["name"])
                        if tool_name not in used_tools:
                            used_tools.append(tool_name)

        # 显示工具调用标记
        if used_tools:
            st.caption(f"🛠️ 调用了：{'、'.join(used_tools)}")
        else:
            st.caption("💬 直接回答（未调用工具）")

        # 显示最终回答
        answer = result["messages"][-1].content
        st.write(answer)

    # 保存到历史
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "tools": used_tools,
    })