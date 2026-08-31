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
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
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
  <text x="{width - 38}" y="32" fill="{MUTED}" font-size="11" font-family="{MONO}">{esc(live)}</text>"""


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
  <text x="{pad + 16}" y="{y + 32}" fill="{CYAN}" font-size="22" font-weight="700" font-family="{MONO}">vikas</text>
  <text x="{pad + 92}" y="{y + 32}" fill="{MUTED}" font-size="14" font-family="{MONO}">— backend engineer (6+ years)</text>
  <text x="{pad + 16}" y="{y + 56}" fill="{TEXT}" font-size="13" font-family="{MONO}">Senior Backend Engineer · NestJS, distributed systems, and agentic AI</text>
  <text x="{pad + 16}" y="{y + 76}" fill="{MUTED}" font-size="12" font-family="{MONO}">Dehradun, India · open to remote · ervikassingh.com</text>"""
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
        f'  <text x="{pad + 16}" y="{y + 48 + i * 18}" fill="{TEXT if i == 0 else MUTED}" font-size="{"13" if i == 0 else "12"}" font-family="{MONO}">{esc(line)}</text>'
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
  <text x="{cx + 16}" y="{cy}" fill="{TEXT}" font-size="12" font-family="{MONO}">{esc(label)}</text>"""
        )
    parts.append(
        f"""
  <rect x="{pad}" y="{y}" width="{col_w:.1f}" height="{mid_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{pad + 16}" y="{y + 24}" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="1.2">PHILOSOPHY.TXT</text>
{quote}
  <rect x="{pad + col_w + gap:.1f}" y="{y}" width="{col_w:.1f}" height="{mid_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{pad + col_w + gap + 16:.1f}" y="{y + 24}" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="1.2">CURRENT_FOCUS</text>
{''.join(chips)}"""
    )
    y += mid_h + gap
    health = [
        ("nestjs", CYAN),
        ("agents", PURPLE),
        ("rag", GOLD),
        ("mcp", GREEN),
        ("web3", ACCENT),
    ]
    tile_h = 72
    tile_w = (inner_w - gap * (len(health) - 1)) / len(health)
    tiles = []
    for i, (name, color) in enumerate(health):
        tx = pad + i * (tile_w + gap)
        tiles.append(
            f"""
  <rect x="{tx:.1f}" y="{y}" width="{tile_w:.1f}" height="{tile_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{tx + 14:.1f}" y="{y + 26}" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="1.2">{esc(name.upper())}</text>
  <text x="{tx + 14:.1f}" y="{y + 52}" fill="{color}" font-size="20" font-weight="700" font-family="{MONO}">ok</text>"""
        )
    height = y + tile_h + pad
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="whoami">
{shell("$ whoami", W, height)}
{''.join(parts)}
{''.join(tiles)}
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
            f'  <text x="{x + 16:.1f}" y="{y + 58 + j * 16:.1f}" fill="{TEXT}" font-size="11" font-family="{MONO}">{esc(line)}</text>'
            for j, line in enumerate(lines[:3])
        )
        cards.append(
            f"""
  <rect x="{x:.1f}" y="{y}" width="{card_w:.1f}" height="{card_h}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="{x + 16:.1f}" y="{y + 28:.1f}" fill="{color}" font-size="14" font-weight="700" font-family="{MONO}">{esc(title)}</text>
{tag_text}"""
        )
    rows = (len(domains) + cols - 1) // cols
    height = y0 + rows * card_h + (rows - 1) * gap + pad
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Stack">
{shell("$ ls ./skills --group-by=domain", W, height)}
{''.join(cards)}
</svg>
"""


def log() -> str:
    jobs = [
        (
            "Oct 2025–now",
            "Web3 Backend Developer",
            "The Hashgraph Group · remote",
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
    y0, row_h = 56, 96
    height = y0 + len(jobs) * row_h + 16
    line_h = y0 + (len(jobs) - 1) * row_h + 18
    parts = [
        f'  <line x1="48" y1="{y0 + 18}" x2="48" y2="{line_h}" stroke="{STROKE}" stroke-width="2"/>'
    ]
    for i, (when, title, company, blurb, color) in enumerate(jobs):
        y = y0 + i * row_h
        lines = wrap(blurb, 92)
        blurb_svg = "\n".join(
            f'  <text x="88" y="{y + 70 + j * 14}" fill="{MUTED}" font-size="11" font-family="{MONO}">{esc(line)}</text>'
            for j, line in enumerate(lines[:2])
        )
        parts.append(
            f"""
  <circle cx="48" cy="{y + 18}" r="6" fill="{color}" stroke="{BG}" stroke-width="3"/>
  <rect x="72" y="{y}" width="{W - 104}" height="88" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="88" y="{y + 22}" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="0.8">{esc(when)}</text>
  <text x="88" y="{y + 44}" fill="{TEXT}" font-size="14" font-weight="700" font-family="{MONO}">{esc(title)}</text>
  <text x="520" y="{y + 44}" fill="{color}" font-size="12" font-family="{MONO}">{esc(company)}</text>
{blurb_svg}"""
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Career log">
{shell("$ git log --author=vikas --oneline --decorate", W, height)}
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
  <text x="{x + 16:.1f}" y="{y + 32:.1f}" fill="{color}" font-size="14" font-weight="700" font-family="{MONO}">{esc(name)}</text>
  <text x="{x + 16:.1f}" y="{y + 54:.1f}" fill="{MUTED}" font-size="12" font-family="{MONO}">{esc(desc)}</text>"""
        )
    rows = (len(repos) + cols - 1) // cols
    height = y0 + rows * card_h + (rows - 1) * gap + pad
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Selected work">
{shell("$ gh repo list ervikassingh --limit 5 --selected", W, height)}
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
  <text x="{x + 38:.1f}" y="{y0 + 28}" fill="{MUTED}" font-size="11" font-family="{MONO}">{esc(when)}</text>
  <text x="{x + 16:.1f}" y="{y0 + 56}" fill="{TEXT}" font-size="13" font-weight="700" font-family="{MONO}">{esc(title)}</text>
  <text x="{x + 16:.1f}" y="{y0 + 76}" fill="{color}" font-size="12" font-family="{MONO}">{esc(issuer)}</text>"""
        )
    height = y0 + card_h + pad
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Certifications">
{shell("$ cat ./certs.json", W, height)}
{''.join(cards)}
</svg>
"""


if __name__ == "__main__":
    write("whoami.svg", whoami())
    write("stack.svg", stack())
    write("log.svg", log())
    write("work.svg", work())
    write("certs.svg", certs())
