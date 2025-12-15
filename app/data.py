"""In-memory data backing the BRAI API prototype."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from uuid import uuid4

DATASET_ROOT = Path(__file__).resolve().parent / "dataset"

# Prediction records are stored in-memory for the prototype.
PREDICTIONS: List[dict] = []


def _dataset_directory(dataset_id: str) -> Path:
    return DATASET_ROOT / dataset_id


def _load_strain_metadata(dataset_dir: Path) -> Tuple[List[str], dict]:
    strains_csv = dataset_dir / "strains" / "strains.csv"
    if not strains_csv.exists():
        return [], {"chr": [], "bp": [], "numberOfSNP": 0}

    with strains_csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
        strain_ids = header[3:] if len(header) > 3 else []

        chr_values: List[str] = []
        bp_values: List[str] = []
        for row in reader:
            if len(row) < 3:
                continue
            chr_values.append(row[1])
            bp_values.append(row[2])

    return strain_ids, {"chr": chr_values, "bp": bp_values, "numberOfSNP": len(bp_values)}


def _load_phenotype_columns(dataset_dir: Path) -> List[str]:
    phenotype_csv = dataset_dir / "phenotype" / "phenotype.csv"
    if not phenotype_csv.exists():
        return []

    # Try multiple encodings (Excel/Windows KR data often comes as cp949/euc-kr)
    for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            with phenotype_csv.open(newline="", encoding=enc) as handle:
                reader = csv.reader(handle)
                header = next(reader, [])
            return header[1:] if header else []
        except UnicodeDecodeError:
            continue

    raise ValueError(
        f"Cannot decode phenotype.csv with supported encodings: {phenotype_csv}"
    )


def _load_phenotype_values(dataset_dir: Path, strain_id: str) -> Optional[dict]:
    """Load phenotype values for a strain from the dataset CSV."""

    phenotype_csv = dataset_dir / "phenotype" / "phenotype.csv"
    if not phenotype_csv.exists():
        return None

    encodings = ("utf-8-sig", "utf-8", "cp949", "euc-kr")
    last_error: Optional[Exception] = None
    for enc in encodings:
        try:
            with phenotype_csv.open(newline="", encoding=enc) as handle:
                reader = csv.reader(handle)
                header = next(reader, [])
                for row in reader:
                    if not row:
                        continue
                    if row[0] != strain_id:
                        continue

                    phenotype: Dict[str, object] = {}
                    for key, value in zip(header[1:], row[1:]):
                        if value == "":
                            phenotype[key] = None
                            continue
                        try:
                            phenotype[key] = float(value)
                        except ValueError:
                            phenotype[key] = value
                    return phenotype
                return None
        except UnicodeDecodeError as exc:
            last_error = exc
            continue

    if last_error is not None:
        raise ValueError(
            f"Cannot decode phenotype.csv with supported encodings: {phenotype_csv}"
        )

    return None


def _load_strain_from_dataset(dataset_dir: Path, strain_id: str) -> Optional[dict]:
    """Load strain metadata from dataset files."""

    strain_ids, _ = _load_strain_metadata(dataset_dir)
    if strain_id not in strain_ids:
        return None

    phenotype = _load_phenotype_values(dataset_dir, strain_id)
    strain: Dict[str, object] = {"id": strain_id, "name": strain_id}
    if phenotype:
        strain["phenotype"] = phenotype
    return strain


def list_datasets() -> List[str]:
    """Return sorted dataset identifiers from the dataset directory."""

    if not DATASET_ROOT.exists():
        return []

    return sorted(item.name for item in DATASET_ROOT.iterdir() if item.is_dir())


def get_dataset(dataset_id: str) -> Optional[dict]:
    """Fetch a single dataset by reading the corresponding dataset folder."""

    dataset_dir = _dataset_directory(dataset_id)
    if not dataset_dir.is_dir():
        return None

    strains, snp_info = _load_strain_metadata(dataset_dir)
    phenotype = _load_phenotype_columns(dataset_dir)

    return {
        "id": dataset_id,
        "name": dataset_id,
        "strains": strains,
        "phenotype": phenotype,
        "snpInfo": snp_info,
    }


def get_strain(strain_id: str) -> Optional[dict]:
    """Fetch a single strain by its identifier."""

    for dataset_id in list_datasets():
        dataset_dir = _dataset_directory(dataset_id)
        strain = _load_strain_from_dataset(dataset_dir, strain_id)
        if strain:
            return strain

    return None


def _iso_now() -> str:
    """Return a millisecond-precision UTC timestamp in ISO 8601 format."""

    return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


def _make_prediction_id() -> str:
    """Create a unique prediction identifier."""

    return f"PRED_{int(datetime.utcnow().timestamp() * 1000)}_{uuid4().hex[:8]}"


def _compute_predicted_phenotype(dataset: dict, male: dict, female: dict) -> dict:
    """Generate a deterministic predicted phenotype payload."""

    result: Dict[str, dict] = {}
    for trait in dataset.get("phenotype", []):
        male_val = male.get("phenotype", {}).get(trait)
        female_val = female.get("phenotype", {}).get(trait)

        numeric_values = [
            value for value in (male_val, female_val) if isinstance(value, (int, float))
        ]
        if numeric_values:
            avg_value = round(sum(numeric_values) / len(numeric_values), 2)
            result[trait] = {"value": avg_value, "confidence": 0.9, "grade": 3}
            continue

        text_value = male_val if male_val is not None else female_val
        if text_value is not None:
            result[trait] = {"value": text_value, "confidence": 0.9}

    return result


def create_prediction(dataset_id: str, model_id: str, male_id: str, female_id: str) -> dict:
    """Create and store a new prediction record."""

    dataset = get_dataset(dataset_id)
    if dataset is None:
        raise ValueError(f"Dataset '{dataset_id}' not found")
    dataset_dir = _dataset_directory(dataset_id)
    male = _load_strain_from_dataset(dataset_dir, male_id)
    female = _load_strain_from_dataset(dataset_dir, female_id)

    if male is None or female is None:
        raise ValueError("Strain ID가 존재하지 않습니다.")

    prediction_body = {
        "id": _make_prediction_id(),
        "predictedPhenotype": _compute_predicted_phenotype(dataset, male, female),
        "createdAt": _iso_now(),
    }

    record = {
        "dataset": dataset_id,
        "model": model_id,
        "maleStrainId": male_id,
        "femaleStrainId": female_id,
        **prediction_body,
    }
    PREDICTIONS.append(record)
    return prediction_body


def list_predictions(page: int, limit: int, sort: str) -> dict:
    """Return paginated predictions sorted by creation date."""

    reverse = sort.lower() != "asc"
    ordered = sorted(PREDICTIONS, key=lambda item: item["createdAt"], reverse=reverse)

    start = (page - 1) * limit
    end = start + limit
    page_items = ordered[start:end]

    return {
        "items": page_items,
        "total": len(ordered),
        "page": page,
        "limit": limit,
        "hasMore": end < len(ordered),
    }


def list_combinations() -> List[str]:
    """Return every unique (female-male) strain combination from stored predictions."""

    combinations = {
        f"{record['femaleStrainId']}-{record['maleStrainId']}" for record in PREDICTIONS
    }
    return sorted(combinations)


def get_prediction_by_combination(male_id: str, female_id: str) -> Optional[dict]:
    """Find a prediction by its male/female strain identifiers."""

    for record in PREDICTIONS:
        if (
            record["maleStrainId"] == male_id
            and record["femaleStrainId"] == female_id
        ):
            return record
    return None
