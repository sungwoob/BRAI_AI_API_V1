from __future__ import annotations

from typing import Dict, List, Optional

# Model metadata keyed by model ID.
MODELS: Dict[str, dict] = {
    "sj_rf": {
        "id": "sj_rf",
        "name": "sj_rf",
        "modelType": "combiationAbility",
        "modelDetail": "radomforest",
        "trainedBy": "AI",
    },
    "keti_ai": {
        "id": "keti_ai",
        "name": "keti_ai",
        "modelType": "combiationAbility",
        "modelDetail": "radomforest",
        "trainedBy": "TC1",
    },
}


def list_models() -> List[str]:
    """Return sorted model identifiers."""

    return sorted(MODELS.keys())


def get_model(model_id: str) -> Optional[dict]:
    """Fetch a single model by its identifier."""

    return MODELS.get(model_id)
