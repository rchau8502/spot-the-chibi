#!/usr/bin/env python3
"""
Generate official iPhone Duo App Store Screenshots for Spot The Chibi.
Specifications based on Apple Developer documentation:
  Inner Display (Unfolded Dual Screen): 2007 x 2853 px (Portrait)
  Outer Display: 1398 x 2034 px (Portrait)
"""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "AppStore_Assets")
DUO_INNER_DIR = os.path.join(OUTPUT_DIR, "Screenshots_iPhone_Duo_Inner_2007x2853")
DUO_OUTER_DIR = os.path.join(OUTPUT_DIR, "Screenshots_iPhone_Duo_Outer_1398x2034")
DESKTOP_DIR = os.path.expanduser("~/Desktop/Spot_The_Chibi_AppStore_Assets/Screenshots_iPhone_Duo")

os.makedirs(DUO_INNER_DIR, exist_ok=True)
os.makedirs(DUO_OUTER_DIR, exist_ok=True)
os.makedirs(DESKTOP_DIR, exist_ok=True)

# Inner screen dimensions
W_INNER, H_INNER = 2007, 2853
# Outer screen dimensions
W_OUTER, H_OUTER = 1398, 2034

def get_font(size, bold=True):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFCompact.ttf",
        "/System/Library/Fonts/Helvetica.ttc"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def create_gradient_bg(width, height, c1, c2):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / float(height)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    return img

def draw_header(canvas, width, tag_text, title_text, sub_text, text_color=(255, 255, 255)):
    draw = ImageDraw.Draw(canvas)
    scale = width / 2007.0
    
    # Pill Tag
    font_tag = get_font(int(46 * scale), bold=True)
    tb = draw.textbbox((0, 0), tag_text, font=font_tag)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]
    px = (width - tw) // 2
    py = int(180 * scale)
    pad_x, pad_y = int(36 * scale), int(18 * scale)
    draw.rounded_rectangle(
        [px - pad_x, py - pad_y, px + tw + pad_x, py + th + pad_y],
        radius=int(30 * scale),
        fill=(255, 255, 255, 45),
        outline=(255, 255, 255, 90),
        width=int(3 * scale)
    )
    draw.text((px, py - int(4 * scale)), tag_text, fill=(255, 255, 255, 245), font=font_tag)
    
    # Title
    font_title = get_font(int(100 * scale), bold=True)
    tb_title = draw.textbbox((0, 0), title_text, font=font_title)
    tx = (width - (tb_title[2] - tb_title[0])) // 2
    draw.text((tx, int(290 * scale)), title_text, fill=text_color, font=font_title)
    
    # Subtitle
    font_sub = get_font(int(46 * scale), bold=False)
    tb_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    sx = (width - (tb_sub[2] - tb_sub[0])) // 2
    draw.text((sx, int(420 * scale)), sub_text, fill=(226, 232, 240, 230), font=font_sub)

def render_round_card(size, symbols_spec):
    card = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    pad = int(size * 0.04)
    draw.ellipse([pad, pad, size - pad, size - pad], fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=int(size * 0.015))
    rim = pad + int(size * 0.02)
    draw.ellipse([rim, rim, size - rim, size - rim], fill=None, outline=(248, 250, 252, 255), width=int(size * 0.01))
    
    center = (size // 2, size // 2)
    radius = (size - 2 * pad) // 2
    
    for path, rx, ry, scale, rot in symbols_spec:
        if os.path.exists(path):
            sym = Image.open(path).convert("RGBA")
            tw = int(size * scale)
            th = int(sym.size[1] * (tw / sym.size[0]))
            sym = sym.resize((tw, th), Image.Resampling.LANCZOS)
            if rot != 0:
                sym = sym.rotate(rot, resample=Image.Resampling.BICUBIC, expand=True)
            px = int(center[0] + rx * radius - sym.size[0] / 2)
            py = int(center[1] + ry * radius - sym.size[1] / 2)
            card.paste(sym, (px, py), sym)
    
    return card

def add_card_shadow(canvas, card, pos):
    shadow_pad = 40
    card_w, card_h = card.size
    shadow = Image.new("RGBA", (card_w + shadow_pad * 2, card_h + shadow_pad * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([shadow_pad, shadow_pad, shadow_pad + card_w, shadow_pad + card_h], fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    canvas.paste(shadow, (pos[0] - shadow_pad, pos[1] - shadow_pad + 18), shadow)
    canvas.paste(card, pos, card)

def build_screenshot_duo(width, height, tag, title, sub, bg1, bg2, cards_data, extra_fn=None):
    img = create_gradient_bg(width, height, bg1, bg2)
    draw_header(img, width, tag, title, sub)
    scale = width / 2007.0

    # Draw central Duo fold visual line / subtle hinge indicator in middle
    hinge_y = int(height * 0.54)
    draw = ImageDraw.Draw(img)
    # Subtle duo seam glow
    draw.line([(int(width * 0.05), hinge_y), (int(width * 0.95), hinge_y)], fill=(255, 255, 255, 20), width=int(2 * scale))

    if cards_data:
        c1_spec, c2_spec, c1_rot, c2_rot = cards_data
        card_size = int(width * 0.44)
        c1 = render_round_card(card_size, c1_spec)
        c2 = render_round_card(card_size, c2_spec)

        if c1_rot != 0:
            c1 = c1.rotate(c1_rot, resample=Image.Resampling.BICUBIC, expand=False)
        if c2_rot != 0:
            c2 = c2.rotate(c2_rot, resample=Image.Resampling.BICUBIC, expand=False)

        spacing = int(width * 0.04)
        start_x = (width - (card_size * 2 + spacing)) // 2
        cards_y = int(height * 0.32)

        add_card_shadow(img, c1, (start_x, cards_y))
        add_card_shadow(img, c2, (start_x + card_size + spacing, cards_y))

    if extra_fn:
        extra_fn(img, width, height, scale)

    return img

print("Generating iPhone Duo Screenshots...")

# Shared symbol specs
web_dir = os.path.join(BASE_DIR, "web")
animals_c1 = [
    (os.path.join(web_dir, "animals/panda.png"), 0.0, 0.0, 0.38, 0),      # SHARED
    (os.path.join(web_dir, "animals/lion.png"), 0.6, -0.4, 0.28, 15),
    (os.path.join(web_dir, "animals/cat.png"), -0.6, -0.4, 0.26, -10),
    (os.path.join(web_dir, "animals/koala.png"), 0.5, 0.5, 0.27, -15),
    (os.path.join(web_dir, "animals/dog.png"), -0.5, 0.5, 0.28, 20),
    (os.path.join(web_dir, "animals/frog.png"), 0.0, -0.65, 0.25, 5),
    (os.path.join(web_dir, "animals/fox.png"), -0.7, 0.1, 0.25, -25),
    (os.path.join(web_dir, "animals/penguin.png"), 0.0, 0.65, 0.26, 10),
]

animals_c2 = [
    (os.path.join(web_dir, "animals/panda.png"), 0.45, -0.45, 0.38, -12), # SHARED
    (os.path.join(web_dir, "animals/tiger.png"), 0.0, 0.0, 0.32, 10),
    (os.path.join(web_dir, "animals/dolphin.png"), -0.5, -0.45, 0.27, 20),
    (os.path.join(web_dir, "animals/elephant.png"), 0.6, 0.3, 0.28, -8),
    (os.path.join(web_dir, "animals/rabbit.png"), -0.6, 0.3, 0.26, -18),
    (os.path.join(web_dir, "animals/unicorn.png"), 0.0, 0.65, 0.27, 5),
    (os.path.join(web_dir, "animals/monkey.png"), 0.0, -0.65, 0.25, -15),
    (os.path.join(web_dir, "animals/owl.png"), -0.65, -0.05, 0.25, 12),
]

# Fantasy C1/C2
fantasy_c1 = [
    (os.path.join(web_dir, "fantasy/dragon.png"), 0.0, 0.0, 0.38, 0),     # SHARED
    (os.path.join(web_dir, "fantasy/wizard.png"), 0.6, -0.4, 0.28, 15),
    (os.path.join(web_dir, "fantasy/castle.png"), -0.6, -0.4, 0.26, -10),
    (os.path.join(web_dir, "fantasy/phoenix.png"), 0.5, 0.5, 0.27, -15),
    (os.path.join(web_dir, "fantasy/potion.png"), -0.5, 0.5, 0.28, 20),
    (os.path.join(web_dir, "fantasy/sword.png"), 0.0, -0.65, 0.25, 5),
    (os.path.join(web_dir, "fantasy/magic_hat.png"), -0.7, 0.1, 0.25, -25),
    (os.path.join(web_dir, "fantasy/crystal_ball.png"), 0.0, 0.65, 0.26, 10),
]
fantasy_c2 = [
    (os.path.join(web_dir, "fantasy/dragon.png"), 0.45, -0.45, 0.38, -12),# SHARED
    (os.path.join(web_dir, "fantasy/unicorn.png"), 0.0, 0.0, 0.32, 10),
    (os.path.join(web_dir, "fantasy/crown.png"), -0.5, -0.45, 0.27, 20),
    (os.path.join(web_dir, "fantasy/spellbook.png"), 0.6, 0.3, 0.28, -8),
    (os.path.join(web_dir, "fantasy/shield.png"), -0.6, 0.3, 0.26, -18),
    (os.path.join(web_dir, "fantasy/hourglass.png"), 0.0, 0.65, 0.27, 5),
    (os.path.join(web_dir, "fantasy/magic_wand.png"), 0.0, -0.65, 0.25, -15),
    (os.path.join(web_dir, "fantasy/treasure_chest.png"), -0.65, -0.05, 0.25, 12),
]

# Ocean C1/C2
ocean_c1 = [
    (os.path.join(web_dir, "ocean/dolphin.png"), 0.0, 0.0, 0.38, 0),     # SHARED
    (os.path.join(web_dir, "ocean/shark.png"), 0.6, -0.4, 0.28, 15),
    (os.path.join(web_dir, "ocean/whale.png"), -0.6, -0.4, 0.26, -10),
    (os.path.join(web_dir, "ocean/turtle.png"), 0.5, 0.5, 0.27, -15),
    (os.path.join(web_dir, "ocean/octopus.png"), -0.5, 0.5, 0.28, 20),
    (os.path.join(web_dir, "ocean/seahorse.png"), 0.0, -0.65, 0.25, 5),
    (os.path.join(web_dir, "ocean/starfish.png"), -0.7, 0.1, 0.25, -25),
    (os.path.join(web_dir, "ocean/crab.png"), 0.0, 0.65, 0.26, 10),
]
ocean_c2 = [
    (os.path.join(web_dir, "ocean/dolphin.png"), 0.45, -0.45, 0.38, -12),# SHARED
    (os.path.join(web_dir, "ocean/coral.png"), 0.0, 0.0, 0.32, 10),
    (os.path.join(web_dir, "ocean/submarine.png"), -0.5, -0.45, 0.27, 20),
    (os.path.join(web_dir, "ocean/anchor.png"), 0.6, 0.3, 0.28, -8),
    (os.path.join(web_dir, "ocean/jellyfish.png"), -0.6, 0.3, 0.26, -18),
    (os.path.join(web_dir, "ocean/scuba.png"), 0.0, 0.65, 0.27, 5),
    (os.path.join(web_dir, "ocean/clownfish.png"), 0.0, -0.65, 0.25, -15),
    (os.path.join(web_dir, "ocean/manta_ray.png"), -0.65, -0.05, 0.25, 12),
]

def extra_tabletop_dock(img, width, height, scale):
    draw = ImageDraw.Draw(img)
    # Player 2 inverted buzzer banner
    p2_box = [int(width * 0.1), int(height * 0.68), int(width * 0.9), int(height * 0.77)]
    draw.rounded_rectangle(p2_box, radius=int(32 * scale), fill=(147, 51, 234, 230), outline=(255, 255, 255, 120), width=int(4 * scale))
    font_btn = get_font(int(60 * scale), bold=True)
    tb = draw.textbbox((0, 0), "🔄 PLAYER 2: ROTATED 180° TABLETOP DOCK", font=font_btn)
    bx = (width - (tb[2] - tb[0])) // 2
    by = p2_box[1] + (p2_box[3] - p2_box[1] - (tb[3] - tb[1])) // 2
    draw.text((bx, by), "🔄 PLAYER 2: ROTATED 180° TABLETOP DOCK", fill=(255, 255, 255), font=font_btn)

    # Player 1 standard buzzer banner
    p1_box = [int(width * 0.1), int(height * 0.81), int(width * 0.9), int(height * 0.90)]
    draw.rounded_rectangle(p1_box, radius=int(32 * scale), fill=(79, 70, 229, 230), outline=(255, 255, 255, 120), width=int(4 * scale))
    tb1 = draw.textbbox((0, 0), "⚡ PLAYER 1: TAP TO BUZZ IN & SPOT MATCH", font=font_btn)
    bx1 = (width - (tb1[2] - tb1[0])) // 2
    by1 = p1_box[1] + (p1_box[3] - p1_box[1] - (tb1[3] - tb1[1])) // 2
    draw.text((bx1, by1), "⚡ PLAYER 1: TAP TO BUZZ IN & SPOT MATCH", fill=(255, 255, 255), font=font_btn)

def extra_themes_banner(img, width, height, scale):
    draw = ImageDraw.Draw(img)
    theme_box = [int(width * 0.08), int(height * 0.72), int(width * 0.92), int(height * 0.88)]
    draw.rounded_rectangle(theme_box, radius=int(36 * scale), fill=(15, 23, 42, 210), outline=(255, 255, 255, 80), width=int(3 * scale))
    font_themes = get_font(int(48 * scale), bold=True)
    themes_str = "🐾 Animals • 🍕 Food • 🦸 Heroes • 🚀 Space • 🚗 Vehicles • 🧙 Fantasy • 🌊 Ocean"
    tb = draw.textbbox((0, 0), themes_str, font=font_themes)
    bx = (width - (tb[2] - tb[0])) // 2
    by = theme_box[1] + (theme_box[3] - theme_box[1] - (tb[3] - tb[1])) // 2
    draw.text((bx, by), themes_str, fill=(255, 255, 255), font=font_themes)

screens_config = [
    {
        "id": "01_duo_tabletop_mode",
        "tag": "IPHONE DUO • TABLETOP 1v1",
        "title": "Face-to-Face Dual Battle",
        "sub": "Fold in tent pose or lay flat on a table — cards rotate 180° for 2 players!",
        "bg1": (79, 70, 229), "bg2": (147, 51, 234),
        "cards": (animals_c1, animals_c2, 0, 180), # P2 rotated 180° for Tabletop!
        "extra": extra_tabletop_dock
    },
    {
        "id": "02_duo_7_vibrant_themes",
        "tag": "7 VIBRANT THEMES • 399 SYMBOLS",
        "title": "Endless Variety & Magic",
        "sub": "Animals, Food, Superheroes, Space, Vehicles, Fantasy, and Ocean World",
        "bg1": (13, 148, 136), "bg2": (15, 23, 42),
        "cards": (fantasy_c1, fantasy_c2, 0, 0),
        "extra": extra_themes_banner
    },
    {
        "id": "03_duo_math_proof",
        "tag": "FINITE PROJECTIVE PLANE PG(2, 7)",
        "title": "Always Exactly ONE Match",
        "sub": "57 cards, 8 symbols each. Spot the shared symbol before your opponent!",
        "bg1": (2, 132, 199), "bg2": (30, 41, 59),
        "cards": (ocean_c1, ocean_c2, 0, 0),
        "extra": None
    }
]

for cfg in screens_config:
    # 1. Inner Display (2007 x 2853)
    inner_img = build_screenshot_duo(
        W_INNER, H_INNER,
        cfg["tag"], cfg["title"], cfg["sub"],
        cfg["bg1"], cfg["bg2"],
        cfg["cards"], cfg["extra"]
    )
    inner_path = os.path.join(DUO_INNER_DIR, f"{cfg['id']}_inner_2007x2853.png")
    inner_img.save(inner_path, "PNG", optimize=True)
    shutil.copy(inner_path, os.path.join(DESKTOP_DIR, f"{cfg['id']}_inner_2007x2853.png"))
    print(f"  ✓ Saved Inner Display: {inner_path}")

    # 2. Outer Display (1398 x 2034)
    outer_img = build_screenshot_duo(
        W_OUTER, H_OUTER,
        cfg["tag"], cfg["title"], cfg["sub"],
        cfg["bg1"], cfg["bg2"],
        cfg["cards"], cfg["extra"]
    )
    outer_path = os.path.join(DUO_OUTER_DIR, f"{cfg['id']}_outer_1398x2034.png")
    outer_img.save(outer_path, "PNG", optimize=True)
    shutil.copy(outer_path, os.path.join(DESKTOP_DIR, f"{cfg['id']}_outer_1398x2034.png"))
    print(f"  ✓ Saved Outer Display: {outer_path}")

print("🎉 ALL IPHONE DUO SCREENSHOTS GENERATED SUCCESSFULLY!")
