# claude-eats

A little orange pixel-art terminal mascot. Run `eat` and it walks across
your screen, mouth opening and closing, devouring a line of text — then
hands control back to a brand new login shell, so your terminal looks
exactly as if it had just been opened.

```
eat
```

That's it — nothing before, nothing after. Pass your own text instead of
the default line if you want:

```
eat "goodbye, cruel message"
```

## Run it without installing

```
uvx --from /path/to/claude-eats eat
```

Once pushed to a git repo, anyone can run it with zero setup:

```
uvx --from git+https://github.com/<you>/claude-eats eat
```

## Install it permanently

```
uv tool install /path/to/claude-eats
eat
```

or, once hosted on a git repo:

```
uv tool install git+https://github.com/<you>/claude-eats
```

Also installable with plain `pip install .` or `pipx install .` — no uv
required. Both give you the `eat` command (and `claude-eats` as an alias).

## Dev

```
uv run eat
```

No runtime dependencies — pure standard library. Requires a truecolor
terminal (Terminal.app, iTerm2, most modern terminals) to render the
mascot's colors correctly.
