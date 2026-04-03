#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
ASSET_DIR = ROOT / "plugins" / "codex-game-studio" / "assets"
WIDTH = 1600
HEIGHT = 960

COLOR = {
    "bg_top": "#08110C",
    "bg_bottom": "#0F1F16",
    "panel": "#122418",
    "panel_alt": "#173122",
    "panel_soft": "#1C3A28",
    "border": "#2F6B49",
    "muted": "#A7C9B5",
    "text": "#F2FFF6",
    "accent": "#4ADE80",
    "accent_soft": "#A7F3D0",
    "amber": "#FBBF24",
    "slate": "#D2E7DB",
    "deep": "#0A170F",
}

FONT_PATHS = {
    "display": [
        "/System/Library/Fonts/Futura.ttc",
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Avenir.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ],
    "bold": [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ],
    "body": [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ],
    "mono": [
        "/System/Library/Fonts/Courier.ttc",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
    ],
}


def load_font(kind: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_PATHS[kind]:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


DISPLAY_XL = load_font("display", 76)
DISPLAY_LG = load_font("display", 52)
TITLE_MD = load_font("bold", 30)
TITLE_SM = load_font("bold", 22)
BODY = load_font("body", 26)
BODY_SM = load_font("body", 20)
CAPTION = load_font("body", 18)
MONO = load_font("mono", 18)


def new_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (WIDTH, HEIGHT), COLOR["bg_top"])
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        ratio = y / max(HEIGHT - 1, 1)
        r1, g1, b1 = ImageColor.hex_to_rgb(COLOR["bg_top"])
        r2, g2, b2 = ImageColor.hex_to_rgb(COLOR["bg_bottom"])
        color = (
            int(r1 + (r2 - r1) * ratio),
            int(g1 + (g2 - g1) * ratio),
            int(b1 + (b2 - b1) * ratio),
            255,
        )
        draw.line([(0, y), (WIDTH, y)], fill=color)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((WIDTH - 520, -180, WIDTH + 120, 420), fill=(74, 222, 128, 44))
    od.ellipse((-180, HEIGHT - 420, 420, HEIGHT + 120), fill=(56, 189, 248, 26))
    od.ellipse((WIDTH - 760, HEIGHT - 300, WIDTH - 120, HEIGHT + 220), fill=(251, 191, 36, 18))
    image.alpha_composite(overlay)
    return image, draw


class ImageColor:
    @staticmethod
    def hex_to_rgb(value: str) -> tuple[int, int, int]:
        value = value.lstrip("#")
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str | None = None, width: int = 2, radius: int = 28) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if text_size(draw, trial, font)[0] <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, fill: str, box: tuple[int, int, int, int], line_gap: int = 10) -> int:
    x1, y1, x2, _ = box
    lines = wrap_lines(draw, text, font, x2 - x1)
    y = y1
    for line in lines:
        draw.text((x1, y), line, font=font, fill=fill)
        y += text_size(draw, line, font)[1] + line_gap
    return y


def chip(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, fill: str = COLOR["panel_alt"], border: str = COLOR["border"], text_fill: str = COLOR["text"]) -> int:
    w, h = text_size(draw, text, BODY_SM)
    pad_x = 18
    pad_y = 10
    rounded(draw, (x, y, x + w + pad_x * 2, y + h + pad_y * 2), fill=fill, outline=border, width=2, radius=18)
    draw.text((x + pad_x, y + pad_y - 1), text, font=BODY_SM, fill=text_fill)
    return x + w + pad_x * 2 + 12


def metric_card(draw: ImageDraw.ImageDraw, x: int, y: int, value: str, label: str, tone: str) -> None:
    rounded(draw, (x, y, x + 260, y + 150), fill=COLOR["panel"], outline=COLOR["border"], width=2, radius=30)
    draw.text((x + 26, y + 26), value, font=DISPLAY_LG, fill=tone)
    draw.text((x + 26, y + 98), label, font=BODY_SM, fill=COLOR["muted"])


def panel_title(draw: ImageDraw.ImageDraw, x: int, y: int, title: str, subtitle: str | None = None) -> int:
    draw.text((x, y), title, font=TITLE_MD, fill=COLOR["text"])
    next_y = y + 40
    if subtitle:
        next_y = draw_wrapped(draw, subtitle, BODY_SM, COLOR["muted"], (x, y + 42, x + 520, y + 120), line_gap=6) + 6
    return next_y


def render_overview() -> Image.Image:
    image, draw = new_canvas()
    draw.text((86, 88), "Codex Game Studio", font=DISPLAY_XL, fill=COLOR["text"])
    draw.text((90, 178), "Turn one Codex session into a structured game development studio.", font=BODY, fill=COLOR["accent_soft"])
    rounded(draw, (1228, 94, 1498, 156), fill=COLOR["panel_alt"], outline=COLOR["border"], width=2, radius=26)
    draw.text((1262, 113), "Codex-native plugin", font=BODY_SM, fill=COLOR["accent"])

    metric_card(draw, 86, 258, "38", "Workflow entrypoints", COLOR["accent"])
    metric_card(draw, 372, 258, "48", "Role briefs", COLOR["amber"])
    metric_card(draw, 658, 258, "26", "Templates", "#60A5FA")
    metric_card(draw, 944, 258, "46", "Engine references", "#F472B6")

    rounded(draw, (86, 454, 860, 850), fill=COLOR["panel"], outline=COLOR["border"], width=2, radius=34)
    y = panel_title(draw, 122, 486, "Studio shape", "The role system keeps direction, ownership, and execution separate instead of collapsing everything into one prompt.")
    tier_y = y + 12
    tiers = [
        ("Leadership", "creative-director, technical-director, producer", COLOR["accent"]),
        ("Department leads", "game-designer, lead-programmer, art-director, qa-lead", COLOR["amber"]),
        ("Specialists", "gameplay-programmer, ui-programmer, writer, technical-artist", "#60A5FA"),
    ]
    for title, body, tone in tiers:
        rounded(draw, (122, tier_y, 824, tier_y + 84), fill=COLOR["panel_alt"], outline=COLOR["border"], width=2, radius=24)
        draw.text((152, tier_y + 18), title, font=TITLE_SM, fill=tone)
        draw.text((152, tier_y + 48), body, font=BODY_SM, fill=COLOR["slate"])
        tier_y += 96

    rounded(draw, (900, 454, 1510, 850), fill=COLOR["panel"], outline=COLOR["border"], width=2, radius=34)
    panel_title(draw, 936, 486, "Core workflow lanes", "Move from concept to implementation and ship checks through named skills instead of ad hoc prompting.")
    x = 936
    y = 580
    for label in ["game-studio", "start", "setup-engine"]:
        x = chip(draw, x, y, label)
    x = 936
    y = 648
    for label in ["brainstorm", "map-systems", "design-system"]:
        x = chip(draw, x, y, label, fill=COLOR["panel_soft"])
    x = 936
    y = 716
    for label in ["team-combat", "team-ui", "team-release"]:
        x = chip(draw, x, y, label)
    x = 936
    y = 784
    for label in ["gate-check", "perf-profile", "launch-checklist"]:
        x = chip(draw, x, y, label, fill=COLOR["panel_soft"])

    draw.text((88, 894), "Codex-first production kit for planning, implementation, QA, and release work.", font=CAPTION, fill=COLOR["muted"])
    return image


def stage_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, items: list[str], tone: str) -> None:
    rounded(draw, box, fill=COLOR["panel"], outline=COLOR["border"], width=2, radius=30)
    x1, y1, x2, _ = box
    draw.text((x1 + 26, y1 + 22), title, font=TITLE_MD, fill=tone)
    y = y1 + 76
    for item in items:
        rounded(draw, (x1 + 24, y, x2 - 24, y + 56), fill=COLOR["panel_alt"], outline=COLOR["border"], width=2, radius=20)
        draw.text((x1 + 42, y + 14), item, font=BODY_SM, fill=COLOR["text"])
        y += 68


def render_router() -> Image.Image:
    image, draw = new_canvas()
    draw.text((86, 88), "Route work through named workflows", font=DISPLAY_LG, fill=COLOR["text"])
    draw_wrapped(
        draw,
        "A single repo can move from onboarding to delivery if the work is routed through explicit lanes with shared docs and release gates.",
        BODY,
        COLOR["accent_soft"],
        (90, 154, 1180, 240),
        line_gap=8,
    )
    rounded(draw, (1208, 90, 1502, 148), fill=COLOR["panel_alt"], outline=COLOR["border"], width=2, radius=24)
    draw.text((1238, 108), "main protected", font=BODY_SM, fill=COLOR["accent"])

    boxes = [
        ((86, 310, 424, 796), "Kickoff", ["game-studio", "start", "setup-engine", "project-stage-detect"], COLOR["accent"]),
        ((454, 310, 792, 796), "Design", ["brainstorm", "map-systems", "design-review", "architecture-decision"], COLOR["amber"]),
        ((822, 310, 1160, 796), "Implementation", ["team-combat", "team-ui", "team-level", "team-release"], "#60A5FA"),
        ((1190, 310, 1528, 796), "Control", ["gate-check", "perf-profile", "release-checklist", "hotfix"], "#F472B6"),
    ]
    for box, title, items, tone in boxes:
        stage_box(draw, box, title, items, tone)

    for start_x in (424, 792, 1160):
        draw.line((start_x + 12, 554, start_x + 18, 554), fill=COLOR["accent_soft"], width=6)
        draw.polygon([(start_x + 18, 542), (start_x + 48, 554), (start_x + 18, 566)], fill=COLOR["accent_soft"])

    rounded(draw, (86, 828, 1528, 892), fill=COLOR["panel_soft"], outline=COLOR["border"], width=2, radius=24)
    draw.text((116, 848), "Shared docs: docs/CODEX-STUDIO.md  •  docs/studio/technical-preferences.md  •  docs/engine-reference/", font=BODY_SM, fill=COLOR["slate"])
    return image


def doc_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], path: str, title: str, note: str, tone: str) -> None:
    rounded(draw, box, fill=COLOR["panel"], outline=COLOR["border"], width=2, radius=28)
    x1, y1, x2, _ = box
    draw.text((x1 + 24, y1 + 22), path, font=MONO, fill=tone)
    draw.text((x1 + 24, y1 + 62), title, font=TITLE_SM, fill=COLOR["text"])
    draw_wrapped(draw, note, BODY_SM, COLOR["muted"], (x1 + 24, y1 + 102, x2 - 24, y1 + 180), line_gap=6)


def render_references() -> Image.Image:
    image, draw = new_canvas()
    draw.text((86, 88), "Pin decisions and current references", font=DISPLAY_LG, fill=COLOR["text"])
    draw_wrapped(
        draw,
        "The plugin stays grounded by keeping engine, standards, and validation in explicit repo files instead of hidden chat state.",
        BODY,
        COLOR["accent_soft"],
        (90, 154, 1200, 240),
        line_gap=8,
    )

    doc_card(
        draw,
        (86, 302, 556, 516),
        "docs/CODEX-STUDIO.md",
        "Project configuration",
        "Pins the active engine, the collaboration protocol, and the current reference path that the studio should treat as source of truth.",
        COLOR["accent"],
    )
    doc_card(
        draw,
        (86, 546, 556, 760),
        "docs/studio/technical-preferences.md",
        "Technical conventions",
        "Captures naming, performance budgets, testing expectations, and engine-specific rules after setup-engine configures the project.",
        COLOR["amber"],
    )
    doc_card(
        draw,
        (586, 302, 1056, 760),
        "docs/engine-reference/",
        "Version-aware engine notes",
        "Curated Godot, Unity, and Unreal references keep Codex aligned with current APIs and known engine changes beyond model training data.",
        "#60A5FA",
    )

    rounded(draw, (1088, 302, 1528, 760), fill=COLOR["panel"], outline=COLOR["border"], width=2, radius=34)
    panel_title(draw, 1122, 334, "Release safety", "The repo now enforces a validate check on main and ships plugin screenshots directly from tracked assets.")
    x = 1122
    y = 440
    for label, fill in [("validate required", COLOR["panel_alt"]), ("admins enforced", COLOR["panel_soft"]), ("force-push blocked", COLOR["panel_alt"]), ("branch delete blocked", COLOR["panel_soft"])]:
        x = chip(draw, x, y, label, fill=fill)
        if x > 1440:
            x = 1122
            y += 70
    rounded(draw, (1118, 612, 1494, 716), fill=COLOR["deep"], outline=COLOR["border"], width=2, radius=22)
    draw.text((1148, 640), "plugin.json -> screenshots[]", font=MONO, fill=COLOR["accent"])
    draw.text((1148, 672), "README + README.vi -> shared preview assets", font=BODY_SM, fill=COLOR["slate"])

    rounded(draw, (86, 816, 1528, 892), fill=COLOR["panel_soft"], outline=COLOR["border"], width=2, radius=24)
    draw.text((118, 840), "Use game-studio to route the repo, setup-engine to pin the stack, and gate-check to control phase changes.", font=BODY_SM, fill=COLOR["text"])
    return image


def save(image: Image.Image, name: str) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(ASSET_DIR / name, format="PNG", optimize=True)


def main() -> int:
    save(render_overview(), "preview-studio-overview.png")
    save(render_router(), "preview-workflow-router.png")
    save(render_references(), "preview-reference-stack.png")
    print("Preview assets rendered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
