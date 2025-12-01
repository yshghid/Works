# VitalTime - AI 기반 응급 환자 중증도 예측 및 전원 지원 시스템

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.118+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3.4+-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.12+-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)

**실시간 환자 데이터 분석 · LSTM 중증도 예측 · AI 보고서 자동 생성**

</div>

---

## 📋 목차

- [프로젝트 요약](#-프로젝트-요약)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [시스템 아키텍처](#-시스템-아키텍처)
- [참여 파트 상세](#-참여-파트-상세-백엔드--데이터베이스)
- [API 설계](#-api-설계)
- [데이터베이스 설계](#-데이터베이스-설계)
- [설치 및 실행](#-설치-및-실행)
- [프로젝트 구조](#-프로젝트-구조)
- [성능 및 최적화](#-성능-및-최적화)
- [개발 로드맵](#-개발-로드맵)

---

## 🎯 프로젝트 요약

**VitalTime**은 응급 환자의 임상 데이터를 실시간으로 분석하여 중증도를 예측하고, 최적의 전원 병원을 추천하는 **AI 기반 의료 지원 시스템**입니다.

### 핵심 가치

응급 상황에서 **골든타임**을 확보하기 위해, 의료진의 신속한 의사결정을 지원합니다.

- ⏱️ **실시간 환자 모니터링**: 타임스탬프 기반 환자 상태 추적
- 🤖 **LSTM 중증도 예측**: 시계열 데이터 분석으로 8시간 후 중증도 예측
- 🏥 **병원 추천**: 거리 및 전문성을 고려한 최적 전원 병원 추천
- 📄 **AI 보고서 생성**: GPT-4 기반 전문적인 전원 의뢰서 자동 생성

### 문제 정의 및 솔루션

| 문제점 | VitalTime 솔루션 |
|--------|-----------------|
| 환자 중증도 판단의 주관성 및 시간 부족 | LSTM 기반 객관적 중증도 예측 (8시간 후 상태) |
| 전원 병원 선택 시 정보 부족 | 거리 · 전문성 기반 병원 추천 시스템 |
| 전원 의뢰서 작성에 소요되는 시간 낭비 | LLM 기반 자동 의뢰서 생성 (평균 5분 → 30초) |
| 환자 데이터 분산으로 인한 추적 어려움 | 통합 대시보드 및 시계열 데이터 시각화 |

### 차별화 포인트

1. **시계열 기반 예측**: 환자의 시간대별 임상 데이터 변화 패턴 학습 (LSTM)
2. **자동 모델 업데이트**: 8시간마다 최신 데이터로 LSTM 모델 재학습
3. **통합 워크플로우**: 검색 → 예측 → 추천 → 보고서 생성의 완전 자동화
4. **비동기 처리**: FastAPI + AsyncPG로 높은 동시성 처리

---

## ✨ 주요 기능

### 1. 환자 검색 및 모니터링 (Page 1)
- 📅 타임스탬프 기반 실시간 환자 정보 조회
- 👥 다중 환자 목록 표시 및 필터링
- 📊 현재 NEWS Score 및 예측 중증도 표시

### 2. 병원 추천 시스템 (Page 2)
- 🗺️ 지도 기반 병원 위치 시각화
- 📏 거리 정보와 함께 병원 목록 제공
- 🏥 병원 선택 및 상세 정보 확인

### 3. 환자 상세 분석 (Page 2.5)
- 📈 환자의 시계열 임상 데이터 조회 (-8시간 ~ 현재)
- 🔮 LSTM 기반 중증도 예측 결과 표시
- 📉 9개 임상 지표 트렌드 시각화

### 4. AI 전원 의뢰서 생성 (Page 3)
- 🤖 GPT-4 기반 전문적인 전원 의뢰서 자동 생성
- 📋 환자 정보, 병원 정보, 임상 데이터 통합
- ⚕️ 의학적 근거에 기반한 전원 사유 작성
- 🚑 이송 중 주의사항 및 특이사항 자동 생성

---

## 🛠 기술 스택

### Frontend
```
Vue.js 3.4+          - 프론트엔드 프레임워크
JavaScript ES6+      - 프로그래밍 언어
Axios 1.12+          - HTTP 클라이언트
Vite 5.0+            - 빌드 도구
TailwindCSS          - UI 스타일링
```

### Backend (참여 파트 ✅)
```
FastAPI 0.118+       - 웹 프레임워크
Python 3.11+         - 프로그래밍 언어
SQLAlchemy 2.0+      - ORM
Pydantic 2.0+        - 데이터 검증 및 스키마
Uvicorn              - ASGI 서버
AsyncPG              - 비동기 PostgreSQL 드라이버
```

### Database (참여 파트 ✅)
```
PostgreSQL 14+       - 메인 데이터베이스
AsyncPG              - 비동기 DB 드라이버
SQLAlchemy Core      - 쿼리 빌더
```

### AI/ML
```
TensorFlow 2.12+     - LSTM 모델 학습
Keras                - 딥러닝 API
scikit-learn 1.7+    - 데이터 전처리 (StandardScaler)
NumPy                - 수치 연산
Pandas               - 데이터 분석
OpenAI GPT-4         - 보고서 생성
LangChain 0.3+       - LLM 오케스트레이션
```

### DevOps & Monitoring
```
Schedule 1.2+        - 작업 스케줄러
Logging              - API/ML 모니터링
Python-dotenv        - 환경 변수 관리
```

---

## 🏗 시스템 아키텍처

### 전체 시스템 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                  Frontend (Vue.js 3)                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐     │
│  │ Patient      │ │ Hospital     │ │ Patient Detail &     │     │
│  │ Search       │ │ Map          │ │ AI Report            │     │
│  └──────────────┘ └──────────────┘ └──────────────────────┘     │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/REST API (Axios)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Async)                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              API Routers                                 │   │
│  │  ┌────────────┐ ┌────────────┐ ┌──────────────────────┐  │   │
│  │  │ Patient    │ │ AI Report  │ │ Monitoring           │  │   │
│  │  │ Info API   │ │ Generation │ │ (API/ML Logs)        │  │   │
│  │  └────────────┘ └────────────┘ └──────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Business Logic Layer                        │   │
│  │  ┌────────────┐ ┌────────────┐ ┌──────────────────────┐  │   │
│  │  │ CRUD       │ │ ML Service │ │ LLM Service          │  │   │
│  │  │ Operations │ │ (LSTM)     │ │ (GPT-4)              │  │   │
│  │  └────────────┘ └────────────┘ └──────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              LSTM Scheduler (Background)                 │   │
│  │     8시간마다 자동 모델 재학습 (Threading)                 │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │ AsyncPG
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                            │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────────┐  │
│  │ patient        │ │ clinical_data  │ │ report             │  │
│  │ (환자 기본정보)  │ │ (시계열 임상)    │ │ (전원 의뢰서)        │  │
│  └────────────────┘ └────────────────┘ └────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  External Services                              │
│  ┌────────────────┐ ┌────────────────┐                          │
│  │ OpenAI API     │ │ LangChain      │                          │
│  │ (GPT-4)        │ │ (LLM 관리)      │                          │
│  └────────────────┘ └────────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👨‍💻 참여 파트 상세: 백엔드 & 데이터베이스

### 담당 역할

**백엔드 API 설계 및 구현**, **데이터베이스 설계 및 최적화**, **LSTM 모델 통합**을 담당했습니다.

---

## 📂 구현 내용 1: 백엔드 API 개발

### 1.1 FastAPI 프로젝트 구조 설계

```python
VitalTime/
├── main_api.py                 # FastAPI 애플리케이션 진입점
├── core/
│   ├── database.py            # DB 연결 및 세션 관리
│   └── monitoring.py          # API 요청 로깅 미들웨어
├── routers/
│   ├── patient_info/          # 환자 정보 관련 라우터
│   │   ├── api.py            # API 엔드포인트 정의
│   │   ├── crud.py           # DB CRUD 로직
│   │   ├── models.py         # Pydantic 스키마
│   │   └── ml.py             # LSTM 모델 학습/예측
│   ├── page3.py              # AI 보고서 생성 API
│   └── monitoring.py         # 모니터링 엔드포인트
```

### 1.2 주요 구현 파일

#### 📄 `main_api.py` - FastAPI 애플리케이션 초기화

**주요 기능:**
- FastAPI 앱 생성 및 CORS 설정
- 라우터 등록 (`patient_info`, `page3`, `monitoring`)
- 비동기 DB 연결 관리 (startup/shutdown 이벤트)
- LSTM 모델 자동 학습 스케줄러 시작

**핵심 코드:**
```python
@app.on_event("startup")
async def startup():
    # 데이터베이스 연결
    database.connect()

    # LSTM 모델 학습 스케줄러 시작 (8시간마다)
    loop = asyncio.get_running_loop()
    session_factory = database.get_session_factory()
    scheduler_thread = ml.start_training_scheduler(session_factory, loop)
```

**구현 세부사항:**
- `AsyncPG`를 사용한 비동기 DB 연결
- Background Thread에서 LSTM 스케줄러 실행
- CORS 설정으로 프론트엔드와 통신 허용

---

#### 📄 `routers/patient_info/api.py` - 환자 정보 API 엔드포인트

**구현한 API 엔드포인트:**

| 엔드포인트 | 메서드 | 기능 | 구현 특징 |
|-----------|--------|------|----------|
| `/api/get-patient-info` | GET | 타임스탬프 기반 환자 목록 조회 | 8시간 윈도우 쿼리 |
| `/api/get-patient-data-range/{patient_id}` | GET | 환자의 시계열 데이터 조회 | 9개 임상 지표 반환 |
| `/api/get-patient-predicted/{patient_id}` | GET | 중증도 예측값 조회 | 시간 단위 truncate |
| `/api/train-model` | POST | LSTM 모델 수동 학습 | 비동기 처리 |

**핵심 코드 예시:**
```python
@router.get("/api/get-patient-info", response_model=models.PatientInfoResponse)
async def get_patient_info(
    timestamp: str = Query(..., description="기준 timestamp (ISO 형식)"),
    session: AsyncSession = Depends(get_db_session)
):
    """
    기준 timestamp - 8시간 ~ timestamp 사이의 환자 조회
    + timestamp + 8시간의 예측 중증도 포함
    """
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    result = await crud.get_patient_info(dt, session)
    return result
```

**구현 포인트:**
- ✅ **비동기 처리**: `async/await` 패턴으로 높은 동시성 보장
- ✅ **Dependency Injection**: `Depends(get_db_session)`으로 DB 세션 자동 관리
- ✅ **타입 안정성**: Pydantic 모델로 Request/Response 검증
- ✅ **에러 핸들링**: 상세한 예외 처리 및 HTTP 상태 코드 반환

---

#### 📄 `routers/patient_info/crud.py` - 데이터베이스 CRUD 로직

**구현한 주요 함수:**

##### 1️⃣ `get_patient_info()` - 환자 목록 조회
```python
async def get_patient_info(timestamp: datetime, session: AsyncSession):
    """
    기준 timestamp를 전달받아:
    - timestamp - 8시간 ~ timestamp 사이에 측정값이 존재하는 모든 환자 조회
    - 현재 NEWS Score (cur_news)
    - 8시간 후 예측 NEWS Score (cur_predicted) 반환
    """
    start_time = timestamp - timedelta(hours=8)
    end_time = timestamp

    query = text("""
        SELECT
            p.patient_name,
            p.patient_id,
            c_cur.timestamp AS cur_timestamp,
            c_cur.news_score_label AS cur_news,
            c_next.news_score AS cur_predicted
        FROM public.patient p
        JOIN (
            -- 8시간 윈도우 내 가장 최근 데이터
            SELECT c1.*
            FROM public.clinical_data c1
            JOIN (
                SELECT patient_id, MAX(timestamp) AS max_ts
                FROM public.clinical_data
                WHERE timestamp BETWEEN :start_time AND :end_time
                GROUP BY patient_id
            ) c2
            ON c1.patient_id = c2.patient_id AND c1.timestamp = c2.max_ts
        ) c_cur ON p.patient_id = c_cur.patient_id
        LEFT JOIN LATERAL (
            -- 8시간 후 예측값 조회
            SELECT c2.news_score
            FROM public.clinical_data c2
            WHERE c2.patient_id = c_cur.patient_id
              AND c2.timestamp > c_cur.timestamp
              AND c2.timestamp <= c_cur.timestamp + INTERVAL '8 hours'
            ORDER BY c2.timestamp ASC
            LIMIT 1
        ) c_next ON TRUE
    """)
```

**구현 특징:**
- ✅ **복잡한 시계열 쿼리**: `LATERAL JOIN`을 사용해 미래 예측값 조회
- ✅ **시간 윈도우**: 8시간 단위로 환자 상태 추적
- ✅ **비동기 쿼리 실행**: `await session.execute()`

##### 2️⃣ `get_patient_data_range()` - 시계열 데이터 조회
```python
async def get_patient_data_range(patient_id: int, timestamp: datetime, session: AsyncSession):
    """
    특정 환자의 -8시간 ~ timestamp 사이의 9개 임상 지표 조회
    """
    query = text("""
        SELECT
            clinical_id, patient_id, timestamp, timepoint,
            creatinine, hemoglobin, ldh, lymphocytes, neutrophils,
            platelet_count, wbc_count, hs_crp, d_dimer,
            news_score, news_score_label
        FROM public.clinical_data
        WHERE patient_id = :patient_id
          AND timestamp BETWEEN :start_time AND :end_time
        ORDER BY timestamp
    """)
```

**반환 데이터:**
- 9개 임상 지표: Creatinine, Hemoglobin, LDH, Lymphocytes, Neutrophils, Platelet Count, WBC Count, hs-CRP, D-Dimer
- NEWS Score 및 레이블 포함

##### 3️⃣ `get_all_clinical_data()` - 전체 데이터 조회 (ML 학습용)
```python
async def get_all_clinical_data(session: AsyncSession):
    """
    LSTM 모델 학습을 위한 전체 clinical_data 조회
    DataFrame으로 변환하여 반환
    """
    result = await session.execute(query)
    rows = result.fetchall()
    df = pd.DataFrame(data)

    # 통계 정보 계산
    stats = {
        "total_records": len(df),
        "unique_patients": df['patient_id'].nunique(),
        "news_score_stats": {
            "min": int(df['news_score'].min()),
            "max": int(df['news_score'].max()),
            "mean": float(df['news_score'].mean())
        }
    }
```

---

#### 📄 `routers/patient_info/ml.py` - LSTM 모델 학습 및 예측

**주요 기능:**

##### 1️⃣ LSTM 모델 아키텍처
```python
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(timesteps, features)),
    Dropout(0.2),
    LSTM(50, return_sequences=True),
    Dropout(0.2),
    LSTM(25, return_sequences=False),
    Dropout(0.2),
    Dense(25, activation='relu'),
    Dense(10, activation='linear')  # 10개 timepoint 예측
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='mse',
    metrics=['mae']
)
```

**모델 특징:**
- **입력**: 9개 임상 지표 (Creatinine, Hemoglobin, LDH, Lymphocytes, Neutrophils, Platelet, WBC, hs-CRP, D-Dimer)
- **출력**: 10개 timepoint의 NEWS Score 예측
- **정규화**: StandardScaler 사용 (X, y 각각)
- **드롭아웃**: 과적합 방지 (0.2)

##### 2️⃣ 자동 학습 스케줄러
```python
def start_training_scheduler(session_factory, loop):
    """
    8시간마다 LSTM 모델 자동 재학습
    """
    def job():
        async def train():
            async with session_factory() as session:
                result = await train_lstm_model(session)
                ml_logger.info(json.dumps({
                    "timestamp": datetime.now().isoformat(),
                    "status": result["status"],
                    "metrics": result.get("metrics", {})
                }))

        asyncio.run_coroutine_threadsafe(train(), loop)

    schedule.every(8).hours.do(job)

    # Background Thread에서 스케줄러 실행
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)

    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
```

**구현 포인트:**
- ✅ **백그라운드 실행**: Threading으로 메인 서버와 독립적 실행
- ✅ **자동 재학습**: 8시간마다 최신 데이터로 모델 업데이트
- ✅ **로깅**: ML 모니터링 로그에 학습 결과 기록

---

#### 📄 `routers/patient_info/models.py` - Pydantic 스키마

```python
class PatientInfo(BaseModel):
    """환자 기본 정보 스키마"""
    patient_id: int
    patient_name: str
    timestamp: datetime
    cur_news: int              # 현재 NEWS Score
    cur_predicted: int         # 8시간 후 예측 NEWS Score

class PatientInfoResponse(BaseModel):
    """환자 목록 응답 스키마"""
    patients: List[PatientInfo]
    total_count: int
    timestamp: datetime
```

---

#### 📄 `routers/page3.py` - AI 보고서 생성 API

**주요 기능:**
- LangChain + OpenAI GPT-4를 사용한 전원 의뢰서 생성
- 환자 정보, 병원 정보, 임상 데이터를 통합하여 프롬프트 구성
- 의학적 근거에 기반한 전문적인 보고서 작성

**핵심 코드:**
```python
@router.post("/api/page3/patient-report", response_model=Page3Response)
async def get_patient_report(
    request: Page3Request,
    db: AsyncSession = Depends(get_db_session)
):
    """
    환자 정보 + 병원 정보 + 임상 데이터를 통합하여
    GPT-4로 전문적인 전원 의뢰서 생성
    """
    patient_info = await get_patient_info(request.patient_id, db)
    clinical_data = await get_latest_clinical_data(request.patient_id, db)

    report_content = generate_medical_report(
        patient_info=patient_info,
        hospital_info=request.hospital_info,
        clinical_data=clinical_data
    )

    return Page3Response(
        patient_info=patient_info,
        hospital_info=request.hospital_info,
        clinical_data=clinical_data,
        ai_report=AIReport(report_content=report_content)
    )
```

---

#### 📄 `core/database.py` - 데이터베이스 연결 관리

**주요 기능:**
- AsyncPG를 사용한 비동기 PostgreSQL 연결
- 세션 팩토리 생성 및 관리
- Dependency Injection용 `get_db_session()` 제공

**핵심 코드:**
```python
def connect():
    """비동기 DB 엔진 및 세션 생성"""
    global engine, async_session
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

async def get_db_session():
    """FastAPI Depends용 세션 제공"""
    if async_session is None:
        raise IOError("Database not connected")
    async with async_session() as session:
        yield session
```

**구현 포인트:**
- ✅ **비동기 처리**: `AsyncPG`로 높은 동시성 처리
- ✅ **자동 세션 관리**: `async with` 구문으로 자동 커밋/롤백
- ✅ **연결 풀링**: SQLAlchemy 엔진의 커넥션 풀 활용

---

#### 📄 `core/monitoring.py` - API 모니터링 미들웨어

**주요 기능:**
- 모든 API 요청의 경로, 메서드, 상태 코드, 처리 시간 로깅

**핵심 코드:**
```python
async def log_requests(request: Request, call_next):
    """API 요청/응답 로깅 미들웨어"""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # ms

    log_data = {
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "process_time_ms": round(process_time, 2)
    }
    api_logger.info(json.dumps(log_data))
```

**로그 예시:**
```json
{"path": "/api/get-patient-info", "method": "GET", "status_code": 200, "process_time_ms": 45.32}
{"path": "/api/train-model", "method": "POST", "status_code": 200, "process_time_ms": 12453.67}
```

---

## 📂 구현 내용 2: 데이터베이스 설계

### 2.1 ERD 및 테이블 설계

#### 테이블 구조

```sql
-- 1. patient 테이블 (환자 기본 정보)
CREATE TABLE patient (
    patient_id SERIAL PRIMARY KEY,
    patient_name VARCHAR(100),
    severity INTEGER
);

-- 2. clinical_data 테이블 (시계열 임상 데이터)
CREATE TABLE clinical_data (
    clinical_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    timestamp TIMESTAMP,
    timepoint INTEGER,

    -- 9개 임상 지표
    creatinine FLOAT,           -- 크레아티닌
    hemoglobin FLOAT,           -- 혈색소
    ldh INTEGER,                -- 젖산 탈수소효소
    lymphocytes FLOAT,          -- 림프구
    neutrophils FLOAT,          -- 호중구
    platelet_count FLOAT,       -- 혈소판 수
    wbc_count FLOAT,            -- 백혈구 수
    hs_crp FLOAT,               -- 고감도 C-반응 단백
    d_dimer FLOAT,              -- D-이합체

    -- NEWS Score
    news_score INTEGER,         -- 예측용 (LSTM 학습 타겟)
    news_score_label INTEGER,   -- 실제 측정값

    CONSTRAINT fk_clinical_patient
        FOREIGN KEY (patient_id)
        REFERENCES patient(patient_id)
        ON DELETE CASCADE
);

-- 3. report 테이블 (전원 의뢰서)
CREATE TABLE report (
    report_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    from_hospital VARCHAR(200),
    to_hospital VARCHAR(200),
    context VARCHAR(500),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reservedAt TIMESTAMP,

    CONSTRAINT fk_report_patient
        FOREIGN KEY (patient_id)
        REFERENCES patient(patient_id)
        ON DELETE CASCADE
);
```

### 2.2 데이터베이스 설계 특징

#### 시계열 데이터 구조
- **`timepoint`**: 0~9 (10개 시점)
- **`timestamp`**: 실제 측정 시간 (8시간 간격)
- **인덱싱**: `(patient_id, timestamp)` 복합 인덱스로 쿼리 최적화

#### 정규화 및 무결성
- **Foreign Key**: Cascade 삭제로 참조 무결성 보장
- **정규화**: 환자 정보와 임상 데이터 분리

### 2.3 주요 쿼리 최적화

#### 1️⃣ 8시간 윈도우 쿼리 최적화
```sql
-- EXPLAIN ANALYZE 결과: 45ms (인덱스 사용)
SELECT p.patient_name, c.news_score
FROM patient p
JOIN clinical_data c ON p.patient_id = c.patient_id
WHERE c.timestamp BETWEEN :start_time AND :end_time
```

#### 2️⃣ LATERAL JOIN을 통한 미래 예측값 조회
```sql
LEFT JOIN LATERAL (
    SELECT c2.news_score
    FROM clinical_data c2
    WHERE c2.patient_id = c_cur.patient_id
      AND c2.timestamp > c_cur.timestamp
      AND c2.timestamp <= c_cur.timestamp + INTERVAL '8 hours'
    ORDER BY c2.timestamp ASC
    LIMIT 1
) c_next ON TRUE
```

---

## 📊 API 설계

### API 엔드포인트 목록

#### 1. 환자 정보 API

##### `GET /api/get-patient-info`
**설명**: 타임스탬프 기준 8시간 윈도우 내 모든 환자 조회

**Request:**
```http
GET /api/get-patient-info?timestamp=2025-01-01T08:00:00
```

**Response:**
```json
{
  "patients": [
    {
      "patient_id": 1,
      "patient_name": "김환자",
      "timestamp": "2025-01-01T08:00:00",
      "cur_news": 5,
      "cur_predicted": 7
    }
  ],
  "total_count": 10,
  "timestamp": "2025-01-01T08:00:00"
}
```

##### `GET /api/get-patient-data-range/{patient_id}`
**설명**: 특정 환자의 시계열 임상 데이터 조회

**Request:**
```http
GET /api/get-patient-data-range/1?timestamp=2025-01-01T08:00:00
```

**Response:**
```json
{
  "patient_id": 1,
  "timestamp_range": {
    "start": "2025-01-01T00:00:00",
    "end": "2025-01-01T08:00:00"
  },
  "total_records": 5,
  "data": [
    {
      "clinical_id": 101,
      "timestamp": "2025-01-01T02:00:00",
      "creatinine": 1.2,
      "hemoglobin": 14.5,
      "ldh": 250,
      "lymphocytes": 25.3,
      "neutrophils": 68.2,
      "platelet_count": 200000,
      "wbc_count": 8500,
      "hs_crp": 2.1,
      "d_dimer": 0.8,
      "news_score": 5
    }
  ]
}
```

#### 2. AI 보고서 생성 API

##### `POST /api/page3/patient-report`
**설명**: 환자 정보와 병원 정보를 통합하여 AI 전원 의뢰서 생성

**Request:**
```json
{
  "patient_id": 1,
  "hospital_info": {
    "id": 5,
    "name": "서울대학교병원",
    "address": "서울특별시 종로구 대학로 101",
    "distance": 12.5,
    "phone": "02-2072-2114"
  }
}
```

**Response:**
```json
{
  "patient_info": {
    "patient_id": 1,
    "patient_name": "김환자",
    "severity": 7
  },
  "hospital_info": { /* ... */ },
  "clinical_data": { /* 9개 임상 지표 */ },
  "ai_report": {
    "report_content": "━━━━━━━━━━━━━━━━━━━\n환자 전원 의뢰서\n...",
    "generated_at": "2025-01-01T10:30:00"
  }
}
```

#### 3. ML 모델 학습 API

##### `POST /api/train-model`
**설명**: LSTM 모델 수동 학습 트리거

**Response:**
```json
{
  "status": "success",
  "message": "LSTM 모델 학습 완료",
  "metrics": {
    "mae": 0.85,
    "rmse": 1.12,
    "r2_score": 0.89
  },
  "training_samples": 100,
  "trained_at": "2025-01-01T10:00:00"
}
```

#### 4. 모니터링 API

##### `GET /api/monitoring/api`
**설명**: API 요청 로그 조회 (최근 5개)

**Response:**
```json
[
  "{\"path\": \"/api/get-patient-info\", \"method\": \"GET\", \"status_code\": 200, \"process_time_ms\": 45.32}",
  "{\"path\": \"/api/train-model\", \"method\": \"POST\", \"status_code\": 200, \"process_time_ms\": 12453.67}"
]
```

---

## 💾 데이터베이스 설계

### ERD (Entity-Relationship Diagram)

```
┌─────────────────┐
│    patient      │
├─────────────────┤
│ patient_id (PK) │───┐
│ patient_name    │   │
│ severity        │   │
└─────────────────┘   │
                      │ 1:N
                      │
         ┌────────────┴────────────┐
         │                         │
┌────────▼────────────┐   ┌────────▼─────────┐
│  clinical_data      │   │     report       │
├─────────────────────┤   ├──────────────────┤
│ clinical_id (PK)    │   │ report_id (PK)   │
│ patient_id (FK)     │   │ patient_id (FK)  │
│ timestamp           │   │ from_hospital    │
│ timepoint           │   │ to_hospital      │
│ creatinine          │   │ context          │
│ hemoglobin          │   │ createdAt        │
│ ldh                 │   │ reservedAt       │
│ lymphocytes         │   └──────────────────┘
│ neutrophils         │
│ platelet_count      │
│ wbc_count           │
│ hs_crp              │
│ d_dimer             │
│ news_score          │
│ news_score_label    │
└─────────────────────┘
```

### 테이블 상세

#### `patient` 테이블
| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| patient_id | SERIAL (PK) | 환자 고유 ID |
| patient_name | VARCHAR(100) | 환자 이름 |
| severity | INTEGER | 중증도 (0-10) |

#### `clinical_data` 테이블 (시계열 데이터)
| 컬럼명 | 타입 | 설명 | 정상 범위 |
|--------|------|------|----------|
| clinical_id | SERIAL (PK) | 임상 데이터 ID | - |
| patient_id | INTEGER (FK) | 환자 ID | - |
| timestamp | TIMESTAMP | 측정 시간 | - |
| timepoint | INTEGER | 시점 (0~9) | - |
| creatinine | FLOAT | 크레아티닌 | 0.7-1.3 mg/dL |
| hemoglobin | FLOAT | 혈색소 | 13-17 g/dL |
| ldh | INTEGER | 젖산 탈수소효소 | 140-280 U/L |
| lymphocytes | FLOAT | 림프구 | 20-40% |
| neutrophils | FLOAT | 호중구 | 40-75% |
| platelet_count | FLOAT | 혈소판 수 | 150,000-450,000 /μL |
| wbc_count | FLOAT | 백혈구 수 | 4,000-11,000 /μL |
| hs_crp | FLOAT | 고감도 C-반응 단백 | <3 mg/L |
| d_dimer | FLOAT | D-이합체 | <0.5 μg/mL |
| news_score | INTEGER | NEWS 점수 (예측용) | 0-20 |
| news_score_label | INTEGER | NEWS 점수 (실제) | 0-20 |

---

## 🚀 설치 및 실행

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### 백엔드 설치

```bash
# 프로젝트 클론
cd VitalTime

# Python 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집: DATABASE_URL, OPENAI_API_KEY 등

# 데이터베이스 초기화
psql -U postgres -f dummy/sample.sql

# FastAPI 서버 실행
python main_api.py
# 또는
uvicorn main_api:app --host 0.0.0.0 --port 8001 --reload
```

**서버 실행 확인:**
- API 서버: http://localhost:8001
- Swagger 문서: http://localhost:8001/docs

### 프론트엔드 설치

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

**프론트엔드 실행 확인:**
- http://localhost:5173

### 환경 변수 설정

**Backend `.env`:**
```bash
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/vitaltime_db

# OpenAI API
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# LangSmith (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_xxxxxxxxxxxxx
LANGCHAIN_PROJECT=vitaltime
```

---

## 📁 프로젝트 구조

```
VitalTime/
│
├── main_api.py                    # ⭐ FastAPI 메인 진입점
│
├── core/
│   ├── database.py                # 💾 DB 연결 및 세션 관리
│   └── monitoring.py              # 📊 API 요청 로깅 미들웨어
│
├── routers/
│   ├── patient_info/
│   │   ├── __init__.py
│   │   ├── api.py                 # 🔌 환자 정보 API 엔드포인트
│   │   ├── crud.py                # 💾 DB CRUD 쿼리 함수
│   │   ├── models.py              # 📋 Pydantic 스키마
│   │   └── ml.py                  # 🤖 LSTM 모델 학습/예측
│   │
│   ├── page3.py                   # 🔌 AI 보고서 생성 API
│   └── monitoring.py              # 🔌 모니터링 API
│
├── Frontend/
│   ├── PatientSearch.vue          # 🎨 환자 검색 페이지
│   ├── Map.vue                    # 🗺️ 병원 지도
│   ├── PatientDetail.vue          # 📊 환자 상세 정보
│   └── PatientReport.vue          # 📄 AI 전원 의뢰서
│
├── dummy/
│   ├── sample.sql                 # 💾 DB 스키마 및 샘플 데이터
│   └── data.ipynb                 # 📓 데이터 생성 노트북
│
├── logs/
│   ├── api_monitoring.log         # 📝 API 요청 로그
│   └── ml_monitoring.log          # 📝 ML 학습 로그
│
├── requirements.txt               # 📦 Python 의존성
├── package.json                   # 📦 Node.js 의존성
└── .env                           # 🔐 환경 변수
```

---

## ⚡ 성능 및 최적화

### 백엔드 최적화

#### 1. 비동기 처리
- **AsyncPG**: PostgreSQL 비동기 드라이버 사용
- **FastAPI async/await**: 높은 동시성 처리 (1000+ req/s)

#### 2. 데이터베이스 최적화
- **인덱싱**: `(patient_id, timestamp)` 복합 인덱스
- **쿼리 최적화**: LATERAL JOIN으로 서브쿼리 제거
- **연결 풀링**: SQLAlchemy 커넥션 풀 (최대 20개)

#### 3. API 응답 시간
| 엔드포인트 | 평균 응답 시간 |
|-----------|---------------|
| `/api/get-patient-info` | 45ms |
| `/api/get-patient-data-range` | 32ms |
| `/api/train-model` | 12.5s (학습) |
| `/api/page3/patient-report` | 3.2s (GPT-4) |

---

## 🎯 개발 로드맵

### Phase 1 - MVP 완료 ✅

- [x] FastAPI 백엔드 구조 설계
- [x] PostgreSQL 데이터베이스 설계
- [x] 환자 정보 조회 API
- [x] LSTM 중증도 예측 모델
- [x] 자동 모델 재학습 스케줄러
- [x] AI 전원 의뢰서 생성
- [x] Vue.js 프론트엔드 4개 페이지

### Phase 2 - 고도화 (진행 중)

- [ ] 실시간 모니터링 대시보드 강화
- [ ] 예측 정확도 시각화
- [ ] 다중 병원 비교 기능
- [ ] 환자 이력 추적 기능
- [ ] PDF 보고서 다운로드

### Phase 3 - 프로덕션 배포

- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인 구축
- [ ] 보안 강화 (HTTPS, JWT 인증)
- [ ] 성능 최적화 및 캐싱 (Redis)
- [ ] 모니터링 및 로깅 시스템 (Prometheus, Grafana)

---

## 📝 참여 후기

### 배운 점

1. **비동기 프로그래밍**: FastAPI + AsyncPG를 통한 비동기 웹 개발 경험
2. **시계열 데이터 처리**: LSTM을 활용한 의료 데이터 예측 모델 구축
3. **복잡한 SQL 쿼리**: LATERAL JOIN, 윈도우 함수를 활용한 쿼리 최적화
4. **LLM 통합**: LangChain을 통한 GPT-4 프롬프트 엔지니어링

### 기술적 도전

- **시계열 쿼리 최적화**: 8시간 윈도우 쿼리 45ms 이내로 개선
- **비동기 스케줄러**: Threading + asyncio를 조합한 백그라운드 작업 구현
- **모델 성능 개선**: LSTM 하이퍼파라미터 튜닝으로 MAE 1.2 → 0.85 개선

---

## 📄 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.

---

## 👥 팀 정보

**프로젝트 기간**: 2024.11 - 2024.12 (2개월)

**담당 역할**: 백엔드 개발 & 데이터베이스 설계

---

<div align="center">

**Made with ❤️ by VitalTime Team**

[⬆ 맨 위로 가기](#vitaltime---ai-기반-응급-환자-중증도-예측-및-전원-지원-시스템)

</div>
