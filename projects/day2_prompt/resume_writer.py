"""
Day 2 - Step 1 师傅示范：用工程级 Prompt 生成简历项目经历
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


# 工程级 Prompt（CRISPE 框架）
prompt = """[角色]
你是一名资深 IT 行业 HR，主要招聘"AI 应用工程师"岗位。
你看过 1000+ 份候选人简历，深知一段优秀的"项目经历"应该有的样子：
3 秒钟能看清项目价值，关键词能匹配岗位 JD，具体动作而非空话。

[背景]
我是一名计算机相关专业的应届毕业生，目标岗位是"AI 应用工程师"。
本周我完成了一个学习项目，请基于以下素材帮我写成简历的"项目经历"：

【项目素材】
- 项目名称：DeepSeek API 多轮对话 AI 助手
- 完成时间：2026 年 5 月（7 天 AI 应用工程师学习计划的 Day 1）
- 技术栈：Python 3.12、OpenAI SDK（兼容 DeepSeek V4-Flash）、python-dotenv、Git/GitHub
- 核心功能：
  * 单轮对话：调用 DeepSeek API 实现基础问答
  * 多轮对话：通过维护 messages 历史数组，实现"对话记忆"
  * Token 用量统计：实时监控输入/输出 token 消耗
- 工程亮点：
  * 用 .env + python-dotenv 管理 API Key，符合密钥安全规范
  * 配置 .gitignore 防止敏感信息泄露
  * 生成 requirements.txt 锁定依赖版本
  * 使用 Conventional Commits 规范的 Git 提交
- 技术深度：
  * 掌握 OpenAI 兼容接口规范（system/user/assistant 三种 role）
  * 理解大模型"无状态"本质和"客户端维护历史"的多轮对话实现机制
  * 了解 token 计费模型和上下文窗口限制
- 项目地址：github.com/zwty999/ai-learning

[任务]
请把以上素材整合成简历里的"项目经历"条目。

[约束]
1. 字数：80-120 字之间（简历项目经历的黄金长度）
2. 视角：用"主动动词"开头（实现、设计、构建、优化），避免被动语态
3. 突出"AI 应用工程师"岗位匹配点（大模型 API 调用、多轮对话、工程规范）
4. 避免空话："拥有较强学习能力"、"对 AI 感兴趣"这类不要写
5. 优先体现"具体技术 + 具体动作 + 具体成果"
6. 不要使用过于初级的措辞（如"做了一个练习"、"学会了"），用专业项目化表述

[输出格式]
按以下模板输出，不要加任何额外说明或解释：

【项目名称】（一行，可加副标题）

【项目周期】XX 月 - XX 月

【技术栈】用 · 或 / 分隔的关键词列表

【项目描述】2-3 行段落，包含：是什么、用了什么技术、实现了什么核心功能

【主要工作】用 3-4 个 bullet point，每条以主动动词开头，包含具体技术细节和工程亮点"""

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": prompt}],
)

print(response.choices[0].message.content)