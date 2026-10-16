"""Pixel-grid sprite for the claude-eats mascot.

The grid is authored as bands of rows/columns (not hand-typed ASCII art),
then rendered with Unicode half-block characters ('▀'/'▄'/'█') in 24-bit
true color, giving two vertical pixels per terminal row. This is real
pixel art, not character-art.
"""

WIDTH = 16

BODY_COLOR = (217, 119, 87)   # Claude clay/orange
EYE_COLOR = (35, 24, 20)      # near-black, warm tone to match flat art

# row -> (start_col, end_col_exclusive) for the body silhouette.
# A flat rectangular body with just the top two corners clipped, square
# eyes near the top, and four distinct leg stubs along the bottom edge
# (matching the reference sprite: blocky body, slit-separated legs).
_BODY_BANDS = {
    0: (1, 15),   # top row, corners clipped
    1: (0, 16),
    2: (0, 16),
    3: (0, 16),
    4: (0, 16),
}

_LEG_ROWS = (5, 6)
# symmetric leg bands with gaps at columns 3, 7-8, 12
_LEG_BANDS = [(0, 3), (4, 7), (9, 12), (13, 16)]

_EYE_PIXELS = [
    (1, 3), (1, 4), (2, 3), (2, 4),
    (1, 11), (1, 12), (2, 11), (2, 12),
]

_HEIGHT = 7  # rows 0..6


def _build_base_grid():
    grid = [["." for _ in range(WIDTH)] for _ in range(_HEIGHT)]

    for row, (start, end) in _BODY_BANDS.items():
        for col in range(start, end):
            grid[row][col] = "#"

    for row in _LEG_ROWS:
        for start, end in _LEG_BANDS:
            for col in range(start, end):
                grid[row][col] = "#"

    for row, col in _EYE_PIXELS:
        grid[row][col] = "E"

    return ["".join(r) for r in grid]


BASE_GRID = _build_base_grid()

# Mouth: a notch carved into the leading (right) edge — the direction of
# travel — that opens and closes. Same height as BASE_GRID so toggling
# between them while walking doesn't make the sprite jitter vertically.
_MOUTH_ROWS = (3, 4)
_MOUTH_COLS = range(13, 16)


def _carve_mouth(grid_rows):
    grid = [list(r) for r in grid_rows]
    for row in _MOUTH_ROWS:
        for col in _MOUTH_COLS:
            grid[row][col] = "."
    return ["".join(r) for r in grid]


MOUTH_OPEN_GRID = _carve_mouth(BASE_GRID)

_COLORS = {"#": BODY_COLOR, "E": EYE_COLOR}


def _half_block_lines(grid):
    height = len(grid)
    width = len(grid[0]) if grid else 0
    lines = []
    for ry in range(0, height, 2):
        top = grid[ry]
        bottom = grid[ry + 1] if ry + 1 < height else "." * width
        parts = []
        for cx in range(width):
            tch = top[cx]
            bch = bottom[cx] if cx < len(bottom) else "."
            tcol = _COLORS.get(tch)
            bcol = _COLORS.get(bch)
            if tcol is None and bcol is None:
                parts.append(" ")
            elif tcol is not None and bcol is not None:
                if tcol == bcol:
                    parts.append(f"\x1b[38;2;{tcol[0]};{tcol[1]};{tcol[2]}m█\x1b[0m")
                else:
                    parts.append(
                        f"\x1b[38;2;{tcol[0]};{tcol[1]};{tcol[2]}m"
                        f"\x1b[48;2;{bcol[0]};{bcol[1]};{bcol[2]}m▀\x1b[0m"
                    )
            elif tcol is not None:
                parts.append(f"\x1b[38;2;{tcol[0]};{tcol[1]};{tcol[2]}m▀\x1b[0m")
            else:
                parts.append(f"\x1b[38;2;{bcol[0]};{bcol[1]};{bcol[2]}m▄\x1b[0m")
        lines.append("".join(parts))
    return lines


SPRITE_LINES = _half_block_lines(BASE_GRID)
SPRITE_MOUTH_OPEN_LINES = _half_block_lines(MOUTH_OPEN_GRID)
SPRITE_WIDTH = WIDTH
