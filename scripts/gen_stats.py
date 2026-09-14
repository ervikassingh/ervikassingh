#!/usr/bin/env python3
"""Generate a GitHub stats SVG from the public API. No third-party widgets."""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "ervikassingh")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("OUT", "assets/stats.svg")

BG = "#0D1117"
PANEL = "#161B22"
STROKE = "#30363D"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
ACCENT = "#E0234E"
CYAN = "#58A6FF"
GOLD = "#D29922"
GREEN = "#3FB950"
PURPLE = "#BC8CFF"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
PALETTE = [CYAN, ACCENT, GOLD, GREEN, PURPLE, "#F778BA", "#79C0FF", "#FFA657"]


def api(url: str, accept: str = "application/vnd.github+json"):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": f"{USER}-profile-stats",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)


def graphql(query: str, variables: dict | None = None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": f"{USER}-profile-stats",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        payload = json.load(res)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]


def years_since(iso: str) -> int:
    created = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    return max(1, int((now - created).days / 365.25))


def collect() -> dict:
    user = api(f"https://api.github.com/users/{USER}")
    repos: list[dict] = []
    page = 1
    while True:
        batch = api(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}&type=owner")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    own = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in own)
    forks = sum(r.get("forks_count", 0) for r in own)

    lang_bytes: Counter[str] = Counter()
    for repo in own:
        langs = api(f"https://api.github.com/repos/{USER}/{repo['name']}/languages")
        for name, size in langs.items():
            lang_bytes[name] += size

    top = lang_bytes.most_common()
    contributions = None
    if TOKEN:
        try:
            data = graphql(
                """
                query($login: String!) {
                  user(login: $login) {
                    contributionsCollection {
                      contributionCalendar { totalContributions }
                    }
                  }
                }
                """,
                {"login": USER},
            )
            contributions = data["user"]["contributionsCollection"]["contributionCalendar"][
                "totalContributions"
            ]
        except Exception as exc:
            print(f"graphql skipped: {exc}", file=sys.stderr)

    return {
        "login": USER,
        "repos": user.get("public_repos", 0),
        "followers": user.get("followers", 0),
        "stars": stars,
        "forks": forks,
        "years": years_since(user["created_at"]),
        "contributions": contributions,
        "top": top,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


def esc(value) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def fmt_pct(size: int, total: int) -> str:
    pct = 100 * size / total
    if pct < 0.1:
        return "<0.1%"
    if pct < 1:
        return f"{pct:.1f}%"
    return f"{pct:.0f}%"


def render(data: dict, width: int = 880, height: int | None = None) -> str:
    metrics = [
        ("PUBLIC REPOS", data["repos"], CYAN),
        ("STARS", data["stars"], GOLD),
        ("FORKS", data["forks"], GREEN),
        ("FOLLOWERS", data["followers"], PURPLE),
    ]

    langs = data["top"]
    legend_cols = 4
    legend_rows = max(1, (len(langs) + legend_cols - 1) // legend_cols)
    footer_y = 174 + legend_rows * 22 + 28
    if height is None:
        height = footer_y + 20

    tile_w = (width - 64 - 36) / 4
    tiles = []
    for i, (label, value, color) in enumerate(metrics):
        x = 32 + i * (tile_w + 12)
        tiles.append(
            f"""
  <rect x="{x:.1f}" y="32" width="{tile_w:.1f}" height="72" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{x + 16:.1f}" y="56" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="1.2">{esc(label)}</text>
  <text x="{x + 16:.1f}" y="86" fill="{color}" font-size="28" font-weight="700" font-family="{SANS}">{esc(value)}</text>"""
        )

    total = sum(size for _, size in langs) or 1
    bar_x, bar_y, bar_w, bar_h = 32, 144, width - 64, 14
    cursor = bar_x
    segments = []
    legend = []
    col_w = (width - 64) / legend_cols
    for i, (lang, size) in enumerate(langs):
        color = PALETTE[i % len(PALETTE)]
        seg = bar_w * size / total
        if i == len(langs) - 1:
            seg = bar_x + bar_w - cursor
        segments.append(
            f'<rect x="{cursor:.1f}" y="{bar_y}" width="{max(seg, 0):.1f}" height="{bar_h}" fill="{color}"/>'
        )
        col = i % legend_cols
        row = i // legend_cols
        lx = 32 + col * col_w
        ly = 174 + row * 22
        legend.append(
            f"""
  <rect x="{lx:.1f}" y="{ly:.1f}" width="8" height="8" rx="2" fill="{color}"/>
  <text x="{lx + 14:.1f}" y="{ly + 9:.1f}" fill="{TEXT}" font-size="12" font-family="{SANS}">{esc(lang)} {esc(fmt_pct(size, total))}</text>"""
        )
        cursor += seg

    years = data["years"]
    contrib = data.get("contributions")
    extra = f" · {contrib} contribs last year" if contrib is not None else ""
    generated = esc(data["generated"])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="GitHub stats for {esc(data['login'])}">
  <rect width="{width}" height="{height}" rx="12" fill="{PANEL}" stroke="{STROKE}"/>
{''.join(tiles)}
  <defs>
    <clipPath id="langbar">
      <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7"/>
    </clipPath>
  </defs>
  <text x="32" y="132" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="1.2">LANGUAGE BYTES (OWN REPOS)</text>
  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7" fill="{PANEL}"/>
  <g clip-path="url(#langbar)">{''.join(segments)}</g>
{''.join(legend)}
  <text x="32" y="{footer_y}" fill="{MUTED}" font-size="11" font-family="{SANS}">on github {years}y{extra} · generated {generated}</text>
</svg>
"""


HEADER_W = 880


def write_header() -> None:
    path = os.path.join(os.path.dirname(OUT) or ".", "stats-header.svg")
    accent_end = 32 + 112
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{HEADER_W}" height="56" viewBox="0 0 {HEADER_W} 56" role="img" aria-label="GitHub stats">
  <path d="M32 48H{HEADER_W - 32}" stroke="{STROKE}"/>
  <path d="M32 48H{accent_end}" stroke="{CYAN}" stroke-width="2"/>
  <circle cx="32" cy="48" r="3" fill="{CYAN}"/>
  <text x="32" y="29" fill="{TEXT}" font-size="18" font-weight="700" font-family="{SANS}">GitHub stats</text>
  <text x="{HEADER_W - 32}" y="29" text-anchor="end" fill="{MUTED}" font-size="12" font-family="{SANS}">Metrics from GitHub</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(svg)
    print(f"wrote {path}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    write_header()
    try:
        stats = collect()
    except Exception as exc:
        print(f"API fetch failed: {exc}", file=sys.stderr)
        sys.exit(1)
    with open(OUT, "w", encoding="utf-8") as handle:
        handle.write(render(stats))
    print(f"wrote {OUT}: {stats}")
