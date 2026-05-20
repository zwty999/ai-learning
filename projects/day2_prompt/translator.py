"""
翻译工具：用 LangChain 实现"翻译邮件"功能
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
# TODO 3: 创建包含两个占位符 {source_language} 和 {target_language} 的模板
# 提示：
#   - system 消息设定角色为"专业翻译助手"
#   - user 消息要求："请把下面这封邮件从 {source_language} 翻译成 {target_language}。
#                    原邮件：{source_text}。
#                    要求：直接给出翻译后的邮件，不要加额外说明，100 字以内。"
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一名专业翻译助手，擅长根据用户需求，将邮件从 {source_language} 翻译成 {target_language}。"
     
        
    ),
    (
        "user",
        """请把下面这封邮件从 {source_language} 翻译成 {target_language}。
        原邮件:{source_text}
        要求：直接给出翻译后的邮件,不要加额外说明。
        """
    ),
])  
# ===== 步骤 3: 准备变量字典 =====
# TODO 4: 创建一个字典，包含 source_language 和 target_language
translator_data = {
    "source_language": "zh-CN",
    "target_language": "en-US",
    "source_text": "老板，我明天请假，有事，不来了。",
}

 

# ===== 步骤 4: 渲染模板 + 调用模型 =====
# TODO 5: 两步合一
prompt = prompt_template.invoke(translator_data)
response = model.invoke(prompt)


# ===== 步骤 5: 打印结果 =====
# TODO 6: 打印 response.content
print("=" * 50)
print("📝 翻译后的文本：")
print(response.content)
print("=" * 50)