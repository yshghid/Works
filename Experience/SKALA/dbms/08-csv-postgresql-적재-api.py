# 6. FastAPI 서버
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2, os
from dotenv import load_dotenv

os.chdir("/Users/yshmbid/Documents/home/github/SQL")
load_dotenv() 

app = FastAPI()

class RecommendRequest(BaseModel):
    user_id: str

def get_conn():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password=os.getenv("PG_PASSWORD"),
    )

@app.post("/recommend")
def recommend(req: RecommendRequest):
    conn = get_conn()
    cur = conn.cursor()
    # user_embeddings 기준으로 유사도 검색 + user_behavior join
    cur.execute("""
        SELECT ub.user_id, ub.age, ub.income, ub.gender
        FROM user_behavior ub
        JOIN user_embeddings ue ON ub.user_id = ue.user_id
        ORDER BY ue.embedding <=> (SELECT embedding FROM user_embeddings WHERE user_id = %s)
        LIMIT 5;
    """, (req.user_id,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return {"recommendations": results}