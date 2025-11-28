# app.py
# 9. RAG 구조 접목
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

os.chdir("/Users/yshmbid/Documents/home/github/SQL")
load_dotenv()

# FastAPI 앱
app = FastAPI()

# OpenAI 클라이언트
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# SentenceTransformer 임베딩 모델 로드
model = SentenceTransformer("all-MiniLM-L6-v2")

# 요청 모델
class Query(BaseModel):
    text: str
    topk: int = 5
    user_id: str | None = None  # 사용자 ID 필드 (옵션)

# pgvector 기반 검색 함수
def search_similar(query, topk=5, user_id=None):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password=os.getenv("PG_PASSWORD"),
    )
    cur = conn.cursor()

    q_emb = model.encode(query).tolist()
    q_emb_str = "[" + ",".join(map(str, q_emb)) + "]"

    if user_id:
        cur.execute(
            """
            SELECT id, title, description
            FROM issues
            WHERE user_id = %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """,
            (user_id, q_emb_str, topk),
        )
    else:
        cur.execute(
            """
            SELECT id, title, description
            FROM issues
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """,
            (q_emb_str, topk),
        )

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# RAG API
@app.post("/search_rag")
def search_rag(query: Query):
    # 1) pgvector 검색
    results = search_similar(query.text, query.topk, query.user_id)

    # 2) 프롬프트 구성
    context_text = "\n".join([f"- {r[1]}: {r[2]}" for r in results])
    prompt = f"""
    새로운 이슈: "{query.text}"
    아래는 DB에서 검색된 유사 이슈들입니다:
    {context_text}

    위 유사 이슈들을 참고해서,
    1) 공통된 문제 요약
    2) 잠재적인 원인
    3) 해결 방향 (가능하다면)
    을 간단히 정리해줘.
    """

    # 3) GPT 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for issue tracking."},
            {"role": "user", "content": prompt}
        ],
    )

    summary = response.choices[0].message.content

    return {
        "query": query.text,
        "results": results,
        "summary": summary
    }