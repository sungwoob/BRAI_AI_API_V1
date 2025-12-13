from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Phenotype(BaseModel):
    weight: float
    length: float
    width: float
    ratio: float
    sugarContent: float
    firmness: float
    skinThickness: float
    shape: str


class Metadata(BaseModel):
    source: Optional[str] = None
    createdAt: Optional[str] = None
    imageUrl: Optional[str] = None


class Strain(BaseModel):
    id: str
    name: str
    type: str
    phenotype: Phenotype
    metadata: Optional[Metadata] = None

    @validator("type")
    def validate_type(cls, value: str) -> str:
        if value not in {"male", "female", "both"}:
            raise ValueError("type must be one of: male, female, both")
        return value


class PredictionOptions(BaseModel):
    predictPhenotype: bool = True
    generateImage: bool = False


class PredictionRequest(BaseModel):
    maleStrainId: str
    femaleStrainId: str
    options: PredictionOptions = Field(default_factory=PredictionOptions)


class PhenotypePrediction(BaseModel):
    value: float | str
    confidence: float
    grade: Optional[int] = None


class PredictionResult(BaseModel):
    id: str
    maleStrain: Strain
    femaleStrain: Strain
    predictedPhenotype: dict
    generatedImages: Optional[List[str]] = None
    overallScore: float
    recommendation: Optional[str] = None
    createdAt: str

    @staticmethod
    def build_timestamp() -> str:
        return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


class PaginatedResponse(BaseModel):
    success: bool
    data: List[PredictionResult]
    total: int
    page: int
    limit: int
    hasMore: bool
