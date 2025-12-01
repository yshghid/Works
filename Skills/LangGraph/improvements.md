# 정확도 향상 아이디어

## 1) [P1] 요구사항 → API 매핑 정확도 향상: LLM Re-ranking 적용

### ① 예시 상황

**요구사항:**
- 사용자는 이메일과 비밀번호로 로그인할 수 있어야 한다.

**API 후보(embedding 검색 Top 3):**
- POST /auth/login
- POST /user/signup
- GET /auth/me

### ② 기존 방식 동작

- embedding cosine similarity만 사용
- POST /auth/login과 POST /user/signup가 비슷한 cosine score(0.78 vs 0.73)를 가진다면
- threshold만으로 판단하기 때문에
- signup이 login 요구사항에 잘못 매핑될 가능성 존재

**문제점:**
- 로그인·회원가입은 유사 단어 사용(auth, user 등)
- embedding만으로는 구별 어려움
- 오탐 발생

### ③ 개선: LLM 기반 Re-ranking

**동작 방식:**

상위 3개의 API만 LLM에게 넣음

아래와 같은 프롬프트로 질문:

```
요구사항: "사용자는 이메일과 비밀번호로 로그인할 수 있어야 한다."
아래 API 중 요구사항을 가장 잘 만족하는 순서대로 정렬해줘:

1. POST /auth/login: 이메일/비밀번호로 로그인
2. POST /user/signup: 회원가입 API
3. GET /auth/me: 내 인증 정보 조회
```

**LLM 판단 결과:**
- 정확히 Login → Signup → Me 순으로 재정렬.

**LLM의 이해:**
- "login" 행위 → 인증 → POST /auth/login
- signup은 "새 계정 생성"이므로 다른 기능
- GET /auth/me는 단순 조회

### ④ 기존 vs 개선 비교

| 항목 | 기존 Embedding만 사용 | LLM Re-ranking 적용 |
|------|---------------------|-------------------|
| 후보군 | login/signup/me | 동일 |
| 최종 선택 | login 또는 signup(오탐 가능) | login으로 100% 선택 |
| 신뢰도 관리 | cosine 기반 | LLM의 reasoning 기반 |
| 매핑 정확도 | 60~70% | 90~95% |

### ⑤ 개선 효과

- 오탐 감소 → 전체 매핑 정확도 대폭 상승
- LLM은 한국어·영어·도메인 지식을 모두 이해하므로
- 요구사항과 API 의미론적 매핑 품질이 크게 올라감.

---

## 2) [P2] API → Code 매핑 정확도 향상: Path Normalization 적용

### ① 예시 상황

**코드에서:**
```javascript
await client.get(`/products/${id}/details`);
```

**OpenAPI:**
```
GET /products/{productId}/details
```

### ② 기존 방식 동작

**매핑 로직:**
```
rawPath = "/products/123/details"
endpoint.path = "/products/{productId}/details"
```

문자열 비교를 수행하면 서로 다르다고 판단됨.

**문제점:**
- path param {productId} vs ${id}
- normalization이 없어서 매칭 실패
- → API–코드 관계가 끊겨버림

### ③ 개선: Path Token Normalization

**변환 예시:**

| 원본 문자열 | 정규화 결과 |
|-----------|-----------|
| /products/${id}/details | /products/:param/details |
| /products/{productId}/details | /products/:param/details |

→ 두 path가 동일 구조임을 인식 가능.

### ④ 기존 vs 개선 비교

| 항목 | 기존 | 개선 |
|------|------|------|
| 문자열 비교 | 불일치 | 일치 |
| ApiCallSite 매핑 | 누락 | 100% 매핑 |
| Component 사용 엔드포인트 추적 | 연결 실패 | 완전 연결 |
| 경우 | 10개 중 2~3개 누락 | 거의 10/10 정확 |

### ⑤ 개선 효과

- API 변경 영향도 분석 정확도↑
- REQ_IMPLEMENTED_IN_COMPONENT 연결 정확도↑
- Playwright 스크립트 생성 시 API오라클 정확도↑

---

## 3) [P3] 요구사항 → 소스코드 합성 정확도 향상: GNN(Graph Attention) Re-scoring

### ① 예시 상황

**Requirement → API 매핑은 다음과 같다고 하자:**

R1("장바구니에 제품 추가") → POST /cart/addItem

**Component–API 매핑:**
- CartPage가 해당 엔드포인트 호출
- ProductDetailPage도 호출(장바구니 버튼 존재)

둘 다 호출하므로 합성 후:
- R1 → CartPage
- R1 → ProductDetailPage

두 개 다 일단 연결됨.

### ② 기존 방식 동작

- 단순히 "API를 사용하는 모든 Component"를 연결
- 결과적으로 불필요한 연결(오탐) 많음

**문제점:**
- ProductDetailPage는 "장바구니 용도"가 아닌 데도 연결됨
- 실제 핵심 구현 컴포넌트는 CartPage인데 구분 불가

### ③ 개선: GNN 기반 Attention Re-scoring

**그래프 특성 사용:**
- Comp imports
- Comp routes
- Handler 이름(handleAddToCart vs openModal)
- Component type(Page/Service/Widget)
- callsite count

**GNN이 학습 후 판단:**
- CartPage: weight 0.92
- ProductDetailPage: weight 0.35
- → REQ_IMPLEMENTED_IN_COMPONENT confidence 조정

### ④ 기존 vs 개선 비교

| 항목 | 기존 | 개선(GNN) |
|------|------|----------|
| 연결 수 | R1 → CartPage, ProductDetailPage | R1 → CartPage(1개로 정리) |
| confidence | 둘 다 0.7 | CartPage: 0.92, ProductDetail: 0.35 |
| 오탐 | 많음 | 대폭 감소 |
| 최종 결과 | 페이지 두 개 연결 | 핵심 페이지 하나 식별 가능 |

### ⑤ 개선 효과

- 요구사항–UI 매핑 정확도 증가
- 테스트 시나리오 생성 시 "정확한 페이지 흐름" 제공
- Self-healing 근거 정확성 증가

---

# 속도 향상 아이디어

## 4) P1 최적화: Embedding Cache

### ① 예시 상황

- 요구사항 500개, API 200개
- 총 500 × 200 = 100,000 embedding 연산 필요

### ② 기존 방식

- 매번 전체 텍스트를 embedding → 매우 느림
- 한번 수행하는데 30~40초

### ③ 개선: Redis 또는 local SQLite에 embedding 캐싱

**동작 예시:**
```
key: SHA256(requirement fullText)
value: embedding vector (768-dim)
```

**재분석 시:**
```
if key in cache → load embedding in 0.2ms
else → embedding 생성 후 cache 저장
```

### ④ 기존 vs 개선 비교

| 항목 | 기존 | 개선 |
|------|------|------|
| embedding 100,000번 | 30~40초 | 1~3초 |
| 재분석 시 속도 | 40초 | 1초 미만 |
| 비용 | GPU/CPU 계속 사용 | 거의 없음 |

### ⑤ 개선 효과

- 임베딩 재생성 비용 90~95% 절감
- 요구사항/코드가 조금만 바뀌어도 매우 빠르게 재분석 가능

---

## 5) P2 속도 향상: AST Incremental Parsing

### ① 예시 상황

- 프론트엔드 코드 파일 2,000개
- 전체 파싱 시 20~30초 소요

요구사항만 수정됐는데 코드 분석이 다시 전부 실행됨 → 비효율.

### ② 기존 방식

- 모든 파일을 다시 파싱
- 매번 초기화해서 AST 생성

### ③ 개선: Incremental AST Parsing

**변경된 파일만 파싱:**
- git diff 로 changed file 목록 추출
- 기존 AST map 재사용

**예시:**
```
수정된 파일 7개
→ 7개만 파싱 (0.3초)
```

### ④ 기존 vs 개선 비교

| 항목 | 기존 | 개선 |
|------|------|------|
| 전체 파싱 시간 | 20~30초 | 0.3초 |
| 전체 CPU 사용량 | 높음 | 매우 낮음 |
| 전체 파이프라인 latency | 30초↑ | 2초 이내 |

### ⑤ 개선 효과

- 대규모 FE 프로젝트에서 속도 압도적으로 개선
- 실시간 테스트 영향도 분석에도 적합

---

## 6) P3 속도 향상: Neo4j Batch Insert (UNWIND 사용)

### ① 예시 상황

- Requirement 500개
- ApiEndpoint 200개
- Component 300개
- 간선 10,000개

### ② 기존 방식

```cypher
FOREACH edge → MERGE node, MERGE relationship
```

→ 관계 하나 만들 때마다 disk seek + lock  
→ 2~4분 걸림

### ③ 개선: batch insert

**예시 Cypher:**
```cypher
UNWIND $edges AS edge
MATCH (a {id: edge.from}), (b {id: edge.to})
CREATE (a)-[:REQ_SATISFIED_BY_ENDPOINT {confidence: edge.conf}]->(b)
```

한 번에 1000개씩 batch로 넣음

### ④ 기존 vs 개선 비교

| 항목 | 기존 | 개선 |
|------|------|------|
| 처리 속도 | 노드/간선 건당 MERGE → 느림 | UNWIND batch insert → 10~50x 빠름 |
| 전체 시간 | 3분 이상 | 5~10초 |

### ⑤ 개선 효과

- 초기 그래프 구축 속도 획기적 향상
- ETL 파이프라인 반복 실행 시 매우 유리

---

# 🎯 최종 핵심 요약

| 아이디어 | 예시 | 기존 | 개선 | 효과 |
|---------|------|------|------|------|
| LLM Re-ranking | 로그인 요구사항 | signup과 오탐 | login 정확 매핑 | 정확도 대폭 상승 |
| Path Normalization | /products/${id} | 매핑 실패 | 매핑 성공 | 코드–API 100% 매핑 |
| GNN Re-scoring | cart 요구사항 | 여러 component 연결 | 핵심 component만 연결 | 오탐 감소 |
| Embedding Cache | 10만 임베딩 | 40초 | 1초 | 속도 30~40x 개선 |
| Incremental Parsing | FE 2000파일 | 20~30초 | 0.3초 | 100x 개선 |
| Batch Insert | 1만 관계 | 2~3분 | 5~10초 | 10~50x 개선 |
