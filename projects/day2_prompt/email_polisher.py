"""
邮件润色工具：用 LangChain 实现"按指定语气润色邮件"功能
"""

import os
from dotenv import load_dotenv

# TODO 1: 导入 LangChain 需要的两个类
# 提示：参考 resume_writer_v2.py 的 import 部分
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


# ===== 步骤 1: 创建 ChatModel =====
# TODO 2: 参考 resume_writer_v2.py，创建 model
model = ChatDeepSeek(
    model=os.getenv("DEEPSEEK_MODEL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base=os.getenv("DEEPSEEK_BASE_URL"),
)


# ===== 步骤 2: 创建 ChatPromptTemplate =====
# TODO 3: 创建包含两个占位符 {tone} 和 {original_email} 的模板
# 提示：
#   - system 消息设定角色为"专业邮件写作助手"
#   - user 消息要求："请把下面这封邮件润色成 {tone} 语气，保持原意但优化措辞。
#                    原邮件：{original_email}。
#                    要求：直接给出润色后的邮件，不要加额外说明，100 字以内。"
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一名专业邮件写作助手，擅长根据用户需求，将邮件润色成指定语气，保持原意但优化措辞。"
     
        
    ),
    (
        "user",
        """请把下面这封邮件润色成 {tone} 语气,保持原意但优化措辞。
        原邮件:{original_email}
        要求：直接给出润色后的邮件,不要加额外说明,100 字以内。
        """
    ),
])  
# ===== 步骤 3: 准备变量字典 =====
# TODO 4: 创建一个字典，包含 tone 和 original_email
email_data = {
    "tone": "正式",
    "original_email": "老板，我明天请假，有事，不来了。",
}


# ===== 步骤 4: 渲染模板 + 调用模型 =====
# TODO 5: 两步合一
prompt = prompt_template.invoke(email_data)
response = model.invoke(prompt)


# ===== 步骤 5: 打印结果 =====
# TODO 6: 打印 response.content
print("=" * 50)
print("📝 润色后的邮件：")
print(response.content)
print("=" * 50)