"""
Day 4 - 企业知识库智能问答助手（RAG Web 应用）
基于 Streamlit + LangChain + Chroma + DeepSeek
"""

import streamlit as st
from rag_core import build_vectorstore, answer_question


# ===== 页面配置 =====
st.set_page_config(
    page_title="企业知识库问答助手",
    page_icon="📚",
    layout="wide",
)

st.title("📚 企业知识库智能问答助手")
st.caption("基于 RAG（检索增强生成）技术 | LangChain + Chroma + DeepSeek")


# ===== 初始化 session_state =====
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0


# ===== 侧边栏：知识库管理 =====
with st.sidebar:
    st.header("📄 知识库管理")

    uploaded_file = st.file_uploader(
        "上传知识库文档（.txt）",
        type=["txt"],
    )

    if st.button("🔨 构建知识库", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.warning("请先上传一个 .txt 文档")
        else:
            text = uploaded_file.read().decode("utf-8")
            with st.spinner("正在构建知识库...（向量化需要几秒）"):
                vectorstore, chunk_count = build_vectorstore(text)
                st.session_state.vectorstore = vectorstore
                st.session_state.chunk_count = chunk_count
                st.session_state.messages = []
            st.success(f"✅ 构建完成！共 {chunk_count} 个片段")

    st.divider()

    # 知识库状态（只显示一次，不堆叠）
    if st.session_state.vectorstore is not None:
        st.success(f"🟢 知识库已就绪（{st.session_state.chunk_count} 个片段）")
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("⚪ 请上传文档并构建知识库")

    st.divider()
    st.markdown("##### 💡 试试这样问：")
    st.caption("• 退货要几天？\n\n• 年假有多少天？\n\n• 报销怎么操作？")


# ===== 主区域：对话界面 =====

# 没有对话历史时，显示欢迎引导
if not st.session_state.messages:
    if st.session_state.vectorstore is None:
        st.info("👈 请先在左侧上传文档并点击「构建知识库」，然后就可以开始提问啦！")
    else:
        st.info("✅ 知识库已就绪！在下方输入框提问试试吧 👇")


# 显示历史对话
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("📎 查看检索来源"):
                for i, src in enumerate(msg["sources"]):
                    st.markdown(f"**片段 {i+1}：** {src}")


# 输入框
if question := st.chat_input("请输入你的问题..."):
    if st.session_state.vectorstore is None:
        st.error("⚠️ 请先在左侧上传文档并构建知识库！")
    else:
        # 显示并保存用户问题
        with st.chat_message("user"):
            st.write(question)
        st.session_state.messages.append({"role": "user", "content": question})

        # 生成 AI 回答
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                answer, sources = answer_question(
                    st.session_state.vectorstore, question
                )
            st.write(answer)
            with st.expander("📎 查看检索来源"):
                for i, src in enumerate(sources):
                    st.markdown(f"**片段 {i+1}：** {src}")

        # 保存 AI 回答
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
        })