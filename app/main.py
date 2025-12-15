from __future__ import annotations

from typing import Dict, Optional

from fastapi import Body, FastAPI, Query
from fastapi.responses import JSONResponse

from app import data

app = FastAPI(
    title="BRAI API Prototype",
    version="1.0.0",
    description="Implements the endpoints described in spec/API_SPECIFICATION_v1.3.md",
)


def _not_found(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"success": False, "code": 404, "errorMessage": message},
    )


@app.get("/api/dataset")
@app.post("/api/dataset")
def list_dataset() -> JSONResponse:
    datasets = data.list_datasets()
    return JSONResponse(
        content={
            "success": True,
            "data": [
                {
                    "datasets": datasets,
                    "numberOfDatasets": len(datasets),
                }
            ],
        }
    )


@app.get("/api/dataset/{dataset_id}")
@app.post("/api/dataset/{dataset_id}")
def get_dataset(dataset_id: str) -> JSONResponse:
    dataset = data.get_dataset(dataset_id)
    if dataset is None:
        return _not_found("데이터세트를 찾을 수 없습니다")

    return JSONResponse(content={"success": True, "data": [dataset]})


@app.get("/api/strains/{strain_id}")
@app.post("/api/strains/{strain_id}")
def get_strain(strain_id: str) -> JSONResponse:
    strain = data.get_strain(strain_id)
    if strain is None:
        return _not_found("계통을 찾을 수 없습니다")

    return JSONResponse(content={"success": True, "data": [strain]})


@app.get("/api/models")
@app.post("/api/models")
def list_models() -> JSONResponse:
    models = data.list_models()
    return JSONResponse(
        content={
            "success": True,
            "data": [
                {
                    "models": models,
                    "numberOfDatasets": len(models),
                }
            ],
        }
    )


@app.get("/api/models/{model_id}")
@app.post("/api/models/{model_id}")
def get_model(model_id: str) -> JSONResponse:
    model = data.get_model(model_id)
    if model is None:
        return _not_found("모델을 찾을 수 없습니다")

    return JSONResponse(content={"success": True, "data": [model]})


@app.get("/")
def root() -> dict:
    return {"success": True, "message": "BRAI API server is running"}


def _bad_request(error: str) -> JSONResponse:
    return JSONResponse(status_code=400, content={"success": False, "error": error})


def _validate_prediction_inputs(payload: Optional[Dict]) -> Optional[JSONResponse]:
    if payload is None:
        return _bad_request("요청 본문이 필요합니다.")

    dataset_id = payload.get("dataset")
    model_id = payload.get("model")
    male_id = payload.get("maleStrainId")
    female_id = payload.get("femaleStrainId")

    if not male_id or not female_id:
        return _bad_request("부친과 모친 계통 ID가 필요합니다.")
    if not model_id:
        return _bad_request("사용할 모델 ID가 필요합니다.")
    if not dataset_id:
        return _bad_request("데이터세트 ID가 필요합니다.")

    if data.get_dataset(dataset_id) is None:
        return _bad_request("데이터세트를 찾을 수 없습니다.")
    if data.get_model(model_id) is None:
        return _bad_request("모델 ID가 존재하지 않습니다.")

    dataset = data.get_dataset(dataset_id)
    if male_id not in dataset["strains"] or female_id not in dataset["strains"]:
        return _bad_request("계통 ID가 존재하지 않습니다.")
    if data.get_strain(male_id) is None or data.get_strain(female_id) is None:
        return _bad_request("계통 ID가 존재하지 않습니다.")

    return None


@app.post("/api/predictions")
def create_prediction(payload: Optional[Dict] = Body(default=None)) -> JSONResponse:
    validation_error = _validate_prediction_inputs(payload)
    if validation_error:
        return validation_error

    dataset_id = payload.get("dataset")
    model_id = payload.get("model")
    male_id = payload.get("maleStrainId")
    female_id = payload.get("femaleStrainId")

    prediction = data.create_prediction(dataset_id, model_id, male_id, female_id)
    return JSONResponse(
        content={
            "success": True,
            "model": model_id,
            "dataset": dataset_id,
            "maleStrainId": male_id,
            "femaleStrainId": female_id,
            "data": prediction,
        }
    )


@app.get("/api/predictions")
def list_predictions(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    sort: str = Query(default="desc", regex="^(asc|desc)$"),
) -> JSONResponse:
    results = data.list_predictions(page, limit, sort)
    return JSONResponse(
        content={
            "success": True,
            "data": results["items"],
            "total": results["total"],
            "page": results["page"],
            "limit": results["limit"],
            "hasMore": results["hasMore"],
        }
    )


@app.post("/api/predictions/existingCombinations")
def list_existing_combinations() -> JSONResponse:
    combinations = data.list_combinations()
    return JSONResponse(
        content={
            "success": True,
            "data": {
                "combinationIds": combinations,
                "numberOfCombination": len(combinations),
            },
        }
    )


@app.get("/api/predictions/byCombination")
def get_prediction_by_combination(
    maleId: str = Query(alias="maleId"), femaleId: str = Query(alias="femaleId")
) -> JSONResponse:
    prediction = data.get_prediction_by_combination(maleId, femaleId)
    if prediction is None:
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": "이 조합에 대한 예측을 찾을 수 없습니다"},
        )

    return JSONResponse(
        content={
            "success": True,
            "model": prediction["model"],
            "dataset": prediction["dataset"],
            "maleStrainId": prediction["maleStrainId"],
            "femaleStrainId": prediction["femaleStrainId"],
            "data": {
                "id": prediction["id"],
                "predictedPhenotype": prediction["predictedPhenotype"],
                "createdAt": prediction["createdAt"],
            },
        }
    )
