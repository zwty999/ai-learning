"""
Prompt 工程对比实验
对比"普通 Prompt"和"工程级 Prompt"的输出质量差距
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)
MODEL = os.getenv("DEEPSEEK_MODEL")


def call_llm(prompt: str) -> str:
    """通用调用函数：传入 prompt，返回 AI 回复"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# ============ 实验 A：普通 Prompt（新人写法）============
prompt_A = """帮我写一段简历的自我评价。"""


# ============ 实验 B：工程级 Prompt（用 CRISPE 框架）============
prompt_B = """[角色]
你是一名资深 IT 行业 HR，看过 1000+ 份应届生简历，深知什么样的自我评价能打动招聘方。

[背景]
我是一名计算机相关专业的应届毕业生，目标岗位是「AI 应用工程师」。
我有 Python 基础，调过 OpenAI/Claude API，对大模型应用开发有兴趣。
准备投递互联网中大厂。

[任务]
请帮我写一段简历的「自我评价」。

[要求]
1. 字数控制在 100-150 字
2. 必须体现 3 个维度：技术能力、学习能力、职业规划
3. 使用具体的能力描述，避免"性格开朗""善于沟通"这类空话
4. 突出与「AI 应用工程师」岗位的匹配度

[输出格式]
直接给出自我评价文本，不要加额外说明。"""


# ============ 跑两个实验，打印对比 ============
print("=" * 60)
print("【实验 A：普通 Prompt】")
print("=" * 60)
print(f"📤 Prompt: {prompt_A}\n")
print(f"📥 输出:\n{call_llm(prompt_A)}\n")

print("=" * 60)
print("【实验 B：工程级 Prompt】")
print("=" * 60)
print(f"📤 Prompt: {prompt_B[:80]}...（省略，详见代码）\n")
print(f"📥 输出:\n{call_llm(prompt_B)}\n")

print("=" * 60)
print("👀 请对比两次输出的：")
print("   1. 字数是否符合要求")
print("   2. 内容是否具体（不是套话）")
print("   3. 是否匹配岗位")
print("=" * 60)