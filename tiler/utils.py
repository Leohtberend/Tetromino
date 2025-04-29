import json
from pathlib import Path
from collections import defaultdict

from tiler.placer import enumerate_tilings
from tiler.shapes import BASE_PIECES
from tiler.drawer import draw_solution


def encode_solution(vals: list[int], N: int, solution: list[dict]) -> list[list[str]] | None:
    """
    Encodes a tiling solution into a 2D list of X.Y tags (as strings).
    Returns None for empty solutions.
    """
    if not solution:
        return None
    shape_map = {name: i + 1 for i, name in enumerate(BASE_PIECES.keys())}
    grid = [["0"] * N for _ in range(N)]
    counts: dict[int, int] = {code: 0 for code in shape_map.values()}
    for placement in solution:
        code = shape_map[placement['piece']]
        counts[code] += 1
        tag = f"{code}.{counts[code]}"
        for idx in placement['cells']:
            r, c = divmod(idx, N)
            grid[r][c] = tag
    return grid


def decode_solution(grid_enc: list[list[str]]) -> list[dict]:
    """
    Decodes a grid of X.Y tags back into placement dictionaries.
    """
    N = len(grid_enc)
    inv_map = {i + 1: name for i, name in enumerate(BASE_PIECES.keys())}
    groups: dict[tuple[int, int], list[int]] = defaultdict(list)
    for r, row in enumerate(grid_enc):
        for c, tag in enumerate(row):
            if tag == "0":
                continue
            parts = tag.split('.')
            if len(parts) != 2 or not all(p.isdigit() for p in parts):
                raise ValueError(f"Invalid tag '{tag}' at ({r},{c})")
            code, inst = map(int, parts)
            groups[(code, inst)].append(r * N + c)
    placements: list[dict] = []
    for (code, inst), cells in groups.items():
        if len(cells) != 4:
            raise ValueError(f"Group {code}.{inst} has {len(cells)} cells, expected 4")
        piece = inv_map.get(code)
        placements.append({'piece': piece, 'cells': set(cells)})
    return placements


def save_solutions(grids: list[list[int]], output_dir: Path, encoding_format: str) -> None:
    """
    Enumerate and save all tiling encodings for each grid.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"solutions.{encoding_format}"
    enc_list: list[dict] = []
    for gid, vals in enumerate(grids):
        N = int(len(vals) ** 0.5)
        sols = enumerate_tilings(vals, N)
        for sid, sol in enumerate(sols, start=1):
            grid_enc = encode_solution(vals, N, sol)
            if grid_enc is None:
                continue
            codes = {int(tag.split('.')[0]) for row in grid_enc for tag in row if tag != '0'}
            shapes_used = sorted(codes, reverse=True)
            enc_list.append({
                'grid': gid,
                'solution': sid,
                'encoding': grid_enc,
                'shapes_used': shapes_used
            })
    with path.open('w') as f:
        json.dump(enc_list, f)
    print(f"→ saved encodings to: {path}")


def decode_and_draw(grids: list[list[int]], output_dir: Path, encoding_format: str, cell_size: int) -> None:
    """
    Load saved encodings and render each decoded tiling.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"solutions.{encoding_format}"
    data = json.load(path.open())
    for entry in data:
        gid, sid, grid_enc = entry['grid'], entry['solution'], entry['encoding']
        N = len(grid_enc)
        vals = grids[gid]
        placements = decode_solution(grid_enc)
        outp = output_dir / f"grid_{gid}_sol{sid}.png"
        draw_solution(vals, N, placements, outp, cell_size)
        print(f"→ drew decoded grid {gid} sol {sid}")
