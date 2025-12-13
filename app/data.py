from __future__ import annotations

from random import randint, random
from typing import Dict, List

from .models import Metadata, Phenotype, PredictionResult, Strain

# 간단한 메모리 데이터베이스
STRAINS: Dict[str, Strain] = {
    "TC1_022": Strain(
        id="TC1_022",
        name="TC1_022",
        type="both",
        phenotype=Phenotype(
            weight=47.24,
            length=44.38,
            width=38.59,
            ratio=1.15,
            sugarContent=5.24,
            firmness=0.51,
            skinThickness=6.81,
            shape="round",
        ),
        metadata=Metadata(
            source="strains folder",
            createdAt="2025-11-16T16:16:04.742Z",
            imageUrl="/images/tomato/strains/TC1_022.png",
        ),
    ),
    "TC1_023": Strain(
        id="TC1_023",
        name="TC1_023",
        type="female",
        phenotype=Phenotype(
            weight=40.12,
            length=42.0,
            width=36.0,
            ratio=1.17,
            sugarContent=5.5,
            firmness=0.48,
            skinThickness=6.2,
            shape="oval",
        ),
        metadata=Metadata(
            source="strains folder",
            createdAt="2025-10-12T08:12:04.742Z",
            imageUrl="/images/tomato/strains/TC1_023.png",
        ),
    ),
    "TC1_026": Strain(
        id="TC1_026",
        name="TC1_026",
        type="male",
        phenotype=Phenotype(
            weight=50.0,
            length=43.0,
            width=39.0,
            ratio=1.1,
            sugarContent=5.0,
            firmness=0.55,
            skinThickness=7.0,
            shape="round",
        ),
        metadata=Metadata(
            source="strains folder",
            createdAt="2025-09-02T10:00:00.000Z",
            imageUrl="/images/tomato/strains/TC1_026.png",
        ),
    ),
}

PREDICTIONS: Dict[str, PredictionResult] = {}


def list_strains(strain_type: str | None = None, search: str | None = None) -> List[Strain]:
    strains = list(STRAINS.values())
    if strain_type:
        strain_type = strain_type.lower()
        strains = [strain for strain in strains if strain.type == strain_type]
    if search:
        lowered = search.lower()
        strains = [
            strain for strain in strains if lowered in strain.id.lower() or lowered in strain.name.lower()
        ]
    return strains


def get_strain(strain_id: str) -> Strain | None:
    return STRAINS.get(strain_id)


def _build_combination_key(male_id: str, female_id: str) -> str:
    return f"{female_id}-{male_id}"


def _generate_prediction_id() -> str:
    random_hash = randint(10**7, 10**8 - 1)
    return f"PRED_{randint(1_700_000_000_000, 1_800_000_000_000)}_{random_hash:08d}"


def create_prediction(male: Strain, female: Strain, generate_images: bool) -> PredictionResult:
    prediction_id = _generate_prediction_id()
    combination_key = _build_combination_key(male.id, female.id)

    predicted = {
        "weight": {"value": round((male.phenotype.weight + female.phenotype.weight) / 2, 2), "confidence": 0.9, "grade": 3},
        "length": {"value": round((male.phenotype.length + female.phenotype.length) / 2, 2), "confidence": 0.88, "grade": 3},
        "sugarContent": {"value": round((male.phenotype.sugarContent + female.phenotype.sugarContent) / 2, 2), "confidence": 0.9, "grade": 3},
        "firmness": {"value": round((male.phenotype.firmness + female.phenotype.firmness) / 2, 2), "confidence": 0.86, "grade": 3},
        "shape": {"value": male.phenotype.shape, "confidence": 0.95},
    }

    generated_images = None
    if generate_images:
        generated_images = [
            f"/images/tomato/predictions/2025/11/cross_{male.id}_{female.id}_01.png",
            f"/images/tomato/predictions/2025/11/cross_{male.id}_{female.id}_02.png",
        ]

    result = PredictionResult(
        id=prediction_id,
        maleStrain=male,
        femaleStrain=female,
        predictedPhenotype=predicted,
        generatedImages=generated_images,
        overallScore=round(random() * 5, 2),
        recommendation="중과종으로 다용도 활용 가능. 가공용으로 활용 권장",
        createdAt=PredictionResult.build_timestamp(),
    )

    PREDICTIONS[prediction_id] = result
    PREDICTIONS[combination_key] = result
    return result


def find_prediction(prediction_id: str) -> PredictionResult | None:
    return PREDICTIONS.get(prediction_id)


def find_prediction_by_combination(male_id: str, female_id: str) -> PredictionResult | None:
    return PREDICTIONS.get(_build_combination_key(male_id, female_id))


def list_predictions(page: int, limit: int, sort: str) -> List[PredictionResult]:
    predictions = [p for key, p in PREDICTIONS.items() if not key.startswith("TC") and not "-" in key]
    predictions.sort(key=lambda p: p.createdAt, reverse=(sort.lower() != "asc"))
    start = (page - 1) * limit
    end = start + limit
    return predictions[start:end]


def existing_combinations() -> Dict[str, int | List[str]]:
    combination_keys = [key for key in PREDICTIONS if "-" in key]
    return {"combinationIds": combination_keys, "total": len(combination_keys)}
