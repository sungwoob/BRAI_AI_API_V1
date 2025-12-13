from __future__ import annotations

from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse

from . import data
from .models import PredictionRequest

app = FastAPI(title="BRAI API", version="1.1.0")


@app.get("/api/strains")
def get_strains(
    type: str | None = Query(None, description="타입별 필터: male, female, both"),
    search: str | None = Query(None, description="이름이나 ID로 검색"),
):
    strains = data.list_strains(type, search)
    return JSONResponse(
        {
            "success": True,
            "data": [strain.dict() for strain in strains],
            "total": len(strains),
        }
    )


@app.get("/api/strains/{strain_id}")
def get_strain_detail(strain_id: str = Path(..., description="계통 ID")):
    strain = data.get_strain(strain_id)
    if not strain:
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": "계통을 찾을 수 없습니다"},
        )
    return JSONResponse({"success": True, "data": strain.dict()})


@app.post("/api/predictions")
def create_prediction(request: PredictionRequest):
    male = data.get_strain(request.maleStrainId)
    female = data.get_strain(request.femaleStrainId)

    if not request.maleStrainId or not request.femaleStrainId:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "부친과 모친 계통 ID가 필요합니다"},
        )

    if not male or not female:
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": "계통을 찾을 수 없습니다"},
        )

    prediction = data.find_prediction_by_combination(male.id, female.id)
    if not prediction:
        prediction = data.create_prediction(male, female, generate_images=request.options.generateImage)

    return JSONResponse({"success": True, "data": prediction.dict(), "message": "예측이 성공적으로 완료되었습니다"})


@app.get("/api/predictions")
def get_predictions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    sort: str = Query("desc", regex="^(asc|desc)$"),
):
    predictions = data.list_predictions(page, limit, sort)
    total = len([p for key, p in data.PREDICTIONS.items() if not key.startswith("TC") and "-" not in key])
    has_more = total > page * limit
    return JSONResponse(
        {
            "success": True,
            "data": [p.dict() for p in predictions],
            "total": total,
            "page": page,
            "limit": limit,
            "hasMore": has_more,
        }
    )


@app.get("/api/predictions/{prediction_id}")
def get_prediction(prediction_id: str):
    prediction = data.find_prediction(prediction_id)
    if not prediction:
        return JSONResponse(status_code=404, content={"success": False, "error": "예측을 찾을 수 없습니다"})
    return JSONResponse({"success": True, "data": prediction.dict()})


@app.get("/api/predictions/by-combination/{male_id}/{female_id}")
def get_prediction_by_combination(male_id: str, female_id: str):
    prediction = data.find_prediction_by_combination(male_id, female_id)
    if not prediction:
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": "이 조합에 대한 예측을 찾을 수 없습니다"},
        )
    return JSONResponse({"success": True, "data": prediction.dict()})


@app.get("/api/predictions/existing-combinations")
def get_existing_combinations():
    combos = data.existing_combinations()
    return JSONResponse({"success": True, "data": combos})


@app.get("/")
def read_root():
    return {
        "success": True,
        "message": "BRAI API 서버가 실행 중입니다",
        "endpoints": [
            "/api/strains",
            "/api/strains/{strain_id}",
            "/api/predictions",
            "/api/predictions/{id}",
            "/api/predictions/by-combination/{maleId}/{femaleId}",
            "/api/predictions/existing-combinations",
        ],
    }
