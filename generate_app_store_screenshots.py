#!/usr/bin/env python3
"""
Generate professional 6.7" App Store Screenshots (1290 x 2796 px)
and export high-res App Store Icon (1024 x 1024 px) for Spot The Chibi.
"""
import math
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "AppStore_Assets")
SCREENSHOTS_DIR = os.path.join(OUTPUT_DIR, "Screenshots_6.7_inch")
DESKTOP_DIR = os.path.expanduser("~/Desktop/Spot_The_Chibi_AppStore_Assets")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(DESKTOP_DIR, exist_ok=True)

# 1. Export 1024x1024 App Store Icon
icon_src = os.path.join(BASE_DIR, "ios", "App", "App", "Assets.xcassets", "AppIcon.appiconset", "AppIcon-512@2x.png")
icon_dest = os.path.join(OUTPUT_DIR, "AppStore_Icon_1024x1024.png")
if os.path.exists(icon_src):
    shutil.copy(icon_src, icon_dest)
    shutil.copy(icon_src, os.path.join(DESKTOP_DIR, "AppStore_Icon_1024x1024.png"))
    print("Exported 1024x1024 App Store Icon.")

W, H = 1290, 2796

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

def create_gradient_bg(c1, c2):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        t = y / float(H)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw = ImageDraw.Draw(img)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
    return img

def draw_header(canvas, tag_text, title_text, sub_text, text_color=(255, 255, 255)):
    draw = ImageDraw.Draw(canvas)
    
    # Pill Tag
    font_tag = get_font(36, bold=True)
    tb = draw.textbbox((0, 0), tag_text, font=font_tag)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]
    px = (W - tw) // 2
    py = 180
    pad_x, pad_y = 28, 14
    draw.rounded_rectangle([px - pad_x, py - pad_y, px + tw + pad_x, py + th + pad_y], radius=24, fill=(255, 255, 255, 40), outline=(255, 255, 255, 80), width=3)
    draw.text((px, py - 4), tag_text, fill=(255, 255, 255, 240), font=font_tag)
    
    # Title
    font_title = get_font(76, bold=True)
    tb_title = draw.textbbox((0, 0), title_text, font=font_title)
    tx = (W - (tb_title[2] - tb_title[0])) // 2
    draw.text((tx, 270), title_text, fill=text_color, font=font_title)
    
    # Subtitle
    font_sub = get_font(38, bold=False)
    tb_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    sx = (W - (tb_sub[2] - tb_sub[0])) // 2
    draw.text((sx, 375), sub_text, fill=(226, 232, 240, 220), font=font_sub)

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
            card.alpha_composite(sym, (px, py))
    return card

# Helper paths
PANDA = os.path.join(BASE_DIR, "web", "animals", "panda.png")
LION = os.path.join(BASE_DIR, "web", "animals", "lion.png")
STAR = os.path.join(BASE_DIR, "web", "space", "star.png")
ROCKET = os.path.join(BASE_DIR, "web", "space", "rocket.png")
PIZZA = os.path.join(BASE_DIR, "web", "food", "pizza.png")
BURGER = os.path.join(BASE_DIR, "web", "food", "burger.png")
LIGHTNING = os.path.join(BASE_DIR, "web", "heroes", "lightning.png")
SHIELD = os.path.join(BASE_DIR, "web", "heroes", "shield.png")
CAR = os.path.join(BASE_DIR, "web", "vehicles", "racing_car.png")
PLANE = os.path.join(BASE_DIR, "web", "vehicles", "airplane.png")

# SCREENSHOT 1: "SPOT THE MATCH!"
def gen_ss1():
    print("Generating Screenshot 1: Spot The Match...")
    bg = create_gradient_bg((30, 27, 75), (79, 70, 229))
    draw_header(bg, "FAST-PACED MATCHING", "Spot The Common Symbol!", "Every 2 cards have exactly 1 match in common.")
    
    # Render two large cards
    card_dim = 620
    c1_symbols = [
        (PANDA, 0.1, -0.15, 0.44, 8),
        (STAR, -0.42, -0.32, 0.32, -15),
        (LION, -0.35, 0.35, 0.34, 10),
        (BURGER, 0.40, 0.35, 0.30, 20),
        (LIGHTNING, 0.0, 0.42, 0.28, -8)
    ]
    c2_symbols = [
        (PANDA, -0.18, 0.12, 0.48, -12),
        (ROCKET, 0.38, -0.30, 0.34, 15),
        (PIZZA, -0.38, -0.38, 0.32, -22),
        (CAR, 0.35, 0.36, 0.32, 28),
        (SHIELD, 0.0, -0.42, 0.28, 5)
    ]
    card1 = render_round_card(card_dim, c1_symbols)
    card2 = render_round_card(card_dim, c2_symbols)
    
    # Shadow and paste Card 1
    s1 = Image.new("RGBA", (card_dim, card_dim), (0, 0, 0, 0))
    s1.paste((10, 15, 40, 150), (0, 0), mask=card1.split()[3])
    s1 = s1.filter(ImageFilter.GaussianBlur(30))
    pos1 = ((W - card_dim) // 2, 540)
    bg.alpha_composite(s1, (pos1[0], pos1[1] + 20))
    bg.alpha_composite(card1, pos1)
    
    # VS Badge
    vs_dim = 140
    vs = Image.new("RGBA", (vs_dim, vs_dim), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vs)
    vdraw.ellipse([0, 0, vs_dim, vs_dim], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=8)
    vfont = get_font(52, bold=True)
    vdraw.text((32, 40), "VS", fill=(255, 255, 255), font=vfont)
    bg.alpha_composite(vs, ((W - vs_dim) // 2, 1150))
    
    # Shadow and paste Card 2
    s2 = Image.new("RGBA", (card_dim, card_dim), (0, 0, 0, 0))
    s2.paste((10, 15, 40, 150), (0, 0), mask=card2.split()[3])
    s2 = s2.filter(ImageFilter.GaussianBlur(30))
    pos2 = ((W - card_dim) // 2, 1280)
    bg.alpha_composite(s2, (pos2[0], pos2[1] + 20))
    bg.alpha_composite(card2, pos2)
    
    # Bottom callout pill: "TAP THE MATCHING PANDA!"
    draw = ImageDraw.Draw(bg)
    font_call = get_font(42, bold=True)
    call_text = "MATCH: PANDA!"
    cb = draw.textbbox((0, 0), call_text, font=font_call)
    cw = cb[2] - cb[0]
    ch = cb[3] - cb[1]
    c_px = (W - cw) // 2
    c_py = 2060
    draw.rounded_rectangle([c_px - 40, c_py - 20, c_px + cw + 40, c_py + ch + 20], radius=32, fill=(16, 185, 129, 255), outline=(255, 255, 255, 255), width=4)
    draw.text((c_px, c_py - 4), call_text, fill=(255, 255, 255), font=font_call)
    
    out_p = os.path.join(SCREENSHOTS_DIR, "1_Spot_The_Match.png")
    bg.convert("RGB").save(out_p, "PNG")
    shutil.copy(out_p, os.path.join(DESKTOP_DIR, "1_Spot_The_Match.png"))

# SCREENSHOT 2: "5 VIBRANT THEMES"
def gen_ss2():
    print("Generating Screenshot 2: 5 Rich Themes...")
    bg = create_gradient_bg((15, 23, 42), (59, 130, 246))
    draw_header(bg, "5 RICH THEMES", "Endless Variety & Fun", "Animals, Food, Superheroes, Space & Vehicles.")
    
    themes = [
        ("Animals", PANDA, (244, 63, 94)),
        ("Food", PIZZA, (249, 115, 22)),
        ("Heroes", LIGHTNING, (168, 85, 247)),
        ("Space", ROCKET, (99, 102, 241)),
        ("Vehicles", CAR, (16, 185, 129))
    ]
    
    start_y = 520
    row_h = 290
    card_w = 1050
    draw = ImageDraw.Draw(bg)
    
    for i, (name, icon_p, color) in enumerate(themes):
        ry = start_y + i * row_h
        rx = (W - card_w) // 2
        # Row card
        draw.rounded_rectangle([rx, ry, rx + card_w, ry + 240], radius=36, fill=(255, 255, 255, 230), outline=(255, 255, 255, 255), width=4)
        
        # Icon
        if os.path.exists(icon_p):
            im = Image.open(icon_p).convert("RGBA").resize((180, 180), Image.Resampling.LANCZOS)
            bg.alpha_composite(im, (rx + 40, ry + 30))
            
        # Title
        font_th = get_font(56, bold=True)
        draw.text((rx + 260, ry + 60), name, fill=(15, 23, 42), font=font_th)
        
        # 57 Symbols Badge
        font_badge = get_font(32, bold=True)
        draw.rounded_rectangle([rx + 260, ry + 135, rx + 490, ry + 185], radius=18, fill=color)
        draw.text((rx + 280, ry + 142), "57 Symbols", fill=(255, 255, 255), font=font_badge)
        
    out_p = os.path.join(SCREENSHOTS_DIR, "2_Five_Rich_Themes.png")
    bg.convert("RGB").save(out_p, "PNG")
    shutil.copy(out_p, os.path.join(DESKTOP_DIR, "2_Five_Rich_Themes.png"))

# SCREENSHOT 3: "SOLO TIME ATTACK"
def gen_ss3():
    print("Generating Screenshot 3: Solo Time Attack...")
    bg = create_gradient_bg((67, 20, 7), (234, 88, 12))
    draw_header(bg, "EXCITING GAME MODES", "Solo Time Attack Race!", "10 fast-paced matches with live millisecond timer.")
    
    draw = ImageDraw.Draw(bg)
    
    # Big Rank Badge
    rx = (W - 800) // 2
    ry = 540
    draw.rounded_rectangle([rx, ry, rx + 800, ry + 560], radius=48, fill=(255, 255, 255, 240), outline=(254, 215, 170, 255), width=6)
    
    # Grade S+
    font_grade = get_font(180, bold=True)
    draw.text((rx + 180, ry + 40), "S+", fill=(234, 88, 12), font=font_grade)
    
    # Rank Title
    font_rt = get_font(52, bold=True)
    draw.text((rx + 110, ry + 270), "LIGHTNING MASTER!", fill=(15, 23, 42), font=font_rt)
    
    # Time
    font_time = get_font(68, bold=True)
    draw.text((rx + 220, ry + 360), "14.82s", fill=(79, 70, 229), font=font_time)
    
    # Best Record Tag
    font_rec = get_font(34, bold=True)
    draw.rounded_rectangle([rx + 240, ry + 465, rx + 560, ry + 515], radius=16, fill=(16, 185, 129))
    draw.text((rx + 265, ry + 472), "NEW BEST RECORD!", fill=(255, 255, 255), font=font_rec)
    
    # Mode cards below
    modes = [
        ("⏱️ Solo Time Attack", "10-round sprint against the clock"),
        ("🃏 57-Card Deck Run", "Full projective deck without repeats"),
        ("👥 2-Player Versus", "Head-to-head live point battle")
    ]
    my = 1200
    for title, desc in modes:
        draw.rounded_rectangle([rx, my, rx + 800, my + 180], radius=32, fill=(255, 255, 255, 220))
        draw.text((rx + 40, my + 35), title, fill=(15, 23, 42), font=get_font(48, bold=True))
        draw.text((rx + 40, my + 105), desc, fill=(100, 116, 139), font=get_font(34, bold=False))
        my += 220

    out_p = os.path.join(SCREENSHOTS_DIR, "3_Solo_Time_Attack.png")
    bg.convert("RGB").save(out_p, "PNG")
    shutil.copy(out_p, os.path.join(DESKTOP_DIR, "3_Solo_Time_Attack.png"))

# SCREENSHOT 4: "PRINTABLE PDF CARDS INCLUDED"
def gen_ss4():
    print("Generating Screenshot 4: Printable Cards Included...")
    bg = create_gradient_bg((6, 78, 59), (16, 185, 129))
    draw_header(bg, "PHYSICAL PARTY PLAY", "Printable Cards Included!", "Print full duplex A4 card decks directly from the app.")
    
    draw = ImageDraw.Draw(bg)
    rx = (W - 900) // 2
    ry = 540
    
    # Big Paper Sheet Mockup
    draw.rounded_rectangle([rx, ry, rx + 900, ry + 1100], radius=40, fill=(255, 255, 255, 255), outline=(226, 232, 240), width=6)
    
    # Sheet Header
    draw.text((rx + 70, ry + 60), "🖨️ A4 Duplex Print Ready", fill=(15, 23, 42), font=get_font(52, bold=True))
    draw.text((rx + 70, ry + 130), "6 Round Cards Per Sheet • Dual Sided", fill=(100, 116, 139), font=get_font(34, bold=False))
    
    # Mini cards on sheet
    grid_start_y = ry + 210
    card_mini_dim = 230
    for row in range(3):
        for col in range(2):
            cx = rx + 140 + col * 360
            cy = grid_start_y + row * 270
            draw.ellipse([cx, cy, cx + card_mini_dim, cy + card_mini_dim], fill=(248, 250, 252), outline=(203, 213, 225), width=4)
            # Add center icon
            ic = [PANDA, PIZZA, STAR, ROCKET, CAR, LIGHTNING][row * 2 + col]
            if os.path.exists(ic):
                im = Image.open(ic).convert("RGBA").resize((120, 120), Image.Resampling.LANCZOS)
                bg.alpha_composite(im, (cx + 55, cy + 55))
                
    # Bottom callout
    font_call = get_font(42, bold=True)
    call_text = "5 COMPLETE PDF DECKS INCLUDED"
    cb = draw.textbbox((0, 0), call_text, font=font_call)
    cw = cb[2] - cb[0]
    ch = cb[3] - cb[1]
    c_px = (W - cw) // 2
    c_py = 1800
    draw.rounded_rectangle([c_px - 40, c_py - 20, c_px + cw + 40, c_py + ch + 20], radius=32, fill=(255, 255, 255), outline=(16, 185, 129), width=4)
    draw.text((c_px, c_py - 4), call_text, fill=(6, 78, 59), font=font_call)
    
    out_p = os.path.join(SCREENSHOTS_DIR, "4_Printable_PDF_Cards.png")
    bg.convert("RGB").save(out_p, "PNG")
    shutil.copy(out_p, os.path.join(DESKTOP_DIR, "4_Printable_PDF_Cards.png"))

if __name__ == "__main__":
    gen_ss1()
    gen_ss2()
    gen_ss3()
    gen_ss4()
    print("All App Store screenshots generated successfully in AppStore_Assets and copied to Desktop!")
