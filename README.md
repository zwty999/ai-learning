# AI 应用开发学习项目

> 7 天从零到 AI 应用工程师的实战学习项目

## 📖 项目简介

本项目是一个系统学习 **AI 应用开发** 的代码与笔记仓库，从环境搭建开始，逐步实现：API 调用、Prompt 工程、RAG 检索增强、Agent 智能体等核心 AI 应用场景。

## 🛠️ 技术栈

- **语言**：Python 3.12
- **大模型**：DeepSeek V4-Flash（OpenAI 兼容接口）
- **核心库**：openai, python-dotenv
- **后续规划**：LangChain, ChromaDB, FastAPI, Streamlit

## 📁 项目结构

```text
ai-learning/
├── notes/                       # 学习笔记
│   └── day1_环境与API调用.md
├── projects/                    # 每日项目代码
│   └── day1_api_call/
│       ├── hello_deepseek.py    # 单轮对话 Demo
│       └── chat_loop.py         # 多轮对话 Demo
├── .env.example                 # 环境变量示例（不含密钥）
├── .gitignore
├── requirements.txt             # 项目依赖
└── README.md
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <你的仓库地址>
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

复制 `.env.example` 为 `.env`，填入你的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=你的Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

### 5. 运行 Demo

```bash
# 单轮对话
python projects/day1_api_call/hello_deepseek.py

# 多轮对话（推荐）
python projects/day1_api_call/chat_loop.py
```

## 📚 学习进度

- [x] Day 1：环境搭建 + API 调用 + 多轮对话
- [ ] Day 2：Prompt 工程 + LangChain 入门
- [ ] Day 3：RAG 核心原理 + 向量数据库
- [ ] Day 4：完整 RAG 项目实战
- [ ] Day 5：Function Calling + Agent
- [ ] Day 6：项目打磨 + 八股复习
- [ ] Day 7：简历定稿 + 模拟面试

## 💡 核心知识点

- 大模型 API 调用规范（OpenAI 兼容接口）
- messages 数组与 system / user / assistant 角色
- 多轮对话的"无状态 + 历史维护"机制
- Token 计费与上下文窗口
- Python 工程化（虚拟环境、依赖管理、密钥安全）

## 📝 学习笔记

详细笔记请见 [`notes/`](./notes/) 目录。

## 📄 License

本项目仅供学习交流使用。