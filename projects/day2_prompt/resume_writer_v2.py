"""
Day 2 - Step 2-3: 用 PromptTemplate 重写简历生成器
核心升级：Prompt 模板化，支持任意项目复用
"""

import os
from dotenv import load_dotenv

from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


# ===== 1. 创建模型（和之前一样）=====
model = ChatDeepSeek(
    model=os.getenv("DEEPSEEK_MODEL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base=os.getenv("DEEPSEEK_BASE_URL"),
)


# ===== 2. 创建 Prompt 模板（核心升级！）=====
# 注意：模板里用 {变量名} 占位，later 会被替换
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一名资深 IT 行业 HR，主要招聘'{target_position}'岗位。"
        "你看过 1000+ 份候选人简历，深知一段优秀的项目经历应该有的样子："
        "3 秒钟能看清项目价值，关键词能匹配岗位 JD，具体动作而非空话。"
    ),
    (
        "user",
        """请把以下项目素材整合成简历的'项目经历'条目。

【项目素材】
- 项目名称：{project_name}
- 完成时间：{date}
- 技术栈：{tech_stack}
- 核心功能：{features}
- 工程亮点：{highlights}
- 项目地址：{repo_url}

【约束】
1. 字数 80-120 字
2. 用主动动词开头（实现、设计、构建、优化）
3. 突出'{target_position}'岗位匹配点
4. 避免空话（"学习能力强"、"对 AI 感兴趣"等不要写）
5. 用专业项目化表述

【输出格式】
按以下模板输出，不要加额外说明：

【项目名称】xxx

【项目周期】xxx

【技术栈】xxx · xxx · xxx

【项目描述】2-3 行段落

【主要工作】
- 主动动词 + 具体动作 + 工程亮点（3-4 条）"""
    )
])


# ===== 3. 准备变量数据（这就是"填空"）=====
project_data = {
    "target_position": "AI 应用工程师",
    "project_name": "DeepSeek API 多轮对话 AI 助手",
    "date": "2026 年 5 月",
    "tech_stack": "Python 3.12、OpenAI SDK（兼容 DeepSeek V4-Flash）、python-dotenv、Git/GitHub",
    "features": (
        "单轮对话（调用 DeepSeek API 实现基础问答）；"
        "多轮对话（通过维护 messages 历史数组实现对话记忆）；"
        "Token 用量实时统计"
    ),
    "highlights": (
        "用 .env + python-dotenv 管理 API Key；"
        "配置 .gitignore 防止泄露；"
        "生成 requirements.txt 锁定依赖；"
        "使用 Conventional Commits 规范"
    ),
    "repo_url": "github.com/zwty999/ai-learning",
}


# ===== 4. 模板 + 变量 → 真实 Prompt =====
# .invoke(变量字典) 会自动把模板里的 {变量名} 替换成真实值
prompt = prompt_template.invoke(project_data)

print("=" * 60)
print("📋 渲染后的 Prompt（看看模板填空效果）：")
print("=" * 60)
# 打印渲染后的消息（看一下模板被填成什么样了）
for msg in prompt.messages:
    print(f"\n[{msg.type.upper()}]")
    print(msg.content[:200] + "..." if len(msg.content) > 200 else msg.content)
print("\n")


# ===== 5. 调用模型 =====
print("=" * 60)
print("🤖 调用 DeepSeek V4-Flash...")
print("=" * 60)
response = model.invoke(prompt)


# ===== 6. 输出结果 =====
print("\n📝 AI 生成的项目经历：\n")
print(response.content)
print()
print("=" * 60)
print(f"📊 Token: 输入 {response.usage_metadata.get('input_tokens')} | "
      f"输出 {response.usage_metadata.get('output_tokens')}")
print("=" * 60)