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


def section_header(title: str, subtitle: str) -> str:
    # Keep the accent tied to the visible heading rather than using a fixed card-like width.
    heading_widths = {
        "About me": 89,
        "Technical stack": 137,
        "Career timeline": 137,
        "Selected work": 128,
        "Certifications": 123,
    }
    accent_end = 32 + heading_widths.get(title, len(title) * 10)
    return f"""  <path d="M32 48H{W - 32}" stroke="{STROKE}"/>
  <path d="M32 48H{accent_end}" stroke="{CYAN}" stroke-width="2"/>
  <circle cx="32" cy="48" r="3" fill="{CYAN}"/>
  <text x="32" y="29" fill="{TEXT}" font-size="18" font-weight="700" font-family="{SANS}">{esc(title)}</text>
  <text x="{W - 32}" y="29" text-anchor="end" fill="{MUTED}" font-size="12" font-family="{SANS}">{esc(subtitle)}</text>"""


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
  <text x="16" y="56" fill="{TEXT}" font-size="13" font-family="{SANS}">NestJS, Distributed Systems, and Agentic AI</text>
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
# Keep the icons prominent while leaving a little more breathing room.
ICON_SRC = 16
ICON_SIZE = 14
ICON_GAP = 7
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
    # Center the larger icon + label block horizontally and vertically.
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
    monochrome = MUTED
    mail = """    <rect x="0.5" y="1.5" width="15" height="13" rx="2"/>
    <path d="M0.5 4.2 8 10.8l7.5-6.6"/>"""
    website = """    <rect x="1" y="1.5" width="14" height="13" rx="2"/>
    <path d="M1 5.2h14M4 3.3h.1M6.5 3.3h.1M9 3.3h.1"/>"""
    linkedin = """    <path d="M2.2 5.8v7.8M2.2 2.6v.1M5.8 13.6V5.8m0 3.7c0-2.1 1.1-3.7 3.1-3.7 1.9 0 2.9 1.2 2.9 3.6v4.2"/>"""
    twitter = """    <path d="M14.8 3.1a6.1 6.1 0 0 1-1.75.48A3.05 3.05 0 0 0 14.39 1.9a6.1 6.1 0 0 1-1.93.74A3.04 3.04 0 0 0 7.2 4.72c0 .24.03.47.08.69A8.63 8.63 0 0 1 1 2.24a3.04 3.04 0 0 0 .94 4.06 3.04 3.04 0 0 1-1.38-.38v.04a3.04 3.04 0 0 0 2.44 2.98 3.07 3.07 0 0 1-1.37.05 3.04 3.04 0 0 0 2.84 2.11A6.1 6.1 0 0 1 .7 12.4a8.6 8.6 0 0 0 4.66 1.37c5.6 0 8.66-4.64 8.66-8.66v-.39a6.2 6.2 0 0 0 1.53-1.61z"/>"""
    instagram = """    <rect x="0.7" y="0.7" width="14.6" height="14.6" rx="4.2"/>
    <circle cx="8" cy="8" r="3.2"/>
    <circle cx="12.2" cy="3.8" r="0.8"/>"""

    contacts = [
        # Icons and labels intentionally use one muted color to match the reference.
        ("Email", mail),
        ("Portfolio", website),
        ("LinkedIn", linkedin),
        ("X", twitter),
        ("Instagram", instagram),
    ]
    for label, icon in contacts:
        write(
            f"pill-{label.lower()}.svg",
            pill(label, icon, color=monochrome, weight=600, font=SANS),
        )


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
