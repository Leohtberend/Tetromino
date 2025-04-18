import colorsys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict


def draw_solution(vals: List[int], N: int, solution: List[Dict], out_path: Path, cell_size: int = 50) -> None:
    """Draws one tiling, coloring each piece in a unique hue."""
    m = len(solution)
    palette = [
        tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i/m, 0.6, 0.9))
        for i in range(m)
    ]
    img = Image.new("RGB", (N*cell_size, N*cell_size), "white")
    draw = ImageDraw.Draw(img)

    # shade unavailable cells
    for idx, v in enumerate(vals):
        if not v:
            r, c = divmod(idx, N)
            draw.rectangle(
                [c*cell_size, r*cell_size, (c+1)*cell_size, (r+1)*cell_size],
                fill=(180,180,180)
            )
    # paint each piece
    for k, p in enumerate(solution):
        for idx in p["cells"]:
            r, c = divmod(idx, N)
            draw.rectangle(
                [c*cell_size+1, r*cell_size+1,
                 (c+1)*cell_size-1, (r+1)*cell_size-1],
                fill=palette[k]
            )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(f"→ saved: {out_path}")


def debug_shapes(out_path: Path) -> None:
    """Draws one tile of each base tetromino shape for reference."""
    from .shapes import BASE_PIECES

    COLS, CW, CH, BS = 4, 120, 120, 20
    rows = (len(BASE_PIECES) + COLS - 1) // COLS
    img = Image.new("RGB", (COLS*CW, rows*CH), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for i, (name, coords) in enumerate(BASE_PIECES.items()):
        col, row = i % COLS, i // COLS
        ox, oy = col*CW, row*CH
        maxr = max(x for x,y in coords) + 1
        maxc = max(y for x,y in coords) + 1
        sx = ox + (CW - maxc*BS)//2
        sy = oy + (CH - maxr*BS - 20)//2
        for x, y in coords:
            tl = (sx + y*BS, sy + x*BS)
            br = (tl[0] + BS, tl[1] + BS)
            draw.rectangle([tl, br], fill="lightgray", outline="black")
        tb = draw.textbbox((0,0), name, font=font)
        tw, th = tb[2]-tb[0], tb[3]-tb[1]
        draw.text((ox + (CW-tw)//2, oy + CH - th - 5), name, fill="black", font=font)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(f"Saved debug shapes to: {out_path}")