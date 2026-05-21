"""
Day 5 - Agent 工具集
把 RAG 封装成工具，加上计算器、时间工具
"""

import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader

load_dotenv()


# ========== 全局：构建知识库（启动时建一次）==========
def _build_knowledge_base():
    """启动时构建知识库向量库（内部函数，下划线开头表示私有）"""
    loader = TextLoader("company_handbook.txt", encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=0,
        separators=["\n\n"],
    )
    chunks = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL"),
        api_key=os.getenv("SILICONFLOW_API_KEY"),
        base_url=os.getenv("SILICONFLOW_BASE_URL"),
    )

    import shutil
    if os.path.exists("./chroma_db_agent"):
        shutil.rmtree("./chroma_db_agent")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db_agent",
    )
    return vectorstore


# 启动时构建一次，全局复用
_vectorstore = _build_knowledge_base()


# ========== 工具1：查询公司知识库（RAG）==========
def search_knowledge_base(query: str) -> str:
    """当用户询问公司制度、政策、规定相关问题时使用此工具查询公司知识库。
    适用于：退货政策、请假流程、报销规定、福利待遇、考勤制度、设备管理、年假等问题。
    
    参数：
        query: 用户的问题
    返回：
        从知识库检索到的相关内容
    """
    results = _vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in results])
    return f"知识库检索结果：\n{context}"


# ========== 工具2：计算器 ==========
def calculator(expression: str) -> str:
    """计算数学表达式。当用户需要进行数学计算时使用。
    
    参数：
        expression: 数学表达式，如 "(100 + 50) * 3"
    返回：
        计算结果
    """
    try:
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算出错：{e}"


# ========== 工具3：获取当前时间 ==========
def get_current_time(query: str = "") -> str:
    """获取当前的日期和时间。当用户询问现在几点、今天日期时使用。
    
    返回：
        当前日期时间
    """
    now = datetime.now()
    return f"当前时间：{now.strftime('%Y年%m月%d日 %H:%M:%S')}"