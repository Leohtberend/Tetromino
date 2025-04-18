"""
Shape definitions and rotation utilities for the tetromino tiler.

Loads base piece layouts and scoring variants from a JSON configuration.
Provides functions to rotate and normalize shapes, and to compute all unique orientations.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

_CONFIG_PATH: Path = Path(__file__).resolve().parent.parent/"config.json"
with open(_CONFIG_PATH, "r") as _f:
    _cfg = json.load(_f)

# ——— base pieces & scoring ———
BASE_PIECES: Dict[str, List[Tuple[int,int]]] = {
    name: [tuple(coord) for coord in coords]
    for name, coords in _cfg["base_pieces"].items()
}

SCORE_VARIANTS: List[Dict[str,int]] = _cfg["score_variants"]


def rotate90(shape: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    return [(c, -r) for r, c in shape]


def normalize(shape: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    min_r = min(r for r, c in shape)
    min_c = min(c for r, c in shape)
    return sorted((r - min_r, c - min_c) for r, c in shape)


def all_rotations(base: List[Tuple[int,int]]) -> List[List[Tuple[int,int]]]:
    seen = set()
    rots = []
    curr = base
    for _ in range(4):
        norm = tuple(normalize(curr))
        if norm not in seen:
            seen.add(norm)
            rots.append(list(norm))
        curr = rotate90(curr)
    return rots


# ——— precompute all piece rotations ———
PIECE_ROTS: Dict[str, List[List[Tuple[int,int]]]] = {
    name: all_rotations(coords)
    for name, coords in BASE_PIECES.items()
}
