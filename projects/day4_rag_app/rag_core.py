"""
RAG 核心逻辑模块
把 Day 3 的 RAG 拆成可复用的函数，供 Web 应用调用
"""

import os
import shutil
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

load_dotenv()


# ===== 配置 Embedding 模型 =====
def get_embeddings():
    """创建 Embedding 模型"""
    return OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL"),
        api_key=os.getenv("SILICONFLOW_API_KEY"),
        base_url=os.getenv("SILICONFLOW_BASE_URL"),
    )


# ===== 配置大模型 =====
def get_llm():
    """创建 DeepSeek 大模型"""
    return ChatDeepSeek(
        model=os.getenv("DEEPSEEK_MODEL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        api_base=os.getenv("DEEPSEEK_BASE_URL"),
        extra_body={"thinking": {"type": "disabled"}},
    )


# ===== 函数1：根据文本内容构建向量库 =====
def build_vectorstore(text: str, persist_dir: str = "./chroma_db_app"):
    """
    把一段文本切分、向量化，存入 Chroma 向量库
    
    参数：
        text: 知识库文本内容
        persist_dir: 向量库存储目录
    返回：
        vectorstore: 构建好的向量库对象
    """
    # 先清空旧库，防止重复入库
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    # 把文本包装成 Document 对象
    documents = [Document(page_content=text)]

    # 切分
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        separators=["\n\n", "\n", "。", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)

    # 向量化 + 存库
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=persist_dir,
    )
    return vectorstore, len(chunks)


# ===== 函数2：基于向量库回答问题 =====
def answer_question(vectorstore, question: str, k: int = 3):
    """
    完整 RAG 流程：检索 → 增强 → 生成
    
    参数：
        vectorstore: 向量库对象
        question: 用户问题
        k: 检索片段数量
    返回：
        answer: AI 回答
        sources: 检索到的来源片段列表
    """
    # ① 检索
    results = vectorstore.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in results])
    sources = [doc.page_content for doc in results]

    # ② 增强（拼 Prompt）
    rag_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """你是一个知识库问答助手。请严格根据下面提供的【参考资料】回答用户问题。

要求：
1. 只能根据参考资料回答，不要编造资料里没有的内容
2. 如果参考资料里没有相关信息，就回答"抱歉，知识库中没有相关信息"
3. 回答要简洁、准确

【参考资料】
{context}"""
        ),
        ("user", "{question}"),
    ])
    prompt = rag_prompt.invoke({"context": context, "question": question})

    # ③ 生成
    response = get_llm().invoke(prompt)

    return response.content, sources