# BRAI 백엔드 API 명세서 v1.0

## 1. 개요

### 1.1 일반 정보
- **API 버전**: 1.0.0
- **출시일**: 2025-11-17
- **Base URL (운영)**: `https://api.brai.example.com`
- **Base URL (스테이징)**: `https://staging-api.brai.example.com`
- **Base URL (개발)**: `http://localhost:8000`
- **프로토콜**: HTTPS (운영/스테이징), HTTP (개발)

### 1.2 요청/응답 형식
- **Content-Type**: `application/json`
- **Accept**: `application/json`
- **문자 인코딩**: UTF-8
- **날짜/시간 형식**: ISO 8601 (예: `2025-11-17T08:30:00.000Z`)

### 1.3 인증
- **현재 (Phase 1)**: 인증 없음
- **향후 (Phase 2)**: JWT Bearer Token
  ```
  Authorization: Bearer <token>
  ```

## 2. 공통 응답 형식

### 2.1 성공 응답
```json
{
  "success": true,
  "data": { ... },
  "message": "선택적 성공 메시지"
}
```

### 2.2 에러 응답
```json
{
  "success": false,
  "error": "에러 메시지 설명"
}
```

### 2.3 페이지네이션 응답
```json
{
  "success": true,
  "data": [ ... ],
  "total": 100,
  "page": 1,
  "limit": 10,
  "hasMore": true
}
```

## 3. HTTP 상태 코드

| 코드 | 설명 | 사용 |
|------|-------------|--------|
| 200 | 성공 | GET, PUT, DELETE 요청 성공 |
| 201 | 생성됨 | POST 요청으로 새 리소스 생성 |
| 400 | 잘못된 요청 | 유효하지 않은 파라미터나 본문 |
| 404 | 찾을 수 없음 | 리소스를 찾을 수 없음 |
| 500 | 서버 오류 | 서버 내부 오류 |

## 4. 핵심 API 엔드포인트

### 4.1 계통(Strains) API

### 4.1.1 데이터 세트 조회
```
GET /api/dataset
```

**설명**: 사용 가능한 모든 데이터세트 목록을 조회

**Query 파라미터**:
None

**응답 예시**:
```json
{
  "success": true,
  "data": [
    {
      "datasets": ["TC1","AI"],
      "numberOfDatasets": 2
    }
  ]
}
```

**요청 예시**:
```bash
curl -X POST "https://api.brai.example.com/api/dataset"
```

### 4.1.2 데이터 세트 상세 조회
```
POST /api/dataset/:id
```

**설명**: 특정 데이터세트의 상세 조회

**Query 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|-----------|------|----------|-------------|
| id | string | 예 | 데이터세트 ID (예: TC1) |

**응답 예시**:
```json
{
  "success": true,
  "data": [
    {
      "id": "TC1",
      "name": "TC1",
      "strains": ["TC1_001", "TC1_002","TC1_003"],
      "phenotype": [
        "weight",
        "length",
        "width",
        "ratio",
        "brix",
        "firmness",
        "skinThickness",
        "shape"
      ],
      "snpInfo" : {
        "chr" : ["1","1","1","1","1"],
        "bp" : ["20288", "62862", "65279", "65409", "65869"],
        "numberOfSNP": 5
      }
    }
  ]
}
```

**요청 예시**:
```bash
curl -X POST "https://api.brai.example.com/api/dataset/{dataset_id}"
```

#### 4.1.3 특정 계체 상세 조회
```
POST /api/strains/:id
```

**설명**: 특정 계통의 상세 정보 조회

**Query 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|-----------|------|----------|-------------|
| id | string | 예 | 계통 ID (예: TC1_022) |

**응답 예시**:
```json
{
  "success": true,
  "data": [
    {
      "id": "TC1_022",
      "name": "TC1_022",
      "type": "both",
      "phenotype": {
        "weight": 47.24,
        "length": 44.38,
        "width": 38.59,
        "ratio": 1.15,
        "brix": 5.24,
        "firmness": 0.51,
        "skinThickness": 6.81,
        "shape": "round"
      }
    }
  ]
}
```

**에러 응답 (404)**:
```json
{
  "success": false,
  "code": 404,
  "errorMessage": "계통을 찾을 수 없습니다"
}
```

**요청 예시**:
```bash
curl -X POST "https://api.brai.example.com/api/strains/{strain_id}"
```

### 4.2 AI 모델(Predictions) API

### 4.2.1 예측 모델 조회
```
POST /api/models
```

**설명**: 사용 가능한 모든 AI 모델 목록을 조회

**Query 파라미터**:
None

**응답 예시**:
```json
{
  "success": true,
  "data": [
    {
      "models": ["sj_rf","keti_ai"],
      "numberOfDatasets": 2
    }
  ]
}
```

**요청 예시**:
```bash
curl -X POST "https://api.brai.example.com/api/models"
```

### 4.2.2 특정 예측의 상세 조회
```
POST /api/models/:id
```

**설명**: 특정 AI 모델의 상세 정보 조회

**Query 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|-----------|------|----------|-------------|
| id | string | 예 | 모델 ID (예: keti_ai) |

**응답 예시**:
```json
{
  "success": true,
  "data": [
    {
      "id": "keti_ai",
      "name": "keti_ai",
      "modelType" : "combiationAbility",
      "modelDetail" : "radomforest",
      "trainedBy": "TC1"
    }
  ]
}
```

**요청 예시**:
```bash
curl -X GET "https://api.brai.example.com/api/models/{model_id}"
```

### 4.3 예측(Predictions) API

#### 4.3.1 예측 생성
```
POST /api/predictions
```

**설명**: 두 부모 계통 간의 새로운 교배 예측 생성, 이미 교배 예측이 생성된 경우 pandas.dataframe에서 이력 관리, csv 파일로 저장하고 api가 실행될 때 이력을 load

**Query 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|-----------|------|----------|-------------|
| dataset | string | 예 | 데이터세트 ID (예: TC1) |
| model | string | 예 | 모델 ID (예: keti_ai) |

**응답 예시**:
```json
{
  "success": true,
  "model": "keti_ai",
  "dataset": "TC1",
  "maleStrainId": "TC1_022",
  "femaleStrainId": "TC1_023",
  "data"{
    "id": "PRED_{현재시간(분,초)}",
    "predictedPhenotype": {
      "weight": {
        "value": 34.89,
        "confidence": 0.92,
        "grade": 3
      },
      "length": {
        "value": 37.31,
        "confidence": 0.88,
        "grade": 3
      },
      "width": {
        "value": 15.31,
        "confidence": 0.75,
        "grade": 3
      },
      "ratio": {
        "value": 4.32,
        "confidence": 0.92,
        "grade": 3
      },
      "brix": {
        "value": 5.32,
        "confidence": 0.90,
        "grade": 3
      },
      "firmness": {
        "value": 0.53,
        "confidence": 0.86,
        "grade": 3
      },
      "skinThickness": {
        "value": 1.11,
        "confidence": 0.94
      },
      "shape": {
        "value": "round",
        "confidence": 0.95
      }
    },
    "createdAt": "{현재시간(ISO 8601)}"
  }
}
```

**요청 본문**:
```json
{
  "dataset": "TC1",
  "model": "keti_ai", 
  "maleStrainId": "TC1_022",
  "femaleStrainId": "TC1_023"
}
```

**에러 응답 (400)**:
```json
{
  "success": false,
  "error": "부친과 모친 계통 ID가 필요합니다."
}
```

```json
{
  "success": false,
  "error": "사용할 모델 ID가 필요합니다."
}
```

```json
{
  "success": false,
  "error": "계통 ID가 존재하지 않습니다."
}
```

#### 4.3.2 예측 이력 조회
```
GET /api/predictions
```

**설명**: 교배 예측 이력 정보에 대한 페이지네이션된 예측 이력 전체 목록 조회

**Query 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|-----------|------|----------|---------|-------------|
| page | integer | 아니오 | 1 | 페이지 번호 (1부터 시작) |
| limit | integer | 아니오 | 10 | 페이지당 항목 수 |
| sort | string | 아니오 | desc | 정렬 순서: `asc` 또는 `desc` |

**응답 예시**:
```json
{
  "success": true,
  "data": [
    {
      "id": "PRED_1763366644698_a3f2b1c4",
      "maleStrain": "TC1_001",
      "femaleStrain": "TC1_002",
      "predictedPhenotype": { /* 표현형 데이터 */ },
      "createdAt": "2025-11-17T08:30:00.000Z"
    }
  ],
  "total": 45,
  "page": 1,
  "limit": 10
}
```

**요청 예시**:
```bash
curl -X GET "https://api.brai.example.com/api/predictions?page=1&limit=10&sort=asc"
```

#### 4.3.3 기존 조합 조회
```
POST /api/predictions/existingCombinations
```

**설명**: 교배 예측 이력 정보에서 기존 예측 조합 부모 ID 전체 목록 조회

**응답 예시**:
```json
{
  "success": true,
  "data": {
    "combinationIds": [
      "TC1_023-TC1_022",
      "TC1_026-TC1_022",
      "TC1_027-TC1_022"
    ],
    "numberOfCombination": 3
  }
}
```

#### 4.2.4 조합으로 예측 조회
```
GET /api/predictions/byCombination
```

**설명**: 특정 부모 계통 조합에 대한 예측 조회

**경로 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|-----------|------|----------|-------------|
| maleId | string | 예 | 부친 계통 ID |
| femaleId | string | 예 | 모친 계통 ID |

**응답**:
```json
{
  "success": true,
  "model": "keti_ai",
  "dataset": "TC1",
  "maleStrainId": "TC1_022",
  "femaleStrainId": "TC1_023",
  "data"{
    "id": "PRED_{현재시간(분,초)}",
    "predictedPhenotype": {
      "weight": {
        "value": 34.89,
        "confidence": 0.92,
        "grade": 3
      },
      "length": {
        "value": 37.31,
        "confidence": 0.88,
        "grade": 3
      },
      "width": {
        "value": 15.31,
        "confidence": 0.75,
        "grade": 3
      },
      "ratio": {
        "value": 4.32,
        "confidence": 0.92,
        "grade": 3
      },
      "brix": {
        "value": 5.32,
        "confidence": 0.90,
        "grade": 3
      },
      "firmness": {
        "value": 0.53,
        "confidence": 0.86,
        "grade": 3
      },
      "skinThickness": {
        "value": 1.11,
        "confidence": 0.94
      },
      "shape": {
        "value": "round",
        "confidence": 0.95
      }
    },
    "createdAt": "2025-11-17T08:30:00.000Z"
  }
}
```

**에러 응답 (404)**:
```json
{
  "success": false,
  "error": "이 조합에 대한 예측을 찾을 수 없습니다"
}
```

**요청 예시**:
```bash
curl -X GET "https://api.brai.example.com/api/predictions/byCombination?maleId=TC1_022&femaleId=TC1_023"
```
