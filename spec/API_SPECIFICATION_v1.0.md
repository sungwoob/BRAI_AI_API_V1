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

#### 4.1.1 전체 계통 조회
```
GET /api/strains
```

**설명**: 사용 가능한 모든 계통 목록을 조회하며, 선택적 필터링 가능

**Query 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|-----------|------|----------|---------|-------------|
| type | string | 아니오 | - | 타입별 필터: `male`, `female`, `both` |
| search | string | 아니오 | - | 이름이나 ID로 검색 (대소문자 무관) |

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
        "sugarContent": 5.24,
        "firmness": 0.51,
        "skinThickness": 6.81,
        "shape": "round"
      },
      "metadata": {
        "source": "strains folder",
        "createdAt": "2025-11-16T16:16:04.742Z",
        "imageUrl": "/images/tomato/strains/TC1_022.png"
      }
    }
  ],
  "total": 50
}
```

**요청 예시**:
```bash
curl -X GET "https://api.brai.example.com/api/strains?type=female&search=TC1"
```

#### 4.1.2 특정 계통 상세 조회
```
GET /api/strains/:id
```

**설명**: 특정 계통의 상세 정보 조회

**경로 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|-----------|------|----------|-------------|
| id | string | 예 | 계통 ID (예: TC1_022) |

**응답 예시**:
```json
{
  "success": true,
  "data": {
    "id": "TC1_022",
    "name": "TC1_022",
    "type": "both",
    "phenotype": {
      "weight": 47.24,
      "length": 44.38,
      "width": 38.59,
      "ratio": 1.15,
      "sugarContent": 5.24,
      "firmness": 0.51,
      "skinThickness": 6.81,
      "shape": "round"
    },
    "metadata": {
      "source": "strains folder",
      "createdAt": "2025-11-16T16:16:04.742Z",
      "imageUrl": "/images/tomato/strains/TC1_022.png"
    }
  }
}
```

**에러 응답 (404)**:
```json
{
  "success": false,
  "error": "계통을 찾을 수 없습니다"
}
```

### 4.2 예측(Predictions) API

#### 4.2.1 예측 생성
```
POST /api/predictions
```

**설명**: 두 부모 계통 간의 새로운 교배 예측 생성

**요청 본문**:
```json
{
  "maleStrainId": "TC1_022",
  "femaleStrainId": "TC1_023",
  "options": {
    "predictPhenotype": true,
    "generateImage": true
  }
}
```

**요청 필드**:
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|-------|------|----------|---------|-------------|
| maleStrainId | string | 예 | - | 부친 계통 ID |
| femaleStrainId | string | 예 | - | 모친 계통 ID |
| options.predictPhenotype | boolean | 아니오 | true | 표현형 예측 여부 |
| options.generateImage | boolean | 아니오 | false | 시각화 이미지 생성 여부 |

**응답 예시**:
```json
{
  "success": true,
  "data": {
    "id": "PRED_1763366644698_a3f2b1c4",
    "maleStrain": { /* 전체 계통 객체 */ },
    "femaleStrain": { /* 전체 계통 객체 */ },
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
      "sugarContent": {
        "value": 5.32,
        "confidence": 0.90,
        "grade": 3
      },
      "firmness": {
        "value": 0.53,
        "confidence": 0.86,
        "grade": 3
      },
      "shape": {
        "value": "round",
        "confidence": 0.95
      }
    },
    "generatedImages": [
      "/images/tomato/predictions/2025/11/cross_TC1_022_TC1_023_01.png",
      "/images/tomato/predictions/2025/11/cross_TC1_022_TC1_023_02.png"
    ],
    "overallScore": 3.2,
    "recommendation": "중과종으로 다용도 활용 가능. 가공용으로 활용 권장",
    "createdAt": "2025-11-17T08:30:00.000Z"
  },
  "message": "예측이 성공적으로 완료되었습니다"
}
```

**에러 응답 (400)**:
```json
{
  "success": false,
  "error": "부친과 모친 계통 ID가 필요합니다"
}
```

#### 4.2.2 예측 이력 조회
```
GET /api/predictions
```

**설명**: 페이지네이션된 예측 이력 목록 조회

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
      "maleStrain": { /* 계통 객체 */ },
      "femaleStrain": { /* 계통 객체 */ },
      "predictedPhenotype": { /* 표현형 데이터 */ },
      "overallScore": 3.2,
      "createdAt": "2025-11-17T08:30:00.000Z"
    }
  ],
  "total": 45,
  "page": 1,
  "limit": 10,
  "hasMore": true
}
```

#### 4.2.3 ID로 예측 조회
```
GET /api/predictions/:id
```

**설명**: ID로 특정 예측 조회

**경로 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|-----------|------|----------|-------------|
| id | string | 예 | 예측 ID |

**응답**: 예측 생성 응답 데이터와 동일

**에러 응답 (404)**:
```json
{
  "success": false,
  "error": "예측을 찾을 수 없습니다"
}
```

#### 4.2.4 조합으로 예측 조회
```
GET /api/predictions/by-combination/:maleId/:femaleId
```

**설명**: 특정 부모 계통 조합에 대한 예측 조회

**경로 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|-----------|------|----------|-------------|
| maleId | string | 예 | 부친 계통 ID |
| femaleId | string | 예 | 모친 계통 ID |

**응답**: 예측 생성 응답 데이터와 동일

**에러 응답 (404)**:
```json
{
  "success": false,
  "error": "이 조합에 대한 예측을 찾을 수 없습니다"
}
```

#### 4.2.5 기존 조합 조회
```
GET /api/predictions/existing-combinations
```

**설명**: 모든 기존 예측 조합 ID 목록 조회

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
    "total": 25
  }
}
```

## 5. 데이터 모델

### 5.1 계통(Strain)
```typescript
interface Strain {
  id: string;                                    // 고유 식별자 (예: "TC1_022")
  name: string;                                  // 계통 표시명
  type: 'male' | 'female' | 'both';            // 교배 능력
  phenotype: {
    weight: number;                              // 무게 (g)
    length: number;                              // 길이 (mm)
    width: number;                               // 너비 (mm)
    ratio: number;                               // 길이/너비 비율
    sugarContent: number;                        // 당도 (%)
    firmness: number;                            // 경도 (kg)
    skinThickness: number;                       // 껍질 두께 (mm)
    shape: 'round' | 'oval' | 'rectangular' | 'pear';  // 과실 형태
  };
  metadata?: {
    source?: string;                             // 데이터 출처
    createdAt?: string;                          // ISO 8601 타임스탬프
    imageUrl?: string;                           // 계통 이미지 URL
  };
}
```

### 5.2 예측 요청(PredictionRequest)
```typescript
interface PredictionRequest {
  maleStrainId: string;                         // 부친 계통 ID
  femaleStrainId: string;                       // 모친 계통 ID
  options: {
    predictPhenotype: boolean;                  // 표현형 예측 활성화
    generateImage: boolean;                     // 이미지 생성 활성화
  };
}
```

### 5.3 예측 결과(PredictionResult)
```typescript
interface PredictionResult {
  id: string;                                    // 고유 예측 ID
  maleStrain: Strain;                           // 완전한 부친 데이터
  femaleStrain: Strain;                         // 완전한 모친 데이터
  predictedPhenotype: {
    weight: {
      value: number;                             // 예측 무게
      confidence: number;                        // 신뢰도 (0-1)
      grade?: number;                            // 품질 등급 (1-5)
    };
    length: {
      value: number;
      confidence: number;
      grade?: number;
    };
    sugarContent: {
      value: number;
      confidence: number;
      grade?: number;
    };
    firmness: {
      value: number;
      confidence: number;
      grade?: number;
    };
    shape: {
      value: string;
      confidence: number;
    };
  };
  generatedImages?: string[];                   // 생성된 이미지 URL 배열
  overallScore: number;                         // 종합 품질 점수 (0-5)
  recommendation?: string;                      // 교배 추천 텍스트
  createdAt: string;                            // ISO 8601 타임스탬프
}
```

## 6. 에러 처리

### 6.1 에러 응답 형식
모든 에러는 다음 표준 형식을 따릅니다:
```json
{
  "success": false,
  "error": "사람이 읽을 수 있는 에러 메시지"
}
```

### 6.2 일반적인 에러 메시지
| 에러 메시지 | 원인 | 해결 방법 |
|---------------|-------|------------|
| "계통을 찾을 수 없습니다" | 잘못된 계통 ID | 계통 ID가 존재하는지 확인 |
| "부친과 모친 계통 ID가 필요합니다" | 필수 필드 누락 | 두 부모 계통 ID 모두 포함 |
| "예측을 찾을 수 없습니다" | 잘못된 예측 ID | 예측 ID 확인 |
| "잘못된 조합 키 형식" | 조합 키 형식 오류 | 형식 사용: `femaleId-maleId` |
| "예측 생성에 실패했습니다" | 서버 처리 오류 | 요청 재시도 |

## 7. API 버전 관리

### 7.1 현재 버전
- 버전: 1.0.0
- 출시일: 2025-11-17

### 7.2 버전 전략
- 주요 버전에 대해 URL 경로 버전 관리 사용
- 마이너 버전은 하위 호환성 유지
- 중대한 변경사항은 새로운 주요 버전 필요

### 7.3 지원 중단 정책
- 지원 중단 엔드포인트는 `Deprecation` 헤더로 표시
- 제거 전 최소 6개월 사전 공지
- 마이그레이션 가이드 제공

## 8. 속도 제한

### 8.1 현재 제한 (Phase 1)
- 속도 제한 없음

### 8.2 향후 제한 (Phase 2)
- 15분 창당 100개 요청
- 시간당 1000개 요청
- 인증된 사용자를 위한 맞춤형 제한

## 9. 부록

### 9.1 조합 ID 형식
조합 ID는 다음 패턴을 따릅니다: `{femaleStrainId}-{maleStrainId}`
- 예시: `TC1_023-TC1_022`
- 모친 ID가 항상 먼저 옴
- 구분자는 하이픈(-)

### 9.2 예측 ID 형식
예측 ID는 다음 패턴을 따릅니다: `PRED_{timestamp}_{randomHash}`
- 예시: `PRED_1763366644698_a3f2b1c4`
- 타임스탬프는 Unix 밀리초
- 랜덤 해시는 8자

### 9.3 이미지 URL 형식
생성된 이미지는 다음 패턴을 따릅니다: `/images/tomato/predictions/{year}/{month}/cross_{maleId}_{femaleId}_{sequence}.png`
- 예시: `/images/tomato/predictions/2025/11/cross_TC1_022_TC1_023_01.png`

## 10. 변경 이력

| 버전 | 날짜 | 변경 사항 |
|---------|---------|---------|
| 1.0.0 | 2025-11-17 | 초기 릴리스 |

---

**문서 버전**: 1.0.0
**최종 수정일**: 2025-11-17
**작성자**: BRAI 개발팀
**연락처**: api@brai.example.com