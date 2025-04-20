# Tetromino Tiler

Discover & draw tilings of tetromino shapes on any N×N grid.

## Setup

1. **Clone the repository**  

2. **Install Python**  

3. **Create & activate a virtual environment**  
   ```
   python -m venv venv
   ```

4. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

## Input & Output

- **Input file**: `input.txt` at project root (or pass `-i` to point elsewhere).  
  - Each line is a comma-separated list of `0`/`1` values.  
  - Total count per line must be a perfect square (e.g. 16, 25, 36…).

**Example** (`input.txt`):

```
0,1,1,1,1,1,1,1,0,0,1,1,0,1,1,1
1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0
1,1,0,0,0,1,1,1,0,1,1,1,1,1,1,1
1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,0
```

- **Output folder**: `outputs/` (override with `-o`). 
For each line you’ll get PNG(s)
```
outputs/grid_<line#>_variant1.png
```

## CLI Usage

```
python main.py [options]
```

**Options**  
- `-i, --input-file`    Path to input (default: `input.txt`)  
- `-o, --output-dir`    Directory for PNGs (default: `outputs/`)  
- `--cell-size`         Pixels per grid cell (default: 50)  
- `--debug`             Generate `all_shapes_debug.png` for shape reference  
- `--debug-path`        Where to save debug image (default: `all_shapes_debug.png`)
- `--get-all-solutions` Generates all possible solutions

## Configuration

All piece layouts and scoring weights live in **config.json** at the project root which can be modified to add new shapes
