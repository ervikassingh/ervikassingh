#!/usr/bin/env python3
"""Generate profile section SVGs in the same style as stats.svg."""

from __future__ import annotations

import os

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
SKY = "#79C0FF"
# GitHub renders SVGs as <img>, so webfonts will not load. Prefer native UI fonts.
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
OUT_DIR = os.environ.get("OUT_DIR", "assets")
W = 880


def esc(value) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def shell(prompt: str, width: int, height: int, live: str = "ok") -> str:
    return f"""
  <rect width="{width}" height="{height}" rx="12" fill="{BG}" stroke="{STROKE}"/>
  <text x="32" y="34" fill="{MUTED}" font-size="13" font-family="{MONO}">{esc(prompt)}</text>
  <circle cx="{width - 48}" cy="28" r="5" fill="{GREEN}"/>
  <text x="{width - 38}" y="32" fill="{MUTED}" font-size="11" font-family="{SANS}">{esc(live)}</text>"""


def wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if len(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


def write(name: str, svg: str) -> None:
    path = os.path.join(OUT_DIR, name)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(svg)
    print(f"wrote {path}")


def whoami() -> str:
    pad, gap = 32, 12
    y = 56
    inner_w = W - pad * 2
    identity_h = 92
    parts = [
        f"""
  <rect x="{pad}" y="{y}" width="{inner_w}" height="{identity_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{pad + 16}" y="{y + 32}" font-family="{SANS}">
    <tspan fill="{CYAN}" font-size="22" font-weight="700">vikas singh</tspan>
    <tspan fill="{MUTED}" font-size="14">  — Senior Backend Engineer (6+ years)</tspan>
  </text>
  <text x="{pad + 16}" y="{y + 56}" fill="{TEXT}" font-size="13" font-family="{SANS}">NestJS, distributed systems, and agentic AI</text>
  <text x="{pad + 16}" y="{y + 76}" fill="{MUTED}" font-size="12" font-family="{SANS}">Dehradun, India · open to remote · ervikassingh.com</text>"""
    ]
    y += identity_h + gap
    col_w = (inner_w - gap) / 2
    mid_h = 118
    quote_lines = [
        '"AI is whatever hasn\'t been done yet."',
        "— Tesler's Theorem",
        "(Larry Tesler, via Hofstadter)",
    ]
    quote = "\n".join(
        f'  <text x="{pad + 16}" y="{y + 48 + i * 18}" fill="{TEXT if i == 0 else MUTED}" font-size="{"13" if i == 0 else "12"}" font-family="{SANS}">{esc(line)}</text>'
        for i, line in enumerate(quote_lines)
    )
    focuses = [
        ("hedera-backends", ACCENT),
        ("nestjs-services", CYAN),
        ("agent-orchestration", PURPLE),
        ("rag-evals", GOLD),
    ]
    chip_y0 = y + 44
    chips = []
    for i, (label, color) in enumerate(focuses):
        cx = pad + col_w + gap + 16
        cy = chip_y0 + i * 18
        chips.append(
            f"""
  <circle cx="{cx + 5}" cy="{cy - 4}" r="3.5" fill="{color}"/>
  <text x="{cx + 16}" y="{cy}" fill="{TEXT}" font-size="12" font-family="{SANS}">{esc(label)}</text>"""
        )
    parts.append(
        f"""
  <rect x="{pad}" y="{y}" width="{col_w:.1f}" height="{mid_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{pad + 16}" y="{y + 24}" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="1.2">PHILOSOPHY.TXT</text>
{quote}
  <rect x="{pad + col_w + gap:.1f}" y="{y}" width="{col_w:.1f}" height="{mid_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{pad + col_w + gap + 16:.1f}" y="{y + 24}" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="1.2">CURRENT-FOCUS.TXT</text>
{''.join(chips)}"""
    )
    height = y + mid_h + pad
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="whoami">
{shell("$ gh whoami --format=pretty --open-to=remote", W, height)}
{''.join(parts)}
</svg>
"""


def stack() -> str:
    domains = [
        ("backend/", "nestjs · node · typescript · rest · grpc · graphql · ws", CYAN),
        ("data/", "postgres · redis · mysql · mongodb · dynamodb · typeorm", GOLD),
        ("messaging/", "kafka · rabbitmq · webhooks · event pipelines", GREEN),
        ("agentic-ai/", "langchain · langgraph · rag · evals · ollama · qdrant · mcp", PURPLE),
        ("infra/", "docker · k8s · helm · aws · ci/cd · prometheus · grafana", SKY),
        ("web3/", "hedera · evm · the-graph · solidity · daos · defi · gnosis-safe", ACCENT),
    ]
    cols, gap, pad = 3, 12, 32
    card_w = (W - pad * 2 - gap * (cols - 1)) / cols
    card_h = 108
    y0 = 56
    cards = []
    for i, (title, tags, color) in enumerate(domains):
        col, row = i % cols, i // cols
        x = pad + col * (card_w + gap)
        y = y0 + row * (card_h + gap)
        lines = wrap(tags, 32)
        tag_text = "\n".join(
            f'  <text x="{x + 16:.1f}" y="{y + 58 + j * 16:.1f}" fill="{TEXT}" font-size="11" font-family="{SANS}">{esc(line)}</text>'
            for j, line in enumerate(lines[:3])
        )
        cards.append(
            f"""
  <rect x="{x:.1f}" y="{y}" width="{card_w:.1f}" height="{card_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{x + 16:.1f}" y="{y + 28:.1f}" fill="{color}" font-size="14" font-weight="700" font-family="{SANS}">{esc(title)}</text>
{tag_text}"""
        )
    rows = (len(domains) + cols - 1) // cols
    height = y0 + rows * card_h + (rows - 1) * gap + pad
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Stack">
{shell("$ gh skills --group-by=domain --limit 6", W, height)}
{''.join(cards)}
</svg>
"""


def log() -> str:
    jobs = [
        (
            "Oct 2025–now",
            "Web3 Backend Developer",
            "The Hashgraph Group",
            "NestJS/TypeScript services over Hedera DLT. Auth, ledger I/O, production Web3 APIs.",
            GREEN,
        ),
        (
            "Dec 2021–Sep 2025",
            "Software Engineer, Blockchain",
            "Appinventiv",
            "Taxicoin + collective-investment platforms. Multi-chain EVM indexer. Graph latency −40%. DAOs, Gnosis Safe.",
            CYAN,
        ),
        (
            "Oct 2020–Dec 2021",
            "Analyst Programmer",
            "EbizON Digital",
            "Express REST APIs for enterprise apps. CI/CD cut release cycle ~25%.",
            GOLD,
        ),
    ]
    pad, rail_gap, inset = 32, 22, 18
    rail_x = pad + 8
    card_x = rail_x + rail_gap
    card_w = W - card_x - pad
    text_x = card_x + inset
    y0, card_h, gap = 56, 100, 12
    row_h = card_h + gap
    height = y0 + len(jobs) * row_h - gap + pad
    mid0 = y0 + card_h / 2
    midn = y0 + (len(jobs) - 1) * row_h + card_h / 2
    parts = [
        f'  <line x1="{rail_x}" y1="{mid0:.0f}" x2="{rail_x}" y2="{midn:.0f}" stroke="{STROKE}" stroke-width="2"/>'
    ]
    for i, (when, title, company, blurb, color) in enumerate(jobs):
        y = y0 + i * row_h
        cy = y + card_h / 2
        lines = wrap(blurb, 108)
        blurb_svg = "\n".join(
            f'  <text x="{text_x}" y="{y + 72 + j * 16}" fill="{MUTED}" font-size="12" font-family="{SANS}">{esc(line)}</text>'
            for j, line in enumerate(lines[:2])
        )
        parts.append(
            f"""
  <circle cx="{rail_x}" cy="{cy:.0f}" r="6" fill="{color}" stroke="{BG}" stroke-width="3"/>
  <rect x="{card_x}" y="{y}" width="{card_w}" height="{card_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{text_x}" y="{y + 26}" fill="{MUTED}" font-size="11" font-family="{SANS}" letter-spacing="0.4">{esc(when)}</text>
  <text x="{text_x}" y="{y + 50}" fill="{TEXT}" font-size="14" font-weight="700" font-family="{SANS}">{esc(title)}</text>
  <text x="{W - pad - inset}" y="{y + 50}" text-anchor="end" fill="{color}" font-size="12" font-family="{SANS}">{esc(company)}</text>
{blurb_svg}"""
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Career log">
{shell("$ gh log --author=vikas --oneline --decorate", W, height)}
{''.join(parts)}
</svg>
"""


def work() -> str:
    repos = [
        ("custom-ai-agent", "RAG agent · NestJS · Ollama · Postgres · Qdrant", PURPLE),
        ("nestjs-microservices-template", "Nx gateway · gRPC · tracing · Helm · Grafana", CYAN),
        ("nestjs-monolithic-template", "JWT + RBAC · TypeORM · Winston · Jest · Compose", GREEN),
        ("prompt-relay", "Local-first LLM context tracking + compressed handoff", GOLD),
        ("nft-market", "ERC-20 / ERC-721 marketplace · ETH/BNB + tokens", ACCENT),
    ]
    cols, gap, pad = 2, 12, 32
    card_w = (W - pad * 2 - gap) / cols
    card_h = 78
    y0 = 56
    cards = []
    for i, (name, desc, color) in enumerate(repos):
        col, row = i % cols, i // cols
        x = pad + col * (card_w + gap)
        y = y0 + row * (card_h + gap)
        last_odd = i == len(repos) - 1 and len(repos) % cols == 1
        w = W - pad * 2 if last_odd else card_w
        cards.append(
            f"""
  <rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{card_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{x + 16:.1f}" y="{y + 32:.1f}" fill="{color}" font-size="14" font-weight="700" font-family="{SANS}">{esc(name)}</text>
  <text x="{x + 16:.1f}" y="{y + 54:.1f}" fill="{MUTED}" font-size="12" font-family="{SANS}">{esc(desc)}</text>"""
        )
    rows = (len(repos) + cols - 1) // cols
    height = y0 + rows * card_h + (rows - 1) * gap + pad
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Selected work">
{shell("$ gh repos --limit 5 --filter=selected", W, height)}
{''.join(cards)}
</svg>
"""


def certs() -> str:
    items = [
        ("Hashgraph Developer", "The Hashgraph Association", "Jan 2026", CYAN),
        ("Noir + ZK Circuits", "Cyfrin Updraft", "Jan 2026", PURPLE),
        ("Fundamentals of ZK Proofs", "Cyfrin Updraft", "Jan 2026", GOLD),
    ]
    cols, gap, pad = 3, 12, 32
    card_w = (W - pad * 2 - gap * (cols - 1)) / cols
    card_h = 96
    y0 = 56
    cards = []
    for i, (title, issuer, when, color) in enumerate(items):
        x = pad + i * (card_w + gap)
        cards.append(
            f"""
  <rect x="{x:.1f}" y="{y0}" width="{card_w:.1f}" height="{card_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <circle cx="{x + 24:.1f}" cy="{y0 + 24}" r="6" fill="{color}"/>
  <text x="{x + 38:.1f}" y="{y0 + 28}" fill="{MUTED}" font-size="11" font-family="{SANS}">{esc(when)}</text>
  <text x="{x + 16:.1f}" y="{y0 + 56}" fill="{TEXT}" font-size="13" font-weight="700" font-family="{SANS}">{esc(title)}</text>
  <text x="{x + 16:.1f}" y="{y0 + 76}" fill="{color}" font-size="12" font-family="{SANS}">{esc(issuer)}</text>"""
        )
    height = y0 + card_h + pad
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Certifications">
{shell("$ gh certs --json --sort=date", W, height)}
{''.join(cards)}
</svg>
"""


PILL_H = 32
FONT_SIZE = 12
TEXT_Y = 21
# Same cap-height and baseline as the 12px label.
ICON_SRC = 16
ICON_SIZE = 9
ICON_X = 10
ICON_Y = TEXT_Y - ICON_SIZE + 0.8
TEXT_X = ICON_X + ICON_SIZE + 6
CHAR_W = 7.4
PAD_RIGHT = 12


def pill_width(label: str) -> int:
    return round(TEXT_X + len(label) * CHAR_W + PAD_RIGHT)


def pill(label: str, icon: str, width: int | None = None, icon_stroke: str = CYAN) -> str:
    w = width if width is not None else pill_width(label)
    scale = ICON_SIZE / ICON_SRC
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{PILL_H}" viewBox="0 0 {w} {PILL_H}" role="img" aria-label="{esc(label)}">
  <rect width="{w}" height="{PILL_H}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <g transform="translate({ICON_X:.1f},{ICON_Y:.1f}) scale({scale:.4f})" fill="none" stroke="{icon_stroke}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
{icon}
  </g>
  <text x="{TEXT_X:.1f}" y="{TEXT_Y}" fill="{CYAN}" font-size="{FONT_SIZE}" font-family="{MONO}">{esc(label)}</text>
</svg>
"""


def write_pills() -> None:
    mail = """    <rect x="0.5" y="1.5" width="15" height="13" rx="2"/>
    <path d="M0.5 4.2 8 10.8l7.5-6.6"/>"""
    globe = """    <circle cx="8" cy="8" r="7.2"/>
    <path d="M0.8 8h14.4"/>
    <path d="M8 0.8c2.1 2.3 3.2 4.6 3.2 7.2s-1.1 4.9-3.2 7.2C5.9 12.9 4.8 10.6 4.8 8s1.1-4.9 3.2-7.2z"/>"""
    linkedin = f"""    <rect x="0" y="0" width="16" height="16" rx="2.6" fill="{CYAN}" stroke="none"/>
    <text x="8" y="12.4" text-anchor="middle" fill="{PANEL}" stroke="none" font-size="10" font-weight="700" font-family="{SANS}">in</text>"""
    x_logo = f"""    <path d="M0.4 0.6h3.6l3.5 4.7 4.15-4.7H15.6L9.2 8.4 15.5 15.4h-3.7L8 10.4 3.55 15.4H0.2l6.5-7.2z" fill="{CYAN}" stroke="none"/>"""
    github = f"""    <path fill="{CYAN}" stroke="none" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82A7.65 7.65 0 0 1 8 3.7c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>"""
    award = """    <circle cx="8" cy="6.4" r="5.2"/>
    <path d="M4.6 10.4 3.2 16 8 13.6 12.8 16 11.4 10.4"/>"""
    write("pill-email.svg", pill("email", mail))
    write("pill-portfolio.svg", pill("portfolio", globe))
    write("pill-linkedin.svg", pill("linkedin", linkedin))
    write("pill-x.svg", pill("x", x_logo))
    for name in (
        "custom-ai-agent",
        "nestjs-microservices-template",
        "nestjs-monolithic-template",
        "prompt-relay",
        "nft-market",
    ):
        write(f"pill-{name}.svg", pill(name, github))
    for name in (
        "hashgraph-developer",
        "noir-zk-circuits",
        "fundamentals-of-zk-proofs",
    ):
        write(f"pill-{name}.svg", pill(name, award, icon_stroke=GOLD))


if __name__ == "__main__":
    write("whoami.svg", whoami())
    write("stack.svg", stack())
    write("log.svg", log())
    write("work.svg", work())
    write("certs.svg", certs())
    write_pills()
