# Cloud 

Docker 및 Kubernetes를 활용한 클라우드 배포 실습

---
## Contents

- 01-Docker-배포-실습
  - Nginx 기반 정적 웹사이트의 Docker 컨테이너화 및 Kubernetes 배포 실습

---

## 01-Docker-배포-실습

### 프로젝트 구조

```text
01-Docker-배포-실습/
├── Dockerfile              # Nginx 기반 Docker 이미지 정의
├── docker-build.sh         # Docker 이미지 빌드 스크립트
├── docker-push.sh          # Docker 이미지 레지스트리 푸시 스크립트
├── default.conf            # Nginx 설정 파일
├── deploy.yaml             # Kubernetes Deployment 매니페스트
├── service.yaml            # Kubernetes Service 매니페스트
├── deploy/                 # 배포 템플릿 및 설정
│   ├── env.properties      # 환경 변수 설정
│   ├── deploy.t            # Deployment 템플릿
│   └── service.t           # Service 템플릿
└── src/                    # 정적 웹사이트 소스
    ├── index.html          # 개인 프로필 페이지
    └── media/              # 이미지 리소스
```

### 주요 구성 요소

#### 1. Dockerfile

- **베이스 이미지**: nginx:alpine
- **기능**:
  - Nginx 설정 파일 복사 (`default.conf`)
  - 정적 리소스 복사 (`src/` → `/usr/share/nginx/html/`)
  - 포트 80 노출
  - Nginx 서버 실행

#### 2. Nginx 설정 (default.conf)

```nginx
location /sk019/ {
    alias /usr/share/nginx/html/;
    index index.html;
    try_files $uri $uri/ /index.html;
}
```

- `/sk019/` 경로로 웹사이트 서빙
- 정적 파일 제공 및 SPA 라우팅 지원

#### 3. Docker 빌드 스크립트 (docker-build.sh)

```bash
NAME=sk019
IMAGE_NAME="posts-get"
VERSION="1.0"
CPU_PLATFORM=arm64  # amd64 또는 arm64
```

- Multi-platform 이미지 빌드 지원 (ARM64/AMD64)
- 이미지 태그: `sk019-posts-get.arm64:1.0`

#### 4. Docker 푸시 스크립트 (docker-push.sh)

- Harbor 레지스트리에 이미지 푸시
- 레지스트리: `amdp-registry.skala-ai.com/skala25a`
- 자동 로그인 및 이미지 태깅

#### 5. Kubernetes 매니페스트

**Deployment (deploy.yaml)**

```yaml
namespace: skala-practice
replicas: 1
image: amdp-registry.skala-ai.com/skala25a/sk019-posts-get:1.0
containerPort: 80
```

**Service (service.yaml)**

```yaml
type: ClusterIP
port: 80
targetPort: 80
```

#### 6. 환경 설정 (deploy/env.properties)

사용자 커스터마이징 영역:

- `USER_NAME`: sk019
- `NAMESPACE`: skala-practice
- `VERSION`: 1.0
- `CPU_PLATFORM`: arm64

### 배포 워크플로우

```text
1. 개발
   └── src/index.html 작성 (개인 프로필 페이지)

2. Docker 이미지 빌드
   └── ./docker-build.sh
       ├── Dockerfile 기반 이미지 생성
       └── ARM64/AMD64 플랫폼 지정

3. 이미지 레지스트리 푸시
   └── ./docker-push.sh
       ├── Harbor 레지스트리 로그인
       ├── 이미지 태깅
       └── 푸시

4. Kubernetes 배포
   └── kubectl apply -f deploy.yaml -f service.yaml
       ├── Deployment 생성 (Pod 1개)
       └── Service 생성 (ClusterIP)
```

### 기술 스택

- **컨테이너**: Docker
- **웹 서버**: Nginx (Alpine)
- **오케스트레이션**: Kubernetes
- **레지스트리**: Harbor
- **플랫폼**: Linux (ARM64/AMD64)

### 웹사이트 내용

개인 프로필 웹사이트 ([src/index.html](01-Docker-배포-실습/src/index.html)):

- 개인 정보 및 소개
- 학력, 경력, 프로젝트 경험
- 미디어 갤러리
- 반응형 디자인

### 접속 방법

배포 후 접속 URL:

```
http://<kubernetes-ingress>/sk019/
```

### 학습 목표

1. Docker 이미지 빌드 및 멀티플랫폼 지원
2. Nginx 설정 및 정적 파일 서빙
3. Docker 레지스트리 사용 (Harbor)
4. Kubernetes Deployment 및 Service 배포
5. 쉘 스크립트를 활용한 배포 자동화
6. 환경 설정 파일 관리

## 참고 사항

- 레지스트리 자격 증명은 `env.properties` 및 `docker-push.sh`에 하드코딩되어 있음 (실무에서는 보안 관리 필요)
- ARM64 플랫폼 기본 설정 (Apple Silicon 환경)
- Namespace: `skala-practice`
