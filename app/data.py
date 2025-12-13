"""In-memory data backing the BRAI API prototype."""

from __future__ import annotations

from typing import Dict, List, Optional

# Dataset metadata keyed by dataset ID.
DATASETS: Dict[str, dict] = {
    "TC1": {
        "id": "TC1",
        "name": "TC1",
        "strains": [
            "TC1_001",
            "TC1_002",
            "TC1_003",
            "TC1_022",
        ],
        "phenotype": [
            "weight",
            "length",
            "width",
            "ratio",
            "brix",
            "firmness",
            "skinThickness",
            "shape",
        ],
        "snpInfo": {
            "chr": ["1", "1", "1", "1", "1"],
            "bp": ["20288", "62862", "65279", "65409", "65869"],
            "numberOfSNP": 5,
        },
    },
    "AI": {
        "id": "AI",
        "name": "AI",
        "strains": [
            "AI_101",
            "AI_142",
            "AI_213",
        ],
        "phenotype": [
            "weight",
            "length",
            "width",
            "brix",
            "firmness",
        ],
        "snpInfo": {
            "chr": ["2", "2", "3"],
            "bp": ["85201", "103992", "209331"],
            "numberOfSNP": 3,
        },
    },
}

# Strain metadata keyed by strain ID.
STRAINS: Dict[str, dict] = {
    "TC1_001": {
        "id": "TC1_001",
        "name": "TC1_001",
        "type": "both",
        "phenotype": {
            "weight": 45.12,
            "length": 43.87,
            "width": 37.98,
            "ratio": 1.15,
            "brix": 5.11,
            "firmness": 0.49,
            "skinThickness": 6.73,
            "shape": "round",
        },
    },
    "TC1_022": {
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
            "shape": "round",
        },
    },
    "AI_101": {
        "id": "AI_101",
        "name": "AI_101",
        "type": "fruit",
        "phenotype": {
            "weight": 39.02,
            "length": 40.12,
            "width": 34.87,
            "brix": 6.15,
            "firmness": 0.62,
        },
    },
    "AI_142": {
        "id": "AI_142",
        "name": "AI_142",
        "type": "fruit",
        "phenotype": {
            "weight": 42.88,
            "length": 42.05,
            "width": 36.02,
            "brix": 6.02,
            "firmness": 0.66,
        },
    },
    "AI_213": {
        "id": "AI_213",
        "name": "AI_213",
        "type": "fruit",
        "phenotype": {
            "weight": 41.33,
            "length": 41.77,
            "width": 35.75,
            "brix": 6.44,
            "firmness": 0.59,
        },
    },
}


def list_datasets() -> List[str]:
    """Return sorted dataset identifiers."""

    return sorted(DATASETS.keys())


def get_dataset(dataset_id: str) -> Optional[dict]:
    """Fetch a single dataset by its identifier."""

    return DATASETS.get(dataset_id)


def get_strain(strain_id: str) -> Optional[dict]:
    """Fetch a single strain by its identifier."""

    return STRAINS.get(strain_id)
