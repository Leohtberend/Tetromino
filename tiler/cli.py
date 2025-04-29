import argparse
from pathlib import Path

from tiler.placer import enumerate_tilings
from tiler.drawer import draw_solution, debug_shapes, draw_raw_grid
from tiler.shapes import SCORE_VARIANTS, BASE_PIECES
from tiler.utils import (
    save_solutions,
    decode_and_draw
)

PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = PACKAGE_ROOT.parent / "input.txt"
DEFAULT_OUTPUT = PACKAGE_ROOT.parent / "outputs"
DEFAULT_DEBUG_PATH = PACKAGE_ROOT.parent / "outputs" / "all_shapes_debug.png"
DEFAULT_DEBUG = False
DEFAULT_GET_ALL_SOLUTIONS = False


def parse_args():
    parser = argparse.ArgumentParser(
        description="Discover & draw tilings of tetromino shapes on any N×N grid."
    )
    parser.add_argument(
        "-i", "--input-file",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Path to input file (default: {DEFAULT_INPUT})"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Directory for output PNGs (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--cell-size",
        type=int,
        default=50,
        help="Pixels per grid cell"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=DEFAULT_DEBUG,
        help="Generate debug image of all tetromino shapes"
    )
    parser.add_argument(
        "--debug-path",
        type=Path,
        default=DEFAULT_DEBUG_PATH,
        help=f"Path for debug shapes image (default: {DEFAULT_DEBUG_PATH})"
    )
    parser.add_argument(
        "--get-all-solutions",
        action="store_true",
        default=DEFAULT_GET_ALL_SOLUTIONS,
        help="Get all solutions for each grid (default: False)"
    )
    parser.add_argument(
        "--raw-render",
        action="store_true",
        help="skip tilings; render each 0/1 grid line as a standalone image"
    )
    parser.add_argument(
        "--save-solutions",
        action="store_true",
        default=False,
        help="Save encoded solutions of displayed tilings to a file"
    )
    parser.add_argument(
        "--encoding-format",
        choices=["csv", "txt", "json"],
        default="json",
        help="Format for saved encodings (csv, txt, or json)"
    )
    parser.add_argument(
        "--decode-solutions",
        action="store_true",
        default=False,
        help="Decode previously saved solutions and draw them without re-computing"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    with args.input_file.open() as f:
        raw_lines = [l.strip() for l in f if l.strip()]
    lines = []
    for l in raw_lines:
        parts = l.split(',')
        if all(part.isdigit() for part in parts):
            lines.append(l)
        else:
            print(f"Skipping non-grid line: {l}")
    grids = [list(map(int, l.split(','))) for l in lines]

    if args.decode_solutions:
        decode_and_draw(grids, args.output_dir, args.encoding_format, args.cell_size)
        return

    if args.save_solutions:
        save_solutions(grids, args.output_dir, args.encoding_format)
        return

    if args.raw_render:
        for idx, vals in enumerate(grids):
            N = int(len(vals) ** 0.5)
            if N * N != len(vals):
                print(f"Grid #{idx}: {len(vals)} cells isn’t square, skipping")
                continue
            outp = args.output_dir / f"grid_{idx}.png"
            draw_raw_grid(vals, N, outp, args.cell_size)
        if args.debug:
            debug_shapes(args.debug_path)
        return

    for idx, vals in enumerate(grids):
        N = int(len(vals) ** 0.5)
        if N * N != len(vals):
            raise ValueError(f"Grid #{idx}: {len(vals)} cells is not a perfect square")
        if sum(vals) == 0:
            print(f"Grid #{idx} ({N}×{N}): empty, skipping")
            continue
        sols = enumerate_tilings(vals, N)
        print(f"Grid #{idx} ({N}×{N}): {len(sols)} solution(s)")
        if args.get_all_solutions:
            for sol_idx, sol in enumerate(sols, start=1):
                print(f"  Solution {sol_idx}")
                draw_solution(vals, N, sol, args.output_dir / f"grid_{idx}_sol{sol_idx}.png", args.cell_size)
        else:
            for vid, score_map in enumerate(SCORE_VARIANTS, 1):
                scored = [(sum(score_map[p['piece']] for p in sol), sol) for sol in sols]
                best_score, best_sol = max(scored, key=lambda x: x[0])
                print(f" Variant {vid}: score={best_score}")
                draw_solution(vals, N, best_sol, args.output_dir / f"grid_{idx}_variant{vid}.png", args.cell_size)
    if args.debug:
        debug_shapes(args.debug_path)


if __name__ == '__main__':
    main()
