import requests
import psycopg2
import os
import ast
from dotenv import load_dotenv

os.chdir("/Users/yshmbid/Documents/home/github/SQL")  # set path 
load_dotenv()  # .env 파일 로드

# DB 연결
def get_db_conn():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=os.getenv("PG_PASSWORD"),
        host="localhost"
    )

# 기준 문서(id=1) 가져오기
conn = get_db_conn()
cur = conn.cursor()
cur.execute("SELECT id, title, content, embedding_vector FROM design_doc WHERE id = 1;")
row = cur.fetchone()
cur.close()
conn.close()

query_id, query_title, query_content, vec_raw = row

# 문자열 → float 리스트 변환
if isinstance(vec_raw, str):
    vec = ast.literal_eval(vec_raw)
else:
    vec = list(vec_raw)

print("=== 쿼리로 사용된 문서 ===")
print(f"id: {query_id}")
print(f"title: {query_title}")
print(f"content: {query_content}")

# API 요청 (가장 유사한 문서 1개)
response = requests.post(
    "http://127.0.0.1:8000/search",
    json={"vector": vec, "limit": 1}
)

print("=== 원본 API 응답 ===")
print(response.json())

# 결과가 있으면 하나만 출력
if "results" in response.json() and len(response.json()["results"]) > 0:
    r = response.json()["results"][0]
    print("\n=== 가장 유사한 문서 ===")
    print(f"id: {r['id']}")
    print(f"title: {r['title']}")
    print(f"content: {r['content']}")
