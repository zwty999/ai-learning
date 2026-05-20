"""
Day 2 - Step 2-4: 用 LCEL 管道符重写翻译工具
对比"两步 invoke"和"一条链"的写法差异
"""

import os
from dotenv import load_dotenv

from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser   # 新增：输出解析器

load_dotenv()


# ===== 1. 创建模型 =====
model = ChatDeepSeek(
    model=os.getenv("DEEPSEEK_MODEL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base=os.getenv("DEEPSEEK_BASE_URL"),
)


# ===== 2. 创建 Prompt 模板 =====
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一名专业翻译助手，擅长将文本从 {source_language} 翻译成 {target_language}。"
    ),
    (
        "user",
        """请把下面的文本从 {source_language} 翻译成 {target_language}。
原文：{source_text}
要求：直接给出翻译结果，不要加额外说明。"""
    ),
])


# ===== 3. 创建输出解析器 =====
parser = StrOutputParser()


# ===== 4. ⭐ 用 LCEL 管道符串成一条链 ⭐ =====
chain = prompt_template | model | parser


# ===== 5. 准备数据 =====
translator_data = {
    "source_language": "zh-CN",
    "target_language": "en-US",
    "source_text": "老板，我明天请假，有事，不来了。",
}


# ===== 6. 一次调用，整条链跑完 =====
print("=" * 50)
print("📝 翻译结果（LCEL 链式调用）：")
result = chain.invoke(translator_data)   # 注意：直接得到字符串，不用 .content
print(result)
print("=" * 50)