from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import joblib
import numpy as np
import pandas as pd

MODEL_ROOT = Path(__file__).resolve().parent / "model"


def _model_directory(model_id: str) -> Path:
    return MODEL_ROOT / model_id


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _load_description(model_dir: Path) -> Optional[dict]:
    description_path = model_dir / "description.json"
    if not description_path.exists():
        return None
    return _load_json(description_path)


def _load_meta(model_dir: Path) -> Optional[dict]:
    meta_path = model_dir / "model_meta.json"
    if not meta_path.exists():
        return None
    return _load_json(meta_path)


def list_models() -> List[str]:
    """Return sorted model identifiers discovered in the model directory."""

    if not MODEL_ROOT.exists():
        return []

    model_ids = [
        path.name for path in MODEL_ROOT.iterdir() if (path / "description.json").exists()
    ]
    return sorted(model_ids)


def get_model(model_id: str) -> Optional[dict]:
    """Fetch model metadata by reading its description and meta files."""

    model_dir = _model_directory(model_id)
    description = _load_description(model_dir)
    meta = _load_meta(model_dir)

    if description is None or meta is None:
        return None

    return {
        **description,
        "traits": meta.get("traits", []),
        "lineIds": meta.get("line_ids", []),
        "n_pc": meta.get("n_pc"),
    }


def _make_cross_feature_from_pc(pc_df: pd.DataFrame, male_id: str, female_id: str, n_pc: int) -> np.ndarray:
    m_pcs = pc_df.loc[male_id].values[:n_pc]
    f_pcs = pc_df.loc[female_id].values[:n_pc]
    add = (m_pcs + f_pcs) / 2.0
    diff = np.abs(m_pcs - f_pcs)
    feat = np.concatenate([add, diff]).reshape(1, -1)
    return feat


@dataclass
class ModelPredictor:
    model_id: str
    model_dir: Path
    traits: List[str]
    n_pc: int
    pc_df: pd.DataFrame
    rf_models: Dict[str, object]

    @classmethod
    def load(cls, model_id: str) -> "ModelPredictor":
        model_dir = _model_directory(model_id)
        meta = _load_meta(model_dir)
        if meta is None:
            raise ValueError("모델 메타데이터를 찾을 수 없습니다.")

        traits = meta.get("traits", [])
        n_pc = int(meta.get("n_pc", 0))

        pc_df = pd.read_csv(model_dir / "line_pcs.csv").set_index("line_id")

        rf_models: Dict[str, object] = {}
        for trait in traits:
            model_path = model_dir / f"rf_{trait}.joblib"
            if not model_path.exists():
                raise ValueError(f"{trait} 예측 모델이 존재하지 않습니다.")
            rf_models[trait] = joblib.load(model_path)

        return cls(
            model_id=model_id,
            model_dir=model_dir,
            traits=traits,
            n_pc=n_pc,
            pc_df=pc_df,
            rf_models=rf_models,
        )

    def predict(self, male_id: str, female_id: str) -> Dict[str, float]:
        if male_id not in self.pc_df.index or female_id not in self.pc_df.index:
            raise ValueError("모델에서 지원하지 않는 계통 ID입니다.")

        feat = _make_cross_feature_from_pc(self.pc_df, male_id, female_id, self.n_pc)
        return {trait: float(model.predict(feat)[0]) for trait, model in self.rf_models.items()}


_PREDICTORS: Dict[str, ModelPredictor] = {}


def _get_predictor(model_id: str) -> ModelPredictor:
    if model_id not in _PREDICTORS:
        _PREDICTORS[model_id] = ModelPredictor.load(model_id)
    return _PREDICTORS[model_id]


def predict(model_id: str, male_id: str, female_id: str) -> Dict[str, float]:
    """Run the trained model to predict trait values for the given combination."""

    predictor = _get_predictor(model_id)
    return predictor.predict(male_id, female_id)
