"""
Day 3 - Embedding 演示
亲眼看"文字变成向量" + "语义相似度计算"
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# ===== 1. 创建硅基流动客户端（兼容 OpenAI 接口）=====
client = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL"),
)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


# ===== 2. 定义一个"获取向量"的函数 =====
def get_embedding(text: str) -> list[float]:
    """把一段文字转成向量"""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


# ===== 3. 定义"计算余弦相似度"的函数 =====
def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """计算两个向量的余弦相似度
    
    公式：cos(θ) = (A·B) / (|A| × |B|)
    返回值范围 -1 到 1，越接近 1 越相似
    """
    # 点积 A·B
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    # 向量长度 |A| 和 |B|
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    # 余弦相似度
    return dot_product / (magnitude_a * magnitude_b)


# ===== 4. 准备测试句子 =====
sentence_A = "退货要几天？"
sentence_B = "本公司提供 30 天无理由退货"
sentence_C = "我想咨询退款政策"
sentence_D = "今天天气真好，适合出去玩"


# ===== 5. 生成向量 =====
print("🔄 正在生成向量...\n")
vec_A = get_embedding(sentence_A)
vec_B = get_embedding(sentence_B)
vec_C = get_embedding(sentence_C)
vec_D = get_embedding(sentence_D)


# ===== 6. 看看向量长什么样 =====
print("=" * 60)
print(f"📊 句子 A：「{sentence_A}」")
print(f"   向量维度：{len(vec_A)} 个数字")
print(f"   向量前 5 个数字：{[round(x, 4) for x in vec_A[:5]]}")
print("=" * 60)


# ===== 7. 计算相似度 =====
print("\n🔍 计算句子 A 和其他句子的语义相似度：\n")
print(f"A vs B「{sentence_B}」")
print(f"   相似度：{cosine_similarity(vec_A, vec_B):.4f}")
print()
print(f"A vs C「{sentence_C}」")
print(f"   相似度：{cosine_similarity(vec_A, vec_C):.4f}")
print()
print(f"A vs D「{sentence_D}」")
print(f"   相似度：{cosine_similarity(vec_A, vec_D):.4f}")
print()

print("=" * 60)
print("👀 观察：A 和 B、C（都和退货相关）相似度应该高")
print("       A 和 D（天气，无关）相似度应该低")
print("=" * 60)