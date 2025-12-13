from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import data

app = FastAPI(
    title="BRAI API Prototype",
    version="1.0.0",
    description="Implements the endpoints described in spec/API_SPECIFICATION_v1.1.md",
)


def _not_found(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"success": False, "code": 404, "errorMessage": message},
    )


@app.get("/api/dataset")
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
def get_dataset(dataset_id: str) -> JSONResponse:
    dataset = data.get_dataset(dataset_id)
    if dataset is None:
        return _not_found("데이터세트를 찾을 수 없습니다")

    return JSONResponse(content={"success": True, "data": [dataset]})


@app.get("/api/strains/{strain_id}")
def get_strain(strain_id: str) -> JSONResponse:
    strain = data.get_strain(strain_id)
    if strain is None:
        return _not_found("계통을 찾을 수 없습니다")

    return JSONResponse(content={"success": True, "data": [strain]})


@app.get("/")
def root() -> dict:
    return {"success": True, "message": "BRAI API server is running"}
