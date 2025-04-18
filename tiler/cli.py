import argparse
from pathlib import Path
from tiler.placer import enumerate_tilings
from tiler.drawer import draw_solution, debug_shapes
from tiler.shapes import SCORE_VARIANTS

PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT               = PACKAGE_ROOT.parent / "input.txt"
DEFAULT_OUTPUT              = PACKAGE_ROOT.parent / "outputs"
DEFAULT_DEBUG_PATH          = PACKAGE_ROOT.parent / "all_shapes_debug.png"
DEFAULT_DEBUG               = False
DEFAULT_GET_ALL_SOLUTIONS   = False


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
    return parser.parse_args()


def main():
    args = parse_args()
    # process grids
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with args.input_file.open() as f:
        for idx, line in enumerate(f):
            vals = list(map(int, line.strip().split(",")))
            size = len(vals)
            N = int(size**0.5)
            if N * N != size:
                raise ValueError(f"Grid #{idx}: {size} cells is not a perfect square")
            if sum(vals) == 0:
                print(f"Grid #{idx} ({N}×{N}): empty, skipping")
                continue
            sols = enumerate_tilings(vals, N)
            print(f"Grid #{idx} ({N}×{N}): {len(sols)} solution(s)")
            if args.get_all_solutions:
                for sol_idx, sol in enumerate(sols, start=1):
                    print(f"  Solution {sol_idx}")
                    outp = args.output_dir / f"grid_{idx}_sol{sol_idx}.png"
                    draw_solution(vals, N, sol, outp, args.cell_size)
            else:
                for vid, score_map in enumerate(SCORE_VARIANTS, 1):
                    scored = [(sum(score_map[p['piece']] for p in sol), sol) for sol in sols]
                    best_score, best_sol = max(scored, key=lambda x: x[0])
                    print(f" Variant {vid}: score={best_score}")
                    outp = args.output_dir / f"grid_{idx}_variant{vid}.png"
                    draw_solution(vals, N, best_sol, outp, args.cell_size)
    if args.debug:
        debug_shapes(args.debug_path)
        