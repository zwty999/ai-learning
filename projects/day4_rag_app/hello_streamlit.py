"""
Day 4 - Streamlit 入门：感受"纯 Python 做网页"
"""

import streamlit as st

# ===== 页面标题 =====
st.title("🤖 我的第一个 Streamlit 应用")

# ===== 文本 =====
st.write("欢迎来到 Streamlit 的世界！")

# ===== 分割线 =====
st.divider()

# ===== 输入框 =====
name = st.text_input("请输入你的名字：")

# ===== 按钮 + 交互 =====
if st.button("打个招呼"):
    if name:
        st.success(f"你好，{name}！👋 欢迎学习 AI 应用开发！")
    else:
        st.warning("请先输入名字哦~")

# ===== 侧边栏 =====
with st.sidebar:
    st.header("侧边栏")
    st.write("这里可以放设置、上传等功能")
    mood = st.select_slider(
        "今天学习的心情：",
        options=["😫", "😐", "🙂", "😄", "🤩"],
        value="🙂"
    )
    st.write(f"你的心情：{mood}")