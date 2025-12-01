# AI 기반 UI 테스트 자동화 지식그래프 설계 보고서

## 1. 개요

### 1.1 배경

본 프로젝트는 웹 서비스의 **요구사항–API–프론트엔드 소스코드**를 자동으로 연계하여:

- 비즈니스 요구사항 기반 테스트 시나리오/오라클 생성
- Playwright 테스트 스크립트 자동 생성
- UI/코드/API 변경 시 영향도 분석 및 자가치유(Self-healing) 테스트

를 가능한 **AI 기반 UI 테스트 자동화 서비스**를 목표로 한다.

현재 입력 데이터는 다음 세 가지 JSON 분석 결과이다.

- `requirement.json`  
  → 요구사항 분석 결과 (요구사항 트리, 제목, 설명, AC 등)
- `api.json`  
  → API 엔드포인트 분석 결과 (OpenAPI 기반, summary/description, 필드 정보 등)
- `source_code.json`  
  → 프론트엔드 소스코드 분석 결과 (컴포넌트, 메서드, 컴포넌트 간 호출 관계 등)

이 보고서는 위 세 JSON을 기반으로 **그래프 DB 스키마(노드, 간선, 속성)**를 정의하고,  
이를 실제 그래프 DB(예: Neo4j)에 적재·활용하기 위한 **구현 계획**을 제시한다.

### 1.2 전체 방향

직접적인 “요구사항 → 엔드포인트” 매핑 정보가 없기 때문에, 아래 전략을 사용한다.

1. **요구사항–API 매핑**  
   - 요구사항(영어 텍스트) ↔ API description/summary(한국어 텍스트)를  
     다국어 임베딩 + 도메인/구조 정보로 매칭하여  
   - `Requirement --REQ_SATISFIED_BY_ENDPOINT--> ApiEndpoint` 간선 생성

2. **API–소스코드 매핑**  
   - 프론트엔드 코드(AST 기반)에서 HTTP 호출 지점을 추출하여  
   - `ApiCallSite --CALLSITE_CALLS_ENDPOINT--> ApiEndpoint`  
   - `Component/Method --COMP_USES_ENDPOINT / METHOD_CALLS_ENDPOINT--> ApiEndpoint`  
     관계를 코드 기반으로 생성

3. **요구사항–소스코드 매핑 (합성)**  
   - 위 두 레이어를 합성하여  
   - `Requirement --REQ_IMPLEMENTED_IN_COMPONENT--> Component`  
   - (옵션) `Requirement --REQ_IMPLEMENTED_IN_METHOD--> Method`  
     관계를 생성하여 traceability를 완성

---

## 2. 그래프 모델링 개요

### 2.1 논리 구조

그래프는 크게 세 개의 레이어로 구성된다.

- **요구사항 레이어**
  - `Requirement` 노드
  - 요구사항 계층 구조: `REQ_PARENT_OF`

- **API 레이어**
  - `ApiEndpoint` 노드
  - (옵션) `ApiField` 노드
  - 엔드포인트–필드 구조: `ENDPOINT_PRODUCES_FIELD`, `ENDPOINT_CONSUMES_FIELD` 등

- **소스코드 레이어**
  - `Component` 노드 (페이지/서비스/공통 컴포넌트)
  - (옵션) `Method` 노드
  - (향후) `ApiCallSite` 노드
  - 컴포넌트/메서드/호출 구조: `COMP_IMPORTS_COMPONENT`, `COMP_CALLS_COMPONENT`, `COMP_HAS_METHOD`, `METHOD_HAS_CALLSITE` 등

이 세 레이어를 연결하는 핵심 브리지 관계는 다음과 같다.

- `Requirement --REQ_SATISFIED_BY_ENDPOINT--> ApiEndpoint`  
- `Component/Method/ApiCallSite --*_CALLS_ENDPOINT--> ApiEndpoint`  
- 합성 결과:  
  `Requirement --REQ_IMPLEMENTED_IN_COMPONENT/REQ_IMPLEMENTED_IN_METHOD--> Component/Method`

---

## 3. 그래프 DB 스키마 설계

아래 스키마는 Neo4j 스타일의 **Property Graph**를 기준으로 한다.

### 3.1 노드 스키마

#### 3.1.1 Requirement 노드

**라벨**: `:Requirement`  
**예시 ID**: `req:R1.1.1.4`

| 필드명          | 타입            | 설명                                                |
|-----------------|-----------------|-----------------------------------------------------|
| `id`            | string (unique) | 요구사항 ID (`req:R1.1.1.4` 등)                     |
| `title`         | string          | 요구사항 제목                                      |
| `description`   | string          | 요구사항 상세 설명                                 |
| `category`      | string          | `"business"`, `"ui"`, `"api"` 등                    |
| `priority`      | string          | `"MUST"`, `"SHOULD"`, `"COULD"` 등                  |
| `acceptanceCriteria` | list<string> | AC 목록                                            |
| `tags`          | list<string>    | 도메인/기능 태그 (auth, product, cart, …)          |
| `projectId`     | string          | 프로젝트 ID                                        |
| `version`       | string          | 요구사항 버전                                      |
| `level`         | int             | 요구사항 계층 깊이 (1~N)                           |
| `domain`        | string          | 도메인 추론 값 (auth, product, order, …)           |
| `fullText`      | string          | title+description+AC+tags를 합친 검색용 텍스트     |

**제약/인덱스**

```cypher
CREATE CONSTRAINT requirement_id IF NOT EXISTS
ON (r:Requirement) ASSERT r.id IS UNIQUE;
```

`domain`, `priority`, `fullText`는 인덱스/풀텍스트 인덱스로 추가 가능.

---

#### 3.1.2 ApiEndpoint 노드

**라벨**: `:ApiEndpoint`  
**예시 ID**: `"POST /auth/login"`

| 필드명          | 타입            | 설명                                               |
|-----------------|-----------------|----------------------------------------------------|
| `id`            | string (unique) | `"METHOD PATH"` 형식 (예: `"POST /auth/login"`)   |
| `method`        | string          | `"GET"`, `"POST"`, `"PUT"`, `"DELETE"`, …         |
| `path`          | string          | `"/auth/login"`, `"/products/{id}"` 등            |
| `summary`       | string          | API 요약 (한국어)                                  |
| `description`   | string          | API 상세 설명                                      |
| `tags`          | list<string>    | OpenAPI tags (`["Authentication"]`, `["Products"]`)|
| `requiresAuth`  | boolean         | 인증 필요 여부                                    |
| `requestFields` | list<string>    | 요청 필드명 목록                                   |
| `responseFields`| list<string>    | 응답 필드명 목록                                   |
| `apiTitle`      | string          | API 문서 제목                                      |
| `apiVersion`    | string          | API 문서 버전                                      |
| `projectId`     | string          | 프로젝트 ID                                        |
| `resource`      | string          | 리소스명 (auth, products, cart, orders, …)         |
| `operationType` | string          | `"READ"`, `"CREATE"`, `"UPDATE"`, `"DELETE"`, `"AUTH"` |
| `pathTokens`    | list<string>    | path를 토큰화한 값 (`["auth","login"]` 등)        |

**제약/인덱스**

```cypher
CREATE CONSTRAINT api_endpoint_id IF NOT EXISTS
ON (e:ApiEndpoint) ASSERT e.id IS UNIQUE;
```

---

#### 3.1.3 ApiField 노드 (옵션, 추천)

**라벨**: `:ApiField`  
**예시 ID**: `"ApiField:POST /auth/login:request.email"`

| 필드명         | 타입            | 설명                                              |
|----------------|-----------------|---------------------------------------------------|
| `id`           | string (unique) | 엔드포인트 + 위치 기반 ID                         |
| `name`         | string          | 필드명 (email, price, cartId, …)                  |
| `in`           | string          | `"request"`, `"response"`, `"path"`, `"query"`    |
| `locationPath` | string          | `products[].price`, `shippingAddress.city`, …     |
| `type`         | string          | `"string"`, `"integer"`, `"number"`, `"object"`…  |
| `description`  | string          | 필드 설명 (있을 경우)                             |
| `isIdentifier` | boolean         | id, cartId, orderId 등 식별자 여부                |
| `businessConcept` | string       | user, product, cart, order 등 도메인 개념         |

**제약**

```cypher
CREATE CONSTRAINT api_field_id IF NOT EXISTS
ON (f:ApiField) ASSERT f.id IS UNIQUE;
```

---

#### 3.1.4 Component 노드

**라벨**: `:Component`  
**예시 ID**: `"comp:LoginPage"`

| 필드명      | 타입            | 설명                                               |
|-------------|-----------------|----------------------------------------------------|
| `id`        | string (unique) | `"comp:LoginPage"` 등                              |
| `name`      | string          | 컴포넌트 이름 (LoginPage, AuthService, …)         |
| `filePath`  | string          | 소스 파일 경로 (`src/pages/LoginPage.jsx`)        |
| `type`      | string          | `"page"`, `"service"`, `"component"` 등           |
| `routes`    | list<string>    | 페이지 라우트 (`["/login"]` 등)                   |
| `exports`   | list<string>    | export된 이름 목록                                 |
| `projectId` | string          | 프로젝트 ID                                       |
| `version`   | string          | 코드베이스 버전                                   |
| `isPage`    | boolean         | type=="page" 여부                                 |
| `isService` | boolean         | type=="service" 여부                              |

**제약**

```cypher
CREATE CONSTRAINT component_id IF NOT EXISTS
ON (c:Component) ASSERT c.id IS UNIQUE;
```

---

#### 3.1.5 Method 노드 (옵션)

**라벨**: `:Method`  
**예시 ID**: `"Method:LoginPage.handleLogin"`

| 필드명       | 타입            | 설명                                             |
|--------------|-----------------|--------------------------------------------------|
| `id`         | string (unique) | `"Method:<ComponentName>.<methodName>"`         |
| `name`       | string          | 메서드 이름 (handleLogin, login, …)            |
| `type`       | string          | `"function"` 등                                  |
| `async`      | boolean         | async 여부                                       |
| `visibility` | string          | `"public"`, `"private"` 등                       |
| `filePath`   | string          | 메서드 정의 파일 경로                           |
| `componentId`| string          | 소속 컴포넌트 ID                                 |

---

#### 3.1.6 ApiCallSite 노드 (향후 AST 확장)

**라벨**: `:ApiCallSite`  
**예시 ID**: `"ApiCallSite:src/pages/LoginPage.jsx:28"`

| 필드명        | 타입            | 설명                                             |
|---------------|-----------------|--------------------------------------------------|
| `id`          | string (unique) | 파일 + 라인 기반 ID                             |
| `filePath`    | string          | 호출이 위치한 파일                              |
| `line`        | int             | 호출 라인 번호                                   |
| `rawExpression` | string        | 원본 코드 스니펫 (`await login(...)` 등)        |
| `method`      | string\|null    | 추론된 HTTP 메서드                              |
| `path`        | string\|null    | 추론된 HTTP 경로                                |
| `library`     | string\|null    | axios, fetch, custom 등                         |
| `componentId` | string          | 소속 컴포넌트 ID                                 |

---

### 3.2 관계(간선) 스키마

#### 3.2.1 요구사항 계층

**타입**: `:REQ_PARENT_OF`  
**패턴**: `(:Requirement)-[:REQ_PARENT_OF]->(:Requirement)`

| 속성명       | 타입   | 설명                                      |
|--------------|--------|-------------------------------------------|
| `relationType` | string | `"structural"`                           |
| `levelDiff`  | int    | 상위/하위 요구사항 간 깊이 차 (보통 1)   |

---

#### 3.2.2 요구사항–API 매핑

**타입**: `:REQ_SATISFIED_BY_ENDPOINT`  
**패턴**: `(:Requirement)-[:REQ_SATISFIED_BY_ENDPOINT]->(:ApiEndpoint)`

| 속성명        | 타입    | 설명                                                       |
|---------------|---------|------------------------------------------------------------|
| `confidence`  | float   | 0~1, 자연어+도메인 기반 매칭 신뢰도                       |
| `evidenceType`| string  | `"text_similarity"`, `"tag_match"`, `"hybrid"` 등          |
| `evidenceText`| string  | 매칭에 사용된 요구사항 텍스트 일부                         |
| `role`        | string  | `"primary"`, `"supporting"` (핵심 엔드 vs 보조 엔드)       |

---

#### 3.2.3 요구사항–필드 매핑 (옵션)

**타입**: `:REQ_CONSTRAINS_FIELD`  
**패턴**: `(:Requirement)-[:REQ_CONSTRAINS_FIELD]->(:ApiField)`

| 속성명          | 타입   | 설명                                                    |
|-----------------|--------|---------------------------------------------------------|
| `constraintType`| string | `"min"`, `"max"`, `"required"`, `"format"`, `"enum"` 등 |
| `constraintValue` | string | `"1"`, `"99"`, `"email format"` 등                    |
| `evidenceText`  | string | AC 일부                                                 |

---

#### 3.2.4 엔드포인트–필드 관계

- `(:ApiEndpoint)-[:ENDPOINT_PRODUCES_FIELD]->(:ApiField)`  
- `(:ApiEndpoint)-[:ENDPOINT_CONSUMES_FIELD]->(:ApiField)`  
- `(:ApiEndpoint)-[:ENDPOINT_HAS_PATH_PARAM]->(:ApiField)`  
- `(:ApiEndpoint)-[:ENDPOINT_HAS_QUERY_PARAM]->(:ApiField)`

공통 속성:

| 속성명     | 타입   | 설명                               |
|------------|--------|------------------------------------|
| `required` | boolean| 필수 여부                          |
| `schemaPath` | string | 응답/요청 내 경로 (`items[].price`) |

---

#### 3.2.5 컴포넌트 간 관계

1. **Import 관계**

   - 타입: `:COMP_IMPORTS_COMPONENT`
   - 패턴: `(:Component)-[:COMP_IMPORTS_COMPONENT]->(:Component)`
   - 속성:
     - `line`: int
     - `context`: string (import 문)

2. **호출 관계**

   - 타입: `:COMP_CALLS_COMPONENT`
   - 패턴: `(:Component)-[:COMP_CALLS_COMPONENT]->(:Component)`
   - 속성:
     - `line`: int
     - `context`: string (호출 코드)

---

#### 3.2.6 컴포넌트–메서드 관계

- 타입: `:COMP_HAS_METHOD`
- 패턴: `(:Component)-[:COMP_HAS_METHOD]->(:Method)`

---

#### 3.2.7 메서드–ApiCallSite 관계

- 타입: `:METHOD_HAS_CALLSITE`
- 패턴: `(:Method)-[:METHOD_HAS_CALLSITE]->(:ApiCallSite)`
- 속성:
  - `line`: int
  - `context`: string

---

#### 3.2.8 ApiCallSite–ApiEndpoint 매핑

- 타입: `:CALLSITE_CALLS_ENDPOINT`
- 패턴: `(:ApiCallSite)-[:CALLSITE_CALLS_ENDPOINT]->(:ApiEndpoint)`

| 속성명      | 타입    | 설명                                    |
|-------------|---------|-----------------------------------------|
| `confidence`| float   | 매칭 신뢰도 (대부분 1.0)                |
| `matchType` | string  | `"exact"`, `"normalized"`, `"heuristic"`|
| `rawPath`   | string  | 코드에 있던 원래 path 문자열            |
| `rawMethod` | string  | 코드에 있던(또는 추론된) HTTP 메서드    |

---

#### 3.2.9 축약 간선 (조회 최적화용)

1. **컴포넌트–엔드포인트 사용 여부**

   - 타입: `:COMP_USES_ENDPOINT`
   - 패턴: `(:Component)-[:COMP_USES_ENDPOINT]->(:ApiEndpoint)`

   | 속성명       | 타입          | 설명                                         |
   |--------------|---------------|----------------------------------------------|
   | `viaMethods` | list<string>  | 이 엔드를 호출하는 메서드 ID 목록           |
   | `viaCallSites` | list<string>| 해당 CallSite ID 목록                        |
   | `confidence` | float         | 보통 1.0                                    |

2. **메서드–엔드포인트**

   - 타입: `:METHOD_CALLS_ENDPOINT`
   - 패턴: `(:Method)-[:METHOD_CALLS_ENDPOINT]->(:ApiEndpoint)`

---

#### 3.2.10 요구사항–소스코드 매핑 (합성 결과)

- 타입: `:REQ_IMPLEMENTED_IN_COMPONENT`
- 패턴: `(:Requirement)-[:REQ_IMPLEMENTED_IN_COMPONENT]->(:Component)`

| 속성명         | 타입          | 설명                                                            |
|----------------|---------------|-----------------------------------------------------------------|
| `viaEndpoints` | list<string>  | 이 매핑이 사용한 API 엔드포인트 ID들                           |
| `viaMethods`   | list<string>  | (옵션) 관련 메서드 ID들                                        |
| `confidence`   | float         | 요구사항–API, API–컴포넌트 매핑을 결합한 신뢰도                |
| `implementationRole` | string | `"entry_point_page"`, `"service"`, `"shared_component"` 등      |

(필요 시 `:REQ_IMPLEMENTED_IN_METHOD`도 동일 패턴으로 정의 가능)

---

## 4. 매핑 전략 상세

### 4.1 요구사항–API 매핑 (자연어 + 구조 기반)

1. **텍스트 빌드**

   - Requirement `fullText`:
     - `title + description + 모든 AC + "Tags: ..." + 기타 메타`
   - ApiEndpoint `fullText`:
     - `"[METHOD PATH] summary + description + tags + requestFields + responseFields"`

2. **다국어 임베딩 & 유사도 계산**

   - multilingual sentence embedding 모델 사용
   - Requirement/ApiEndpoint 각각 임베딩 → cosine similarity
   - `textSim` 점수 (0~1)

3. **구조/도메인 보정**

   - `domainScore`:
     - Requirement.tags ↔ ApiEndpoint.resource/tags 매칭 시 가산
   - `operationScore`:
     - Requirement 텍스트에서 동사/행위 추론 (view/add/update/delete/login 등)
     - ApiEndpoint.method 기반 operationType과 일치 여부로 가산

4. **최종 스코어**

   ```text
   finalScore = 0.6 * textSim
              + 0.2 * domainScore
              + 0.2 * operationScore
   ```

5. **간선 생성**

   - 요구사항별로 상위 k개 엔드포인트 후보 선택 (예: k=3)
   - `finalScore >= threshold` (예: 0.6) 인 경우에만
     - `REQ_SATISFIED_BY_ENDPOINT` 관계 생성
   - 속성으로 `confidence=finalScore`, `evidenceType`, `evidenceText` 저장

---

### 4.2 API–Source 매핑 (코드 기반)

1. **AST 분석 확장**

   - 서비스/페이지 코드에서 HTTP 호출 패턴 탐지:
     - `axios.get('/products')`, `fetch('/api/cart')`, `client.post('/auth/login', ...)` 등
   - 각 호출을 `ApiCallSite` JSON으로 추출:
     - filePath, line, rawExpression, method, path, library 등

2. **그래프 적재**

   - `ApiCallSite` → `:ApiCallSite` 노드 생성
   - 각 callsite를 포함하는 메서드/컴포넌트와 연결:
     - `(:Method)-[:METHOD_HAS_CALLSITE]->(:ApiCallSite)`
     - (옵션) componentId 속성으로 컴포넌트 링크

3. **엔드포인트 매핑**

   - `method + path`를 정규화하여 `ApiEndpoint.id`와 매칭
   - 매칭 성공 시:
     - `(:ApiCallSite)-[:CALLSITE_CALLS_ENDPOINT {confidence:1.0, matchType:"exact"}]->(:ApiEndpoint)`

4. **축약 간선 생성**

   - `Component`가 어떤 엔드포인트를 사용하는지:
     ```cypher
     MATCH (c:Component)-[:COMP_HAS_METHOD]->(m:Method)
           -[:METHOD_HAS_CALLSITE]->(cs:ApiCallSite)
           -[:CALLSITE_CALLS_ENDPOINT]->(e:ApiEndpoint)
     MERGE (c)-[rel:COMP_USES_ENDPOINT]->(e)
     ON CREATE SET rel.viaMethods  = [m.id],
                   rel.viaCallSites = [cs.id],
                   rel.confidence = 1.0
     ON MATCH SET  rel.viaMethods  = apoc.coll.toSet(rel.viaMethods + m.id),
                   rel.viaCallSites = apoc.coll.toSet(rel.viaCallSites + cs.id);
     ```

---

### 4.3 요구사항–소스코드 매핑 (합성)

1. **패턴**

   - `Requirement --REQ_SATISFIED_BY_ENDPOINT--> ApiEndpoint`  
   - `Component --COMP_USES_ENDPOINT--> ApiEndpoint`  

2. **합성 후 간선 생성**

   ```cypher
   MATCH (r:Requirement)-[re:REQ_SATISFIED_BY_ENDPOINT]->(e:ApiEndpoint)
         <-[ce:COMP_USES_ENDPOINT]-(c:Component)
   WITH r, e, c, re, ce
   MERGE (r)-[rc:REQ_IMPLEMENTED_IN_COMPONENT]->(c)
   ON CREATE SET rc.viaEndpoints = [e.id],
                 rc.confidence   = re.confidence,
                 rc.implementationRole = CASE
                   WHEN c.isPage THEN "entry_point_page"
                   WHEN c.isService THEN "service"
                   ELSE "component"
                 END
   ON MATCH SET  rc.viaEndpoints = apoc.coll.toSet(rc.viaEndpoints + e.id),
                 rc.confidence   = GREATEST(rc.confidence, re.confidence);
   ```

3. **결과**

- 요구사항 하나가 여러 엔드포인트/컴포넌트와 연결될 수 있고,
- 컴포넌트 하나가 여러 요구사항과 연결될 수 있는 **many-to-many traceability**가 형성된다.

---

## 5. 구현 계획

### 5.1 기술 스택

- Graph DB: Neo4j (Aura/서버형 중 택1)
- ETL/분석 스크립트: Python
  - `neo4j` 공식 드라이버
  - `sentence-transformers` (multilingual 모델)
  - AST 분석기 (TypeScript/JavaScript → JSON)

---

### 5.2 파이프라인 단계별

#### P0 – 그래프 뼈대 적재

- `requirement.json` → `:Requirement` + `:REQ_PARENT_OF`
- `api.json` → `:ApiEndpoint`, `:ApiField` + 엔드포인트–필드 관계
- `source_code.json` → `:Component`, `:Method`, `:COMP_HAS_METHOD`, `:COMP_IMPORTS_COMPONENT`, `:COMP_CALLS_COMPONENT`

검증:
- 각 레이어가 독립적으로 잘 적재되는지 확인
- 간단한 구조 쿼리로 트리/컴포넌트 그래프 시각화

#### P1 – 요구사항–API NLP 매핑

- requirement/api 텍스트 정규화 및 임베딩
- cosine similarity + domain/operation 보정으로 점수 산출
- `REQ_SATISFIED_BY_ENDPOINT` 관계 생성
- 샘플 요구사항에 대한 결과를 수동 검증 → threshold/weight 튜닝

#### P2 – 코드 기반 API–Source 매핑

- AST 분석기 확장 → `ApiCallSite` JSON 추가 생성
- `ApiCallSite` 노드 및 `METHOD_HAS_CALLSITE`, `CALLSITE_CALLS_ENDPOINT` 관계 적재
- `COMP_USES_ENDPOINT`, `METHOD_CALLS_ENDPOINT` 축약간선 생성

#### P3 – 요구사항–소스코드 합성

- 위 Cypher 패턴을 이용해 `REQ_IMPLEMENTED_IN_COMPONENT` (및 필요 시 `REQ_IMPLEMENTED_IN_METHOD`) 생성
- 샘플 요구사항에 대해:
  - “이 요구사항 구현하는 페이지/서비스/메서드 목록” 쿼리 실행
  - 결과를 UI나 콘솔로 확인

#### P4 – 품질 개선 & 피드백 루프

- 매핑 결과를 UI에서 노출:
  - 요구사항 클릭 → 관련 엔드포인트/컴포넌트 표시
  - 사람이 “매핑 맞음/틀림” 체킹 가능하게
- `REQ_SATISFIED_BY_ENDPOINT` 및 `REQ_IMPLEMENTED_IN_COMPONENT` 관계에 `verified: true/false` 속성 추가
- 이 피드백 데이터를 기반으로:
  - 자연어 매핑 모델/룰의 weight 개선
  - 향후 semi-supervised 방식으로 매핑 품질 향상

---

## 6. 활용 시나리오 예시

### 6.1 요구사항 기반 테스트 영향도 분석

- 특정 요구사항 ID로부터:

  ```cypher
  MATCH (r:Requirement {id: "req:R1.1.1.4"})
        -[:REQ_IMPLEMENTED_IN_COMPONENT]->(c:Component)
        -[:COMP_USES_ENDPOINT]->(e:ApiEndpoint)
  RETURN r, c, e;
  ```

- 이 요구사항 관련 페이지/서비스/엔드포인트를 한 번에 조회
- 이 엔드포인트/페이지에 변경이 발생했을 때,
  - 어떤 요구사항과 테스트 케이스가 영향을 받는지 역으로 추적 가능

### 6.2 엔드포인트 변경 시 영향도 분석

```cypher
MATCH (e:ApiEndpoint {id: "POST /auth/login"})
OPTIONAL MATCH (r:Requirement)-[:REQ_SATISFIED_BY_ENDPOINT]->(e)
OPTIONAL MATCH (c:Component)-[:COMP_USES_ENDPOINT]->(e)
RETURN e, collect(DISTINCT r.id) AS requirements, collect(DISTINCT c.id) AS components;
```

- `/auth/login` 변경 → 영향을 받는 요구사항/컴포넌트 한 번에 파악

### 6.3 테스트 시나리오/스크립트 생성 기반

- 요구사항 → 엔드포인트 → 컴포넌트/메서드 경로를 따라가면:
  - 어느 페이지에서 어떤 동작을 통해 어떤 API를 호출하는지 추론 가능
- 여기에 DOM 스냅샷/DB 스키마까지 붙이면:
  - UI locator, API 오라클, DB 검증 조건을 모두 그래프에서 끌어와  
    **요구사항 단위의 E2E 테스트 케이스/Playwright 스크립트 자동 생성**이 가능해진다.

---

## 7. 결론

본 보고서는 `requirement.json`, `api.json`, `source_code.json`을 통합하여

- 요구사항–API–소스코드를 하나의 지식그래프로 표현하기 위한
  - 노드/관계/속성 수준의 **그래프 DB 스키마**
  - 자연어 + 코드 분석 기반 **매핑 전략**
  - 단계별 **구현 계획(ETL/NLP/AST/합성)**

을 제시하였다.

이 스키마를 구현하면,

- 요구사항 중심의 테스트 설계/생성,
- 코드/API 변경에 따른 영향도 분석,
- 추후 자가치유(Self-healing) 테스트 시나리오의 근거 데이터

를 모두 그래프 기반으로 다룰 수 있게 되며,  
AI 기반 UI 테스트 자동화 서비스의 **핵심 인프라(Traceability Graph)** 역할을 수행하게 된다.
