#!/usr/bin/env python3
"""Render the two GitHub profile cards with Python's standard library."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1120, 620
COLS = 76
TEXT_X = 424
THEMES = {
    "dark": {"bg": "#161b22", "fg": "#c9d1d9", "key": "#ffa657", "value": "#a5d6ff", "muted": "#616e7f", "green": "#3fb950"},
    "light": {"bg": "#f6f8fa", "fg": "#24292f", "key": "#953800", "value": "#0a3069", "muted": "#a6b3c3", "green": "#1a7f37"},
}


def span(value, cls=None):
    attr = f' class="{cls}"' if cls else ""
    return f"<tspan{attr}>{html.escape(str(value))}</tspan>"


def field(label, value):
    value = str(value)
    dots = COLS - len(label) - len(value) - 6
    if dots < 2:
        raise ValueError(f"Value too long for {label}: {value}")
    return span(". ", "muted") + span(label, "key") + span(":") + span(" " + "." * dots + " ", "muted") + span(value, "value")


def section(title):
    return span(title + " ") + span("─" * (COLS - len(title) - 1), "muted")


def build(theme, profile, stats, portrait):
    c = THEMES[theme]
    rows = [
        section(profile["header"]),
        field("Name", profile["name"]),
        field("Host", profile["host"]),
        field("Kernel", profile["role"]),
        field("Location", profile["location"]),
        field("Focus", profile["focus"]),
        span(". ", "muted"),
        field("Languages.Code", profile["programming"]),
        field("Languages.Human", profile["languages"]),
        field("Stack.Data", profile["data_stack"]),
        field("Stack.AI", profile["ai_stack"]),
        field("Stack.Cloud", profile["cloud_stack"]),
        field("Stack.Web", profile["web_stack"]),
        span(". ", "muted"),
        field("Hobbies", profile["hobbies"]),
        span(". ", "muted"),
        section("- Contact"),
        field("Email", profile["email"]),
        field("LinkedIn", profile["linkedin"]),
        field("Portfolio", profile["portfolio"]),
        span(". ", "muted"),
        section("- GitHub Stats"),
        field("Repos.Public", f'{stats["public_repos"]}  |  Stars: {stats["stars"]}'),
        field("Followers", f'{stats["followers"]}  |  Since: {stats["joined"]}'),
        field("Updated.UTC", stats["updated"]),
        span(". ", "muted") + span(f'github.com/{profile["username"]}', "green"),
    ]
    text = "\n".join(f'<text x="{TEXT_X}" y="{36 + i * 22}">{row}</text>' for i, row in enumerate(rows))
    portrait_start = (HEIGHT - (len(portrait) - 1) * 13) / 2 + 4
    ascii_art = "\n".join(f'<tspan x="24" y="{portrait_start + i * 13:g}">{html.escape(row)}</tspan>' for i, row in enumerate(portrait))
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
<title id="title">Alexandre Bredillot — GitHub Profile</title>
<desc id="desc">ASCII portrait and terminal-style profile of Alexandre Bredillot, Data Analytics Engineer in Paris. Public GitHub statistics updated {stats['updated']}.</desc>
<style>
text {{ font-family: Menlo, Consolas, "DejaVu Sans Mono", monospace; font-size: 14px; fill: {c['fg']}; white-space: pre; }}
.portrait {{ font-size: 11.4px; }}
.key {{ fill: {c['key']}; }}
.value {{ fill: {c['value']}; }}
.muted {{ fill: {c['muted']}; }}
.green {{ fill: {c['green']}; }}
</style>
<rect width="{WIDTH}" height="{HEIGHT}" rx="15" fill="{c['bg']}"/>
<g xml:space="preserve">
<text class="portrait">{ascii_art}</text>
{text}
</g>
</svg>
'''


def main():
    profile = json.loads((ROOT / "data/profile.json").read_text())
    stats = json.loads((ROOT / "data/stats.json").read_text())
    portrait = (ROOT / "data/portrait.txt").read_text().splitlines()
    if len(portrait) > 43 or any(len(row) > 54 for row in portrait):
        raise ValueError("Portrait must fit in 54 columns and 43 rows")
    for theme in THEMES:
        output = ROOT / f"{theme}_mode.svg"
        output.write_text(build(theme, profile, stats, portrait), encoding="utf-8")
        print(f"Rendered {output.name}")


if __name__ == "__main__":
    main()
