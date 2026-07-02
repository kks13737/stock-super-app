# Architecture: 나만의 주식관리 슈퍼앱

## 1. 기술 방향
- 백엔드: Python FastAPI
- 실행 도구: `uv`
- HTML 파싱: BS4
- 자동 수집: 스케줄러 기반 배치 작업
- 저장소: SQLite
- 프론트엔드: 정적 HTML, CSS, JS

## 2. 시스템 구성

### 2.1 프론트엔드
- 매매일지 캘린더
- 뉴스 목록 화면
- 공포탐욕지수 카드 또는 그래프 영역
- 수동 수집 버튼
- 수집 상태 및 오류 표시
- 백엔드가 `frontend/index.html`, `frontend/styles.css`, `frontend/app.js`를 정적 파일로 서빙

### 2.2 백엔드
- 매매일지 CRUD API
- 뉴스 수집 API
- 공포탐욕지수 수집 API
- 스케줄러 실행 모듈
- 공통 예외 처리 및 로깅

### 2.3 수집 모듈
- `naver_news_crawler`
  - 네이버 증권 뉴스 목록 페이지 파싱
  - 기사 메타데이터 추출
- `cnn_fear_greed_crawler`
  - CNN 공포탐욕지수 페이지 파싱
  - 현재 지수와 상태 추출

## 3. 권장 프로젝트 구조

```text
backend/
  app/
    api/
    services/
    crawlers/
    models/
    repositories/
    schedulers/
    utils/
  tests/
frontend/
  index.html
  styles.css
  app.js
docs/
  PRD.md
  Architecture.md
  Operation.md
  index.html
```

## 4. 모듈별 역할

### 4.1 `api`
- 클라이언트 요청을 받는 진입점
- 수동 수집, 매매일지 저장, 조회 요청 처리

### 4.2 `services`
- 비즈니스 로직 담당
- 중복 저장 체크
- 수집 결과 정규화
- 날짜별 집계

### 4.3 `crawlers`
- BS4 기반 파싱 전용 모듈
- HTML 구조 변경 시 이 레이어만 우선 수정

### 4.4 `models`
- 매매일지, 뉴스 기사, 공포탐욕지수 데이터 모델 정의

### 4.5 `repositories`
- DB 접근 전담
- 저장, 조회, 중복 검사

### 4.6 `schedulers`
- 9시(KST) 뉴스 수집
- 6시간마다 공포탐욕지수 수집
- 수동 실행과 충돌하지 않도록 작업 잠금 관리

### 4.7 `utils`
- 날짜/시간 처리
- KST 변환
- 로깅 헬퍼
- 파서 공통 함수

### 4.8 정적 FE 서빙
- 백엔드가 `/assets` 경로로 프론트 정적 파일을 노출한다.
- 브라우저는 루트(`/`)에서 `index.html`을 받아 단일 화면 앱처럼 동작한다.

## 5. 데이터 모델 초안

### 5.1 `trade_journal`
- `id`
- `trade_date`
- `ticker`
- `stock_name`
- `side` `buy | sell | hold`
- `quantity`
- `price`
- `memo`
- `created_at`
- `updated_at`

### 5.2 `news_article`
- `id`
- `source`
- `title`
- `url`
- `publisher`
- `published_at`
- `summary`
- `fetched_at`
- `created_at`

### 5.3 `fear_greed_index`
- `id`
- `source`
- `index_value`
- `state_label`
- `fetched_at`
- `created_at`

### 5.4 `crawl_job_log`
- `id`
- `job_type`
- `status`
- `started_at`
- `finished_at`
- `error_message`
- `payload`

## 6. 실행 흐름

### 6.1 뉴스 자동 수집
1. 스케줄러가 매일 9시(KST)에 작업 시작
2. 크롤러가 네이버 증권 뉴스 목록 페이지 요청
3. BS4로 기사 목록 파싱
4. 서비스 계층에서 정규화 및 중복 제거
5. DB 저장 후 결과 로그 기록

### 6.2 공포탐욕지수 자동 수집
1. 스케줄러가 6시간 주기로 작업 시작
2. CNN 페이지 요청
3. 지수 값과 상태 추출
4. DB 저장 및 최신 상태 갱신

### 6.3 수동 수집
1. 사용자가 버튼 클릭
2. API가 수집 작업을 직접 호출
3. 결과를 즉시 UI에 반환

## 7. 기술적 요구사항
- 크롤러는 HTML 구조 변경에 대비해 선택자와 파싱 로직을 분리한다.
- 수집 데이터는 중복 방지 키를 둔다. 예: `source + url`, `source + fetched_at`
- 스케줄 작업은 동일 작업의 중복 실행을 막아야 한다.
- 실패 시 재시도 정책과 에러 로그를 남긴다.
- 시간 기준은 KST로 통일한다.

## 8. 품질 기준
- 수집 성공/실패 여부를 확인할 수 있어야 한다.
- 운영 시 파서 오류를 빠르게 추적할 수 있어야 한다.
- 날짜 조회와 최근 수집 현황은 빠르게 응답해야 한다.
