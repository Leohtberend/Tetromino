from typing import List, Tuple, Dict
from .shapes import PIECE_ROTS


def compute_placements(vals: List[int], N: int) -> Tuple[List[Dict], Dict[int,List[Dict]], List[int]]:
    """
    Given a flat list of 0/1 `vals` of length N*N, returns:
      - all valid piece placements,
      - a mapping cell_index → placements covering that cell,
      - list of available cell indices.
    """
    avail = [i for i, v in enumerate(vals) if v]
    by_cell: Dict[int, List[Dict]] = {i: [] for i in avail}
    placements: List[Dict] = []

    for piece, rots in PIECE_ROTS.items():
        for shape in rots:
            max_r = max(x for x, y in shape)
            max_c = max(y for x, y in shape)
            for i_off in range(N - max_r):
                for j_off in range(N - max_c):
                    cells = [(i_off + x, j_off + y) for x, y in shape]
                    idxs = [r * N + c for r, c in cells]
                    if all(vals[i] for i in idxs):
                        placement = {"piece": piece, "cells": set(idxs)}
                        placements.append(placement)
                        for i in idxs:
                            by_cell[i].append(placement)
    return placements, by_cell, avail


def enumerate_tilings(vals: List[int], N: int) -> List[List[Dict]]:
    """Return all exact tilings of the available cells by tetromino pieces."""
    placements, by_cell, avail = compute_placements(vals, N)
    if len(avail) % 4:
        raise ValueError("Available cells not divisible by 4")

    solutions: List[List[Dict]] = []
    def backtrack(covered: set, sol: List[Dict]):
        if len(covered) == len(avail):
            solutions.append(sol.copy())
            return
        # choose the uncovered cell with fewest placement options
        cell = min(
            (i for i in avail if i not in covered),
            key=lambda i: sum(1 for p in by_cell[i] if p["cells"].isdisjoint(covered))
        )
        for p in by_cell[cell]:
            if p["cells"].isdisjoint(covered):
                covered |= p["cells"]
                sol.append(p)
                backtrack(covered, sol)
                sol.pop()
                covered -= p["cells"]

    backtrack(set(), [])
    return solutions
    