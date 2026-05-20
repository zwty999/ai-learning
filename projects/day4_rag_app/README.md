# 📚 企业知识库智能问答助手

> 基于 RAG（检索增强生成）技术的知识库问答系统，支持文档上传、智能问答、来源追溯。

![tech](https://img.shields.io/badge/LangChain-1.x-blue) ![tech](https://img.shields.io/badge/Streamlit-Web-red) ![tech](https://img.shields.io/badge/DeepSeek-LLM-green) ![tech](https://img.shields.io/badge/Chroma-VectorDB-orange)

## 🎯 项目简介

这是一个企业级知识库问答助手，用户上传内部文档后，可以用自然语言提问，系统基于 RAG 技术从文档中检索相关内容，并生成准确、有据可依的回答，有效解决大模型「不懂私有知识」和「幻觉」两大问题。

## ✨ 核心功能

- 📄 **文档上传**：支持上传 .txt 知识库文档，一键构建向量知识库
- 💬 **智能问答**：基于检索增强生成，回答严格依据文档内容
- 📎 **来源追溯**：每个回答可展开查看检索到的原文片段，可信可验证
- 🛡️ **防幻觉**：知识库中没有的信息，明确告知「没有相关信息」，不编造
- 🔄 **多轮对话**：支持连续提问，保留对话历史

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| 大语言模型 | DeepSeek V4-Flash |
| 文本嵌入 | BAAI/bge-m3（硅基流动）|
| 向量数据库 | Chroma |
| 应用框架 | LangChain 1.3.1 |
| Web 界面 | Streamlit |

## 🏗️ 系统架构

\`\`\`
用户提问
   ↓
[检索 Retrieval] 向量库计算相似度，召回最相关的文档片段
   ↓
[增强 Augmented] 把检索片段 + 问题拼成 Prompt
   ↓
[生成 Generation] DeepSeek 基于资料生成答案
   ↓
返回答案 + 来源片段
\`\`\`

## 🚀 快速开始

### 1. 安装依赖
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. 配置环境变量
在项目根目录创建 \`.env\` 文件：
\`\`\`env
DEEPSEEK_API_KEY=你的DeepSeek密钥
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
SILICONFLOW_API_KEY=你的硅基流动密钥
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
EMBEDDING_MODEL=BAAI/bge-m3
\`\`\`

### 3. 运行应用
\`\`\`bash
streamlit run app.py
\`\`\`
浏览器自动打开 http://localhost:8501

## 📂 项目结构

\`\`\`
day4_rag_app/
├── app.py              # Streamlit 主界面
├── rag_core.py         # RAG 核心逻辑（构建知识库、问答）
├── company_handbook.txt # 示例知识库文档
└── README.md
\`\`\`

## 💡 工程亮点

- **模块化设计**：RAG 核心逻辑与界面分离，便于复用和测试
- **Chunking 调优**：针对结构化文档优化切分策略，保证检索精度
- **状态管理**：使用 session_state 持久化向量库和对话历史，避免重复构建
- **来源透明**：展示检索来源，提升答案可信度和可追溯性