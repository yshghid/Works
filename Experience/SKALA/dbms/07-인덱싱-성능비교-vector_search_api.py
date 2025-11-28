from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

os.chdir("/Users/yshmbid/Documents/home/github/SQL")  # set path
load_dotenv()  # .env 파일 로드

# FastAPI 앱 생성
app = FastAPI()

class QueryVector(BaseModel):
    vector: list[float]
    limit: int = 5

def get_db_conn():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=os.getenv("PG_PASSWORD"),
        host="localhost"
    )

@app.post("/search")
def search_vector(data: QueryVector):
    try:
        conn = get_db_conn()
        cur = conn.cursor()

        # content까지 포함
        query = """
            SELECT id, title, content
            FROM design_doc
            ORDER BY embedding_vector <=> %s::vector
            LIMIT %s;
        """

        # Python list → pgvector 문자열 변환
        vector_str = "[" + ",".join(map(str, data.vector)) + "]"

        cur.execute(query, (vector_str, data.limit))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {
            "results": [
                {"id": r[0], "title": r[1], "content": r[2]} for r in rows
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")