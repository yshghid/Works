from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI
import os

# 경로 설정
os.chdir("/Users/yshmbid/Documents/home/github/SQL")

# .env 로드
load_dotenv()

# OpenAI 클라이언트
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# DB 연결
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password=os.getenv("PG_PASSWORD"),
)
cursor = conn.cursor()

# FastAPI 앱 객체 생성
app = FastAPI()

# 요청 데이터 모델 정의
class DesignRequest(BaseModel):
    description: str

# 임베딩 함수
def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

@app.post("/register_design")
def register_design(req: DesignRequest):
    try:
        cursor.execute("BEGIN;")
        embedding = get_embedding(req.description)

        cursor.execute(
            "INSERT INTO design (description, embedding) VALUES (%s, %s)",
            (req.description, embedding)
        )
        conn.commit()
        return {"status": "success", "message": "등록 성공"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"등록 실패: {e}")