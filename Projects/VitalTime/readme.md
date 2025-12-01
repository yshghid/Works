# VitalTime 

**AI 기반 응급 환자 중증도 예측 및 병원 추천 시스템**

***

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [시스템 아키텍처](#2-시스템-아키텍처)
3. [기술 스택](#3-기술-스택)
4. [주요 기능](#4-주요-기능)
5. [폴더 구조](#5-폴더-구조)
6. [API 설계](#6-api-설계)
7. [설치 및 실행](#7-설치-및-실행)
8. [환경 변수](#8-환경-변수)
9. [개발 로드맵](#9-개발-로드맵)

***

## 1. 프로젝트 개요

### 1.1 서비스 소개

**VitalTime**은 응급 환자의 임상 데이터를 실시간으로 분석하여 중증도를 예측하고, 최적의 전원 병원을 추천하는 AI 기반 의료 지원 시스템입니다.

**핵심 기능:**

- **환자 검색**: 타임스탬프 기반 실시간 환자 정보 조회
- **중증도 예측**: LSTM 모델을 활용한 환자 중증도 자동 예측
- **병원 추천**: 거리 및 병원 정보를 고려한 최적 전원 병원 추천
- **AI 보고서 생성**: LLM 기반 환자 전원 의뢰서 자동 생성


### 1.2 문제 정의

**응급의료 현황:**

- 응급 환자 전원 결정 시간 부족으로 인한 골든타임 손실
- 환자 중증도 판단의 주관성과 의료진 부담 과중
- 전원 병원 선택 시 정보 부족으로 인한 비효율적 의사결정
- 전원 의뢰서 작성에 소요되는 시간 낭비

**VitalTime 솔루션:**

- 실시간 중증도 예측으로 빠른 의사결정 지원
- LSTM 기반 객관적 중증도 판단 제공
- 거리 및 전문성을 고려한 병원 추천
- AI 기반 전원 의뢰서 자동 생성으로 업무 효율 향상


### 1.3 차별화 포인트

1. **LSTM 기반 시계열 분석**: 환자의 시간대별 임상 데이터 변화 패턴 학습
2. **실시간 데이터 처리**: 타임스탬프 기반 최신 환자 상태 반영
3. **통합 워크플로우**: 검색 → 예측 → 추천 → 보고서 생성의 완전 자동화
4. **자동 모델 업데이트**: 8시간마다 최신 데이터로 LSTM 모델 재학습

***

## 2. 시스템 아키텍처

### 2.1 전체 시스템 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                  사용자 인터페이스 (Vue.js 3)                        │
│                  - 환자 검색 (PatientSearch.vue)                   │
│                  - 병원 지도 및 선택 (Map.vue)                      │
│                  - 환자 상세 정보 (PatientDetail.vue)               │
│                  - AI 전원 의뢰서 (PatientReport.vue)               │
└──────┬──────────────────────────────────────────────────────────┘
       │
       │ HTTP (Axios)
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                              │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐   │
│  │ /api/            │  │ /api/            │  │ /api/        │   │
│  │ get-patient-info │  │ get-patient-     │  │ train-model  │   │
│  │                  │  │ predicted        │  │              │   │
│  │ (환자 정보 조회)   │  │ (중증도 예측)      │  │ (모델 학습)    │   │
│  └──────────────────┘  └──────────────────┘  └──────────────┘   │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ /api/page3/      │  │ LSTM Scheduler   │                     │
│  │ patient-report   │  │ (8시간마다 자동    │                     │
│  │ (AI 보고서 생성)   │  │  모델 재학습)      │                     │
│  └──────────────────┘  └──────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  PostgreSQL / AsyncPG                │
│  - patient (환자 기본 정보)            │
│  - clinical_data (임상 검사 데이터)     │
│  - hospital (병원 정보)                │
│  - lstm_predictions (예측 결과)        │
└──────────────────────────────────────┘
       │
       └───────────────┐
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              AI/ML 컴포넌트                                       │
│  - LSTM 중증도 예측 모델                                          │
│  - OpenAI GPT-4 (전원 의뢰서 생성)                                │
│  - LangChain (프롬프트 관리)                                      │
└─────────────────────────────────────────────────────────────────┘
```


***

## 3. 기술 스택

### 3.1 백엔드

```yaml
프레임워크: FastAPI 0.118+
언어: Python 3.11+

AI/ML:
  - TensorFlow 2.12+ (LSTM 모델)
  - scikit-learn 1.7+ (데이터 전처리)
  - LangChain 0.3+ (LLM 오케스트레이션)
  - LangSmith (모니터링)
  - OpenAI GPT-4 (보고서 생성)

데이터베이스:
  - PostgreSQL (메인 DB)
  - AsyncPG (비동기 DB 드라이버)

ORM: SQLAlchemy 2.0+
스키마: Pydantic 2.0+
작업 스케줄러: schedule 1.2+
```


### 3.2 프론트엔드

```yaml
프레임워크: Vue.js 3.4+
언어: JavaScript
HTTP 클라이언트: Axios 1.12+
빌드도구: Vite 5.0+
```


### 3.3 머신러닝

```yaml
모델 아키텍처: LSTM (Long Short-Term Memory)
입력 특성:
  - D-Dimer (D-이합체)
  - LDH (젖산 탈수소효소)
  - Creatinine (크레아티닌)
  - Hemoglobin (혈색소)
  - Lymphocytes (림프구)
  - Neutrophils (호중구)
  - Platelet Count (혈소판)
  - WBC Count (백혈구)
  - hs-CRP (고감도 C-반응 단백)

학습 방식: 시계열 데이터 기반 지도학습
업데이트 주기: 8시간마다 자동 재학습
```


***

## 4. 주요 기능

### 4.1 환자 검색 (Page 1)

- 타임스탬프 기반 실시간 환자 정보 조회
- 환자 기본 정보 및 중증도 표시
- 다중 환자 목록 표시

### 4.2 병원 추천 (Page 2)

- 지도 기반 병원 위치 시각화
- 거리 정보와 함께 병원 목록 제공
- 병원 선택 및 상세 정보 확인

### 4.3 환자 상세 분석 (Page 2.5)

- 환자의 시계열 임상 데이터 조회
- LSTM 기반 중증도 예측 결과 표시
- 예측 신뢰도 및 위험도 시각화

### 4.4 AI 전원 의뢰서 생성 (Page 3)

- LLM 기반 전문적인 전원 의뢰서 자동 생성
- 환자 정보, 병원 정보, 임상 데이터 통합
- 의학적 근거에 기반한 전원 사유 작성
- 이송 중 주의사항 및 특이사항 자동 생성


***

## 5. 폴더 구조

### 5.1 백엔드

```
VitalTime/
├── main_api.py                        # FastAPI 진입점
│
├── core/
│   ├── database.py                    # DB 연결 관리
│   └── monitoring.py                  # API 모니터링
│
├── routers/
│   ├── patient_info/
│   │   ├── __init__.py
│   │   ├── api.py                     # 환자 정보 API
│   │   ├── crud.py                    # DB CRUD 작업
│   │   ├── ml.py                      # LSTM 모델 학습/예측
│   │   └── models.py                  # Pydantic 모델
│   │
│   ├── page3.py                       # AI 보고서 생성 API
│   └── monitoring.py                  # 모니터링 API
│
├── dummy/
│   ├── data.ipynb                     # 데이터 생성 노트북
│   ├── patient_info_api.py            # 더미 API
│   └── sample.sql                     # 샘플 데이터 SQL
│
├── logs/
│   ├── api_monitoring.log
│   └── ml_monitoring.log
│
├── requirements.txt                   # Python 의존성
├── .env                               # 환경 변수
└── config.js.example                  # 설정 파일 예시
```


### 5.2 프론트엔드

```
Frontend/
├── PatientSearch.vue                  # 환자 검색 페이지 (Page 1)
├── Map.vue                            # 병원 지도 및 선택 (Page 2)
├── PatientDetail.vue                  # 환자 상세 정보 (Page 2.5)
└── PatientReport.vue                  # AI 전원 의뢰서 (Page 3)
```


***

## 6. API 설계

### 6.1 환자 정보 API

#### 환자 정보 조회

```
GET /api/get-patient-info?timestamp={ISO_TIMESTAMP}
```

**Request:**
```
GET /api/get-patient-info?timestamp=2025-01-01T08:00:00
```

**Response:**
```json
{
  "patient_id": 1,
  "patient_name": "김환자",
  "age": 45,
  "gender": "M",
  "severity": 7,
  "timestamp": "2025-01-01T08:00:00"
}
```


#### 환자 시계열 데이터 조회

```
GET /api/get-patient-data-range/{patient_id}?timestamp={ISO_TIMESTAMP}
```

**Response:**
```json
{
  "patient_id": 1,
  "data_points": [
    {
      "timepoint": 0,
      "d_dimer": 1.2,
      "ldh": 350,
      "creatinine": 1.5,
      "timestamp": "2025-01-01T08:00:00"
    },
    {
      "timepoint": 1,
      "d_dimer": 1.5,
      "ldh": 380,
      "creatinine": 1.6,
      "timestamp": "2025-01-01T09:00:00"
    }
  ]
}
```


### 6.2 중증도 예측 API

```
GET /api/get-patient-predicted/{patient_id}?timestamp={ISO_TIMESTAMP}
```

**Response:**
```json
{
  "patient_id": 1,
  "predicted_severity": 8,
  "confidence": 0.92,
  "risk_level": "high",
  "timestamp": "2025-01-01T08:00:00"
}
```


### 6.3 AI 보고서 생성 API

```
POST /api/page3/patient-report
```

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
  "hospital_info": {
    "id": 5,
    "name": "서울대학교병원",
    "address": "서울특별시 종로구 대학로 101",
    "distance": 12.5,
    "phone": "02-2072-2114"
  },
  "clinical_data": {
    "d_dimer": 1.5,
    "ldh": 380,
    "creatinine": 1.6,
    "hemoglobin": 14.2,
    "lymphocytes": 25.5,
    "neutrophils": 68.3,
    "hs_crp": 3.8,
    "timepoint": 5
  },
  "ai_report": {
    "report_content": "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n환자 전원 의뢰서\n...",
    "generated_at": "2025-01-01T10:30:00"
  }
}
```


### 6.4 모델 학습 API

```
POST /api/train-model
```

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
  "training_samples": 1500,
  "trained_at": "2025-01-01T10:00:00"
}
```


***

## 7. 설치 및 실행

### 7.1 Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### 7.2 백엔드 설치

```bash
# 저장소 클론
cd VitalTime

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 DATABASE_URL, OPENAI_API_KEY 등 설정

# 데이터베이스 초기화
psql -U postgres -f dummy/sample.sql

# 서버 실행
python main_api.py
# 또는
uvicorn main_api:app --host 0.0.0.0 --port 8001 --reload
```

서버가 http://localhost:8001 에서 실행됩니다.


### 7.3 프론트엔드 설치

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드가 http://localhost:5173 에서 실행됩니다.


### 7.4 API 문서 확인

서버 실행 후 http://localhost:8001/docs 에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다.


***

## 8. 환경 변수

### Backend `.env`

```bash
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/vitaltime_db

# OpenAI API
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# LangSmith (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_xxxxxxxxxxxxx
LANGCHAIN_PROJECT=vitaltime

# Hugging Face (Optional, for local LLM)
hf_token=hf_xxxxxxxxxxxxxxxxxxxxx
```


***

## 9. 개발 로드맵

### 9.1 Phase 1 - MVP 완료 ✓

- [x] FastAPI 백엔드 구조 설계
- [x] PostgreSQL 데이터베이스 설계
- [x] 환자 정보 조회 API
- [x] LSTM 중증도 예측 모델
- [x] 자동 모델 재학습 스케줄러
- [x] AI 전원 의뢰서 생성
- [x] Vue.js 프론트엔드 4개 페이지


### 9.2 Phase 2 - 고도화 (진행 중)

- [ ] 실시간 모니터링 대시보드 강화
- [ ] 예측 정확도 시각화
- [ ] 다중 병원 비교 기능
- [ ] 환자 이력 추적 기능
- [ ] PDF 보고서 다운로드


### 9.3 Phase 3 - 프로덕션 배포

- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인 구축
- [ ] 보안 강화 (HTTPS, 인증/인가)
- [ ] 성능 최적화 및 캐싱
- [ ] 모니터링 및 로깅 시스템
- [ ] 백업 및 복구 시스템


***

## 10. 주요 기술적 특징

### 10.1 비동기 처리

- SQLAlchemy의 AsyncSession을 활용한 비동기 DB 처리
- FastAPI의 async/await 패턴으로 높은 동시성 처리

### 10.2 자동화된 머신러닝 파이프라인

- 8시간마다 자동으로 최신 데이터로 LSTM 모델 재학습
- Background scheduler를 통한 무중단 학습

### 10.3 확장 가능한 아키텍처

- 모듈화된 라우터 구조로 기능 추가 용이
- Pydantic 모델을 통한 타입 안정성 보장
- 환경 변수 기반 설정으로 배포 환경 대응


***

## 11. 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.


***

**문서 버전:** 1.0.0
**최종 수정일:** 2025-12-01
**담당자:** VitalTime 개발팀
