# AI 应用开发实战项目

> 7 天从零到 AI 应用工程师的系统学习项目 —— 涵盖 RAG、Agent、LangChain 等核心技术栈

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)]()
[![LangChain](https://img.shields.io/badge/LangChain-1.x-green.svg)]()

## 📖 项目简介

本项目是系统学习 **AI 应用开发**的完整实战记录，从环境搭建出发，逐步实现了 **API 调用、Prompt 工程、RAG 检索增强生成、多工具智能 Agent** 等核心 AI 应用场景，并完成了两个带 Web 界面的可演示产品。

**两个核心项目：**

- 🔍 **企业知识库 RAG 问答系统** —— 基于检索增强生成，支持文档上传、智能问答、来源追溯、防幻觉
- 🤖 **多工具智能 Agent** —— 基于 Function Calling，集成知识库检索(RAG)、计算、时间查询，自主决策调用工具

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 编程语言 | Python 3.12 |
| 大模型 | DeepSeek V4-Flash（OpenAI 兼容接口） |
| 应用框架 | LangChain（create_agent、LCEL） |
| 向量数据库 | Chroma |
| Embedding | BAAI/bge-m3（硅基流动） |
| Web 界面 | Streamlit |
| 核心技术 | RAG、Agent、Function Calling、Prompt 工程 |
| 工程工具 | Git、虚拟环境、模块化开发 |

## 📁 项目结构

```text
ai-learning/
├── projects/
│   ├── day1_api_call/          # API 调用基础
│   │   ├── hello_deepseek.py   # 单轮对话
│   │   └── chat_loop.py        # 多轮对话
│   ├── day2_prompt/            # Prompt 工程 + LangChain
│   │   ├── prompt_compare.py   # Prompt 对比
│   │   ├── resume_writer.py    # 简历生成器
│   │   ├── translator_lcel.py  # LCEL 链式调用
│   │   └── agent_demo.py       # 初探 Agent
│   ├── day3_rag/               # RAG 核心原理
│   │   ├── embedding_demo.py   # 向量化演示
│   │   ├── rag_retrieval.py    # 检索演示
│   │   └── rag_complete.py     # 完整 RAG 流程
│   ├── day4_rag_app/           # RAG Web 应用 ⭐项目1
│   │   ├── rag_core.py         # RAG 核心逻辑
│   │   └── app.py              # Streamlit 界面
│   └── day5_agent/             # 多工具 Agent ⭐项目2
│       ├── agent_tools.py      # 工具集（RAG+计算+时间）
│       ├── agent_app.py        # 命令行 Agent
│       └── agent_streamlit.py  # Agent Web 界面
├── .env.example                # 环境变量示例（不含密钥）
├── .gitignore
├── requirements.txt            # 项目依赖
└── README.md
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/zwty999/ai-learning.git
cd ai-learning
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的密钥：

```text
DEEPSEEK_API_KEY=你的Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
SILICONFLOW_API_KEY=你的Key
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
EMBEDDING_MODEL=BAAI/bge-m3
```

### 5. 运行核心项目

```bash
# 项目1：RAG 问答系统（Web 界面）
streamlit run projects/day4_rag_app/app.py

# 项目2：多工具 Agent（Web 界面）
streamlit run projects/day5_agent/agent_streamlit.py
```

## 💡 核心项目说明

### 🔍 项目1：企业知识库 RAG 问答系统

基于 **RAG（检索增强生成）** 技术，解决大模型「不知道私有知识、容易幻觉、知识更新难」三大痛点。

- **完整 RAG 流程**：文档切分(Chunking) → 向量化(Embedding) → 语义检索 → 检索增强 → 生成
- **技术亮点**：通过 Chunking 策略调优解决检索质量问题；通过 Prompt 约束抑制幻觉，确保回答严格基于知识库
- **产品功能**：文档上传、多轮对话、检索来源追溯

### 🤖 项目2：多工具智能 Agent

基于 **Function Calling** 机制实现的多工具智能体，能根据用户意图**自主决策**调用合适的工具。

- **集成工具**：知识库检索(RAG)、数学计算、时间查询
- **架构亮点**：将 RAG 系统封装为 Agent 的一个工具，实现 **RAG + Agent 融合架构**
- **可视化**：Web 界面展示 Agent 的工具调用决策过程

## 📚 学习进度

- [x] Day 1：环境搭建 + API 调用 + 多轮对话
- [x] Day 2：Prompt 工程 + LangChain 入门（LCEL、create_agent）
- [x] Day 3：RAG 核心原理 + 向量数据库
- [x] Day 4：完整 RAG 项目实战（Web 应用）
- [x] Day 5：Function Calling + 多工具 Agent
- [x] Day 6：项目打磨 + 知识体系梳理
- [x] Day 7：简历定稿 + 模拟面试

## 🎯 核心知识点

**基础层**
- 大模型 API 调用规范（OpenAI 兼容接口）、messages 三角色、Token 计费、多轮对话「无状态 + 历史维护」机制

**框架层**
- LangChain 三大抽象、LCEL 管道符（Runnable 协议）、create_agent

**RAG**
- Embedding 语义向量化、Chunking 切分策略、Chroma 向量库、检索增强生成、防幻觉 Prompt 约束

**Agent**
- Function Calling（大模型决策 / 代码执行）、工具决策机制（docstring）、ReAct、RAG 与 Agent 融合架构

**工程实践**
- 虚拟环境隔离、依赖管理、API 密钥安全（.env + .gitignore）、模块化开发、Streamlit 产品化

## 📝 学习笔记

详细学习笔记与知识体系梳理见飞书文档。

## 📄 License

本项目仅供学习交流使用。
