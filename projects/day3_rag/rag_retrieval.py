"""
Day 3 - RAG 检索系统
流程：加载文档 → 切分 → 向量化存入 Chroma → 检索
"""

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()


# ===== 1. 加载文档 =====
print("📄 步骤 1：加载知识库文档...")
loader = TextLoader("company_handbook.txt", encoding="utf-8")
documents = loader.load()
print(f"   加载完成，共 {len(documents)} 个文档对象")
print(f"   文档总字数：{len(documents[0].page_content)} 字\n")


# ===== 2. 切分文档（Chunking）=====
print("✂️ 步骤 2：切分文档...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=0,
    separators=["\n\n"],
)
chunks = text_splitter.split_documents(documents)
print(f"   切分完成，共 {len(chunks)} 个 chunk\n")

print("   📋 前 3 个 chunk 预览：")
for i, chunk in enumerate(chunks[:3]):
    preview = chunk.page_content.replace("\n", " ")[:50]
    print(f"   [chunk {i}] {preview}...")
print()


# ===== 3. 配置 Embedding（用硅基流动）=====
print("🔢 步骤 3：配置 Embedding 模型...")
embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL"),
)
print("   Embedding 配置完成\n")


# ===== 4. 向量化 + 存入 Chroma =====
print("💾 步骤 4：把 chunks 向量化并存入 Chroma 向量库...")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)
print("   向量库构建完成\n")


# ===== 5. 检索测试 =====
print("=" * 60)
print("🔍 步骤 5：检索测试")
print("=" * 60)

def search(query: str, k: int = 2):
    """检索：找出最相关的 k 个 chunk"""
    print(f"\n🧑 问题：{query}")
    results = vectorstore.similarity_search_with_score(query, k=k)
    print(f"📚 检索到最相关的 {k} 个片段：")
    for i, (doc, score) in enumerate(results):
        content = doc.page_content.replace("\n", " ")
        print(f"   [{i+1}] (距离={score:.4f}) {content}")


search("退货要几天能到账？")
search("我想请假，要怎么操作？")
search("公司有什么福利？")