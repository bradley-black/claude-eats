"""claude-eats: a little orange terminal mascot that eats your messages.

Installed as both `eat` and `claude-eats` — same program either way.

Just run `eat` — nothing before, nothing after. The mascot walks
left-to-right, Pac-Man style, mouth opening and closing as it eats a
line of text (whatever you pass as arguments, e.g. `eat "hello"`, or a
default line if you give it nothing). Once it's done, the program hands
control back to a brand new login shell, so the terminal looks exactly
as if it had just been opened — no trace it ran.
"""

import getpass
import os
import random
import shutil
import sys
import time

from .sprite import SPRITE_LINES, SPRITE_MOUTH_OPEN_LINES, SPRITE_WIDTH

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
CLEAR = "\x1b[2J\x1b[H"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"

SOUNDS = ["*nom*", "*crunch*", "*chomp*", "*mnawp*", "*munch*"]


def _term_size():
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.columns, size.lines


def render(pending, mascot_lines=SPRITE_LINES, mascot_x=1, caption="", active_line=None):
    cols, rows = _term_size()
    out = [CLEAR]

    title = "claude-eats"
    out.append(f"{BOLD}{title}{RESET}\n\n")

    indent = " " * max(0, mascot_x)
    mascot_h = len(mascot_lines)
    mid = mascot_h // 2
    for i, ml in enumerate(mascot_lines):
        line = indent + ml
        if caption and i == mid:
            line += "  " + caption
        out.append(line + "\n")
    out.append("\n")

    if active_line is not None:
        out.append(active_line[: max(0, cols - 1)] + "\n\n")

    max_pending = max(0, rows - mascot_h - (4 if active_line is not None else 2))
    for line in pending[:max_pending]:
        out.append(line[: max(0, cols - 1)] + "\n")

    sys.stdout.write("".join(out))
    sys.stdout.flush()


def _run_across(line, pending_rest):
    """Slide the mascot left-to-right across `line`, mouth flapping open and
    shut, eating it word by word."""
    words = line.split(" ")
    display = line
    offset = 0
    x = 0.0

    for word in words:
        target = offset + len(word)
        steps = max(2, len(word) // 2)
        for s in range(1, steps + 1):
            x = offset + (target - offset) * (s / steps)
            frame = SPRITE_MOUTH_OPEN_LINES if s % 2 == 0 else SPRITE_LINES
            render(pending_rest, mascot_lines=frame, mascot_x=round(x), active_line=display)
            time.sleep(0.025)

        display = display[:offset] + " " * len(word) + display[offset + len(word):]
        offset = target + 1  # skip the space
        render(
            pending_rest,
            mascot_lines=SPRITE_MOUTH_OPEN_LINES,
            mascot_x=round(x),
            caption=random.choice(SOUNDS),
            active_line=display,
        )
        time.sleep(0.05)


def _return_to_fresh_terminal():
    """End the program and hand control to a brand-new login shell, so the
    terminal looks exactly as if it had just been opened.

    Only attempted when stdin/stdout are a real interactive terminal —
    piped/non-interactive runs (tests, the /eat skill if run from Bash)
    just fall back to a normal idle screen instead.
    """
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        render([])
        return

    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.write(CLEAR)
    sys.stdout.flush()

    try:
        os.execvp("login", ["login", "-pf", getpass.getuser()])
    except OSError:
        pass

    shell = os.environ.get("SHELL", "/bin/zsh")
    try:
        os.execvp(shell, [shell, "-l"])
    except OSError:
        render([])


def eat_animation(history):
    pending = list(history)

    for _ in range(2):
        render(pending[1:], mascot_lines=SPRITE_MOUTH_OPEN_LINES, caption=random.choice(SOUNDS), active_line=pending[0])
        time.sleep(0.09)
        render(pending[1:], mascot_lines=SPRITE_LINES, active_line=pending[0])
        time.sleep(0.06)

    while pending:
        line = pending[0]
        _run_across(line, pending[1:])
        pending.pop(0)
        render(pending, mascot_lines=SPRITE_LINES, caption="*gulp*")
        time.sleep(0.12)

    render([], mascot_lines=SPRITE_MOUTH_OPEN_LINES, caption="ahh, delicious.")
    time.sleep(0.9)
    history.clear()
    _return_to_fresh_terminal()


def main():
    args = sys.argv[1:]
    text = " ".join(args).strip() or "a tasty byte"
    history = [f"you  {text}"]
    sys.stdout.write(HIDE_CURSOR)
    try:
        eat_animation(history)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
