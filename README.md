# BRAI AI API v1

FastAPI 기반으로 작성된 BRAI 백엔드 API 모의 서버입니다. `spec/API_SPECIFICATION_v1.0.md`에 정의된 주요 엔드포인트를 구현하며, 메모리 내 가짜 데이터를 반환합니다.

## 필수 조건
- Python 3.11+

## 설치 및 실행
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 주요 엔드포인트
- `GET /api/strains` — 계통 목록 조회 (타입, 검색 필터 지원)
- `GET /api/strains/{strain_id}` — 특정 계통 상세 조회
- `POST /api/predictions` — 교배 예측 생성 (조합 재사용 지원)
- `GET /api/predictions` — 예측 목록 페이지네이션 조회
- `GET /api/predictions/{id}` — ID로 예측 조회
- `GET /api/predictions/by-combination/{maleId}/{femaleId}` — 부모 조합으로 예측 조회
- `GET /api/predictions/existing-combinations` — 저장된 조합 ID 목록 조회

루트 경로 `/`는 서버 상태와 주요 엔드포인트 목록을 반환합니다.
