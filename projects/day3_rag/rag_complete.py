"""
Day 3 - 完整 RAG 系统
检索（向量库）+ 生成（大模型）= 完整 RAG
"""

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


# ========== 第一部分：构建向量库（检索系统）==========
print("🔧 正在构建知识库...")

# 加载 + 切分
loader = TextLoader("company_handbook.txt", encoding="utf-8")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=0,
    separators=["\n\n"],
)
chunks = text_splitter.split_documents(documents)

# Embedding + 存向量库
embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL"),
)

# 先清空旧向量库，防止重复入库
import shutil
if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")
    print("   已清空旧向量库")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)
print("✅ 知识库构建完成\n")


# ========== 第二部分：大模型（生成系统）==========
model = ChatDeepSeek(
    model=os.getenv("DEEPSEEK_MODEL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base=os.getenv("DEEPSEEK_BASE_URL"),
    extra_body={"thinking": {"type": "disabled"}},   # 关闭 thinking 模式
)


# ========== 第三部分：RAG Prompt 模板 ==========
# ⭐ 这是 RAG 的灵魂：告诉大模型"只根据资料回答"
rag_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """你是一个公司制度问答助手。请严格根据下面提供的【参考资料】回答用户问题。

要求：
1. 只能根据参考资料回答，不要编造资料里没有的内容
2. 如果参考资料里没有相关信息，就回答"抱歉，知识库中没有相关信息"
3. 回答要简洁、准确

【参考资料】
{context}"""
    ),
    (
        "user",
        "{question}"
    ),
])


# ========== 第四部分：RAG 问答函数 ==========
def rag_answer(question: str):
    """完整 RAG 流程：检索 → 增强 → 生成"""
    print("=" * 60)
    print(f"🧑 用户问题：{question}")
    print("=" * 60)

    # ① 检索（向量库干的活）
    results = vectorstore.similarity_search(question, k=6)
    context = "\n\n".join([doc.page_content for doc in results])

    print(f"📚 检索到 {len(results)} 个片段：")
    for i, doc in enumerate(results):
        preview = doc.page_content.replace("\n", " ")[:40]
        print(f"   [{i+1}] {preview}...")
    print()

    # ② 增强（把资料填进 Prompt）
    prompt = rag_prompt.invoke({"context": context, "question": question})

    # ③ 生成（大模型干的活）
    response = model.invoke(prompt)

    print("🤖 RAG 回答：")
    print(f"   {response.content}\n")


# ========== 测试 ==========
rag_answer("退货多久能退款到账？")
rag_answer("年假有几天，能不能攒到明年？")
rag_answer("公司食堂几点开饭？")   # ⭐ 故意问一个知识库里【没有】的问题，看会不会瞎编