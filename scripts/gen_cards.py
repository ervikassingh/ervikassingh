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


def section_header(title: str, subtitle: str) -> str:
    return f"""  <rect width="{W}" height="56" rx="12" fill="{BG}" stroke="{STROKE}"/>
  <text x="32" y="35" fill="{TEXT}" font-size="18" font-weight="700" font-family="{SANS}">{esc(title)}</text>
  <text x="{W - 32}" y="35" text-anchor="end" fill="{MUTED}" font-size="12" font-family="{SANS}">{esc(subtitle)}</text>"""


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


def whoami_header() -> str:
    height = 56
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="About me">
{section_header("About me", "Backend Engineering · AI · Web3")}
</svg>
"""


def whoami_identity() -> str:
    width, height = W - 64, 92
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="vikas singh">
  <rect width="{width}" height="{height}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="16" y="32" font-family="{SANS}">
    <tspan fill="{CYAN}" font-size="22" font-weight="700">vikas singh</tspan>
    <tspan fill="{MUTED}" font-size="14">  — Senior Backend Engineer (6+ years)</tspan>
  </text>
  <text x="16" y="56" fill="{TEXT}" font-size="13" font-family="{SANS}">NestJS, distributed systems, and agentic AI</text>
  <text x="16" y="76" fill="{MUTED}" font-size="12" font-family="{SANS}">Dehradun, India · open to remote · ervikassingh.com</text>
</svg>
"""


def whoami_philosophy() -> str:
    width, height = card_width(2), 118
    lines = [
        '"AI is whatever hasn\'t been done yet."',
        "— Tesler's Theorem",
        "(Larry Tesler, via Hofstadter)",
    ]
    quote = "\n".join(
        f'  <text x="16" y="{48 + i * 18}" fill="{TEXT if i == 0 else MUTED}" font-size="{"13" if i == 0 else "12"}" font-family="{SANS}">{esc(line)}</text>'
        for i, line in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height}" viewBox="0 0 {width:.0f} {height}" role="img" aria-label="Philosophy">
  <rect width="{width:.0f}" height="{height}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="16" y="24" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="1.2">PHILOSOPHY.TXT</text>
{quote}
</svg>
"""


def whoami_focus() -> str:
    width, height = card_width(2), 118
    focuses = [
        ("hedera-backends", ACCENT),
        ("nestjs-services", CYAN),
        ("agent-orchestration", PURPLE),
        ("rag-evals", GOLD),
    ]
    chips = "\n".join(
        f"""  <circle cx="21" cy="{44 + i * 18 - 4}" r="3.5" fill="{color}"/>
  <text x="32" y="{44 + i * 18}" fill="{TEXT}" font-size="12" font-family="{SANS}">{esc(label)}</text>"""
        for i, (label, color) in enumerate(focuses)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height}" viewBox="0 0 {width:.0f} {height}" role="img" aria-label="Current focus">
  <rect width="{width:.0f}" height="{height}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="16" y="24" fill="{MUTED}" font-size="11" font-family="{MONO}" letter-spacing="1.2">CURRENT-FOCUS.TXT</text>
{chips}
</svg>
"""


def stack_header() -> str:
    height = 56
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Stack">
{section_header("Technical stack", "Tools and frameworks")}
</svg>
"""


LOG_CARDS = [
    (
        "hashgraph-group",
        "Oct 2025–now",
        "Web3 Backend Developer",
        "The Hashgraph Group",
        "Built Hedera backends and owned 2 products; scaled THA Academy to 120K+ users and shipped DynamoDB tooling for 200+ employees.",
        GREEN,
    ),
    (
        "appinventiv",
        "Dec 2021–Sep 2025",
        "Software Engineer, Blockchain",
        "Appinventiv",
        "Built a shared multi-chain EVM indexer and Web3 platforms; Graph queries cut latency 40% across DAOs, tokenization, and Gnosis Safe.",
        CYAN,
    ),
    (
        "ebizon-digital",
        "Oct 2020–Dec 2021",
        "Analyst Programmer",
        "EbizON Digital",
        "Built 3+ enterprise web apps with Express.js and React; optimized APIs and introduced CI/CD workflows that accelerated releases 25%.",
        GOLD,
    ),
]


def log_header() -> str:
    height = 56
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Career timeline">
{section_header("Career timeline", "Backend engineering experience")}
</svg>
"""


def log_card(when: str, title: str, company: str, blurb: str, color: str) -> str:
    width = W - 64
    height = 100
    lines = wrap(blurb, 108)
    blurb_svg = "\n".join(
        f'  <text x="56" y="{72 + j * 16}" fill="{MUTED}" font-size="12" font-family="{SANS}">{esc(line)}</text>'
        for j, line in enumerate(lines[:2])
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">
  <rect width="{width}" height="{height}" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <circle cx="28" cy="{height // 2}" r="6" fill="{color}"/>
  <text x="56" y="26" fill="{MUTED}" font-size="11" font-family="{SANS}" letter-spacing="0.4">{esc(when)}</text>
  <text x="56" y="50" fill="{TEXT}" font-size="14" font-weight="700" font-family="{SANS}">{esc(title)}</text>
  <text x="{width - 18}" y="50" text-anchor="end" fill="{color}" font-size="12" font-family="{SANS}">{esc(company)}</text>
{blurb_svg}
</svg>
"""


def work_header() -> str:
    height = 56
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Selected work">
{section_header("Selected work", "Projects and reusable building blocks")}
</svg>
"""


CERTS = [
    ("hashgraph-developer", "Hashgraph Developer", "The Hashgraph Association", "Jan 2026", CYAN),
    ("noir-zk-circuits", "Noir + ZK Circuits", "Cyfrin Updraft", "Jan 2026", PURPLE),
    ("fundamentals-of-zk-proofs", "Fundamentals of ZK Proofs", "Cyfrin Updraft", "Jan 2026", GOLD),
]
CERT_CARD_W = 264
CERT_CARD_H = 96

STACK_CARDS = [
    ("backend", "backend/", "nestjs · node · typescript · rest · grpc · graphql · ws", CYAN),
    ("data", "data/", "postgres · redis · mysql · mongodb · dynamodb · typeorm", GOLD),
    ("messaging", "messaging/", "kafka · rabbitmq · webhooks · event pipelines", GREEN),
    ("agentic-ai", "agentic-ai/", "langchain · langgraph · rag · evals · ollama · qdrant · mcp", PURPLE),
    ("infra", "infra/", "docker · k8s · helm · aws · ci/cd · prometheus · grafana", SKY),
    ("web3", "web3/", "hedera · evm · the-graph · solidity · daos · defi · gnosis-safe", ACCENT),
]
WORK_CARDS = [
    ("agent-orchestration", "agent-orchestration", "LangGraph · FastAPI · RAG · Chroma · React", PURPLE),
    ("custom-ai-agent", "custom-ai-agent", "NestJS · Ollama · RAG · Qdrant · PostgreSQL · Docker", CYAN),
    ("prompt-relay", "prompt-relay", "TypeScript · Chrome Extension · LLM context handoff", GOLD),
    ("nestjs-microservices-template", "nestjs-microservices-template", "NestJS · Nx · gRPC · Redis · Docker · Kubernetes", GREEN),
    ("nestjs-monolithic-template", "nestjs-monolithic-template", "NestJS · TypeORM · JWT · Swagger · Docker", ACCENT),
]


def certs_header() -> str:
    height = 56
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Certifications">
{section_header("Certifications", "Professional learning and certifications")}
</svg>
"""


def stack_card(slug: str, title: str, tags: str, color: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{card_width(3)}" height="108" viewBox="0 0 {card_width(3)} 108" role="img" aria-label="{esc(title)}">
  <rect width="{card_width(3)}" height="108" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="16" y="28" fill="{color}" font-size="14" font-weight="700" font-family="{SANS}">{esc(title)}</text>
  {''.join(f'<text x="16" y="{58 + i * 16}" fill="{TEXT}" font-size="11" font-family="{SANS}">{esc(line)}</text>' for i, line in enumerate(wrap(tags, 32)[:3]))}
</svg>
"""


def work_card(slug: str, title: str, desc: str, color: str) -> str:
    width = (W - 64 - 12) / 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="78" viewBox="0 0 {width:.0f} 78" role="img" aria-label="{esc(title)}">
  <rect width="{width:.0f}" height="78" rx="8" fill="{PANEL}" stroke="{STROKE}"/>
  <text x="16" y="32" fill="{color}" font-size="14" font-weight="700" font-family="{SANS}">{esc(title)}</text>
  <text x="16" y="54" fill="{MUTED}" font-size="12" font-family="{SANS}">{esc(desc)}</text>
</svg>
"""


def card_width(columns: int) -> float:
    gap, pad = 12, 32
    return (W - pad * 2 - gap * (columns - 1)) / columns


def cert_card(slug: str, title: str, issuer: str, when: str, color: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CERT_CARD_W}" height="{CERT_CARD_H}" viewBox="0 0 {CERT_CARD_W} {CERT_CARD_H}" role="img" aria-label="{esc(title)}">
  <rect width="{CERT_CARD_W}" height="{CERT_CARD_H}" rx="12" fill="{PANEL}" stroke="{STROKE}"/>
  <circle cx="24" cy="24" r="6" fill="{color}"/>
  <text x="38" y="28" fill="{MUTED}" font-size="11" font-family="{SANS}">{esc(when)}</text>
  <text x="16" y="56" fill="{TEXT}" font-size="13" font-weight="700" font-family="{SANS}">{esc(title)}</text>
  <text x="16" y="76" fill="{color}" font-size="12" font-family="{SANS}">{esc(issuer)}</text>
</svg>
"""


PILL_H = 32
FONT_SIZE = 12
TEXT_Y = 21
# Same cap-height and baseline as the 12px label.
ICON_SRC = 16
ICON_SIZE = 11
ICON_GAP = 6
CHAR_W = 7.4
PAD_X = 12


def pill_width(label: str) -> int:
    return round(PAD_X + ICON_SIZE + ICON_GAP + len(label) * CHAR_W + PAD_X)


def pill(
    label: str,
    icon: str,
    width: int | None = None,
    color: str = CYAN,
    rx: int = 8,
    weight: int = 400,
    font: str = MONO,
) -> str:
    w = width if width is not None else pill_width(label)
    scale = ICON_SIZE / ICON_SRC
    # Center the icon + label block horizontally and vertically.
    content_w = ICON_SIZE + ICON_GAP + len(label) * CHAR_W
    icon_x = (w - content_w) / 2
    icon_y = (PILL_H - ICON_SIZE) / 2
    text_x = icon_x + ICON_SIZE + ICON_GAP
    weight_attr = f' font-weight="{weight}"' if weight != 400 else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{PILL_H}" viewBox="0 0 {w} {PILL_H}" role="img" aria-label="{esc(label)}">
  <rect width="{w}" height="{PILL_H}" rx="{rx}" fill="{PANEL}" stroke="{STROKE}"/>
  <g transform="translate({icon_x:.1f},{icon_y:.1f}) scale({scale:.4f})" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
{icon}
  </g>
  <text x="{text_x:.1f}" y="{TEXT_Y}" fill="{color}" font-size="{FONT_SIZE}"{weight_attr} font-family="{font}">{esc(label)}</text>
</svg>
"""


def write_pills() -> None:
    mail = """    <rect x="0.5" y="1.5" width="15" height="13" rx="2"/>
    <path d="M0.5 4.2 8 10.8l7.5-6.6"/>"""
    globe = """    <circle cx="8" cy="8" r="7.2"/>
    <path d="M0.8 8h14.4"/>
    <path d="M8 0.8c2.1 2.3 3.2 4.6 3.2 7.2s-1.1 4.9-3.2 7.2C5.9 12.9 4.8 10.6 4.8 8s1.1-4.9 3.2-7.2z"/>"""
    def linkedin(color: str) -> str:
        return f"""    <rect x="0" y="0" width="16" height="16" rx="2.6" fill="{color}" stroke="none"/>
    <text x="8" y="12.4" text-anchor="middle" fill="{PANEL}" stroke="none" font-size="10" font-weight="700" font-family="{SANS}">in</text>"""

    def x_logo(color: str) -> str:
        return f"""    <path d="M0.4 0.6h3.6l3.5 4.7 4.15-4.7H15.6L9.2 8.4 15.5 15.4h-3.7L8 10.4 3.55 15.4H0.2l6.5-7.2z" fill="{color}" stroke="none"/>"""

    def github(color: str) -> str:
        return f"""    <path fill="{color}" stroke="none" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82A7.65 7.65 0 0 1 8 3.7c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>"""

    award = """    <circle cx="8" cy="6.4" r="5.2"/>
    <path d="M4.6 10.4 3.2 16 8 13.6 12.8 16 11.4 10.4"/>"""
    contacts = [
        # (label, icon, accent) — brand-accurate colors on the dark theme
        ("Email", mail, CYAN),
        ("Portfolio", globe, SKY),
        ("LinkedIn", linkedin("#4A9EEF"), "#4A9EEF"),
        ("X", x_logo(TEXT), TEXT),
    ]
    for label, icon, color in contacts:
        write(
            f"pill-{label.lower()}.svg",
            pill(label, icon, color=color, weight=600, font=SANS),
        )
    for name in (
        "custom-ai-agent",
        "nestjs-microservices-template",
        "nestjs-monolithic-template",
        "prompt-relay",
        "nft-market",
    ):
        write(f"pill-{name}.svg", pill(name, github(CYAN)))
    for name in (
        "hashgraph-developer",
        "noir-zk-circuits",
        "fundamentals-of-zk-proofs",
    ):
        write(f"pill-{name}.svg", pill(name, award, color=GOLD))


if __name__ == "__main__":
    write("whoami-header.svg", whoami_header())
    write("whoami-identity.svg", whoami_identity())
    write("whoami-philosophy.svg", whoami_philosophy())
    write("whoami-focus.svg", whoami_focus())
    write("stack-header.svg", stack_header())
    for slug, title, tags, color in STACK_CARDS:
        write(f"stack-{slug}.svg", stack_card(slug, title, tags, color))
    write("log-header.svg", log_header())
    for slug, when, title, company, blurb, color in LOG_CARDS:
        write(f"log-{slug}.svg", log_card(when, title, company, blurb, color))
    write("work-header.svg", work_header())
    for slug, title, desc, color in WORK_CARDS:
        write(f"work-{slug}.svg", work_card(slug, title, desc, color))
    write("certs-header.svg", certs_header())
    for slug, title, issuer, when, color in CERTS:
        write(f"cert-{slug}.svg", cert_card(slug, title, issuer, when, color))
    write_pills()
