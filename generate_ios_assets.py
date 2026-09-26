#!/usr/bin/env python3
"""
Generate professional App Icon (1024x1024) and Launch Splash screens (2732x2732)
for Spot The Chibi iOS App Store release.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "ios", "App", "App", "Assets.xcassets")
APP_ICON_PATH = os.path.join(ASSETS_DIR, "AppIcon.appiconset", "AppIcon-512@2x.png")
SPLASH_DIR = os.path.join(ASSETS_DIR, "Splash.imageset")

def create_gradient(width, height, start_color, end_color):
    """Create a smooth vertical/diagonal linear gradient."""
    base = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for y in range(height):
        t = y / float(height)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
        draw = ImageDraw.Draw(base)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    return base

def draw_circle_card(size, symbols_spec):
    """
    Renders a circular card on a transparent canvas of `size` x `size`.
    `symbols_spec`: list of (image_path, rel_x, rel_y, scale, angle_deg)
    """
    card_canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card_canvas)
    
    pad = int(size * 0.05)
    card_diam = size - 2 * pad
    center = (size // 2, size // 2)
    radius = card_diam // 2
    
    # Card base
    draw.ellipse([pad, pad, size - pad, size - pad], fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=int(size * 0.015))
    
    # Inner subtle rim
    rim_pad = pad + int(size * 0.02)
    draw.ellipse([rim_pad, rim_pad, size - rim_pad, size - rim_pad], fill=None, outline=(241, 245, 249, 255), width=int(size * 0.01))
    
    # Place symbols
    for path, rx, ry, scale, rot in symbols_spec:
        if os.path.exists(path):
            sym = Image.open(path).convert("RGBA")
            target_w = int(size * scale)
            target_h = int(sym.size[1] * (target_w / sym.size[0]))
            sym = sym.resize((target_w, target_h), Image.Resampling.LANCZOS)
            if rot != 0:
                sym = sym.rotate(rot, resample=Image.Resampling.BICUBIC, expand=True)
            
            # Position relative to center
            px = int(center[0] + rx * radius - sym.size[0] / 2)
            py = int(center[1] + ry * radius - sym.size[1] / 2)
            card_canvas.alpha_composite(sym, (px, py))
            
    return card_canvas

def create_app_icon():
    W, H = 1024, 1024
    print("Generating 1024x1024 App Icon...")
    
    # Rich modern gradient: Deep Royal Violet (#3730A3) to Radiant Indigo/Fuchsia (#6366F1 -> #8B5CF6)
    bg = create_gradient(W, H, (55, 48, 163), (139, 92, 246))
    
    # Add a subtle warm radial highlight in the center/upper portion
    highlight = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.ellipse([100, 50, W - 100, H - 200], fill=(255, 255, 255, 35))
    highlight = highlight.filter(ImageFilter.GaussianBlur(120))
    bg.alpha_composite(highlight)
    
    # Circular game cards
    card_dim = 560
    
    # Card 1: Back Card (Top-Left tilted)
    # Symbols: Panda, Star, Lion, Rocket
    panda_path = os.path.join(BASE_DIR, "web", "animals", "panda.png")
    star_path = os.path.join(BASE_DIR, "web", "space", "star.png")
    lion_path = os.path.join(BASE_DIR, "web", "animals", "lion.png")
    rocket_path = os.path.join(BASE_DIR, "web", "space", "rocket.png")
    pizza_path = os.path.join(BASE_DIR, "web", "food", "pizza.png")
    lightning_path = os.path.join(BASE_DIR, "web", "heroes", "lightning.png")
    
    card1_symbols = [
        (panda_path, 0.15, -0.15, 0.40, 10),      # The matching panda!
        (star_path, -0.45, -0.35, 0.28, -15),
        (lion_path, -0.35, 0.35, 0.30, 8),
        (rocket_path, 0.40, 0.35, 0.28, 25)
    ]
    card1_img = draw_circle_card(card_dim, card1_symbols)
    card1_rot = card1_img.rotate(14, resample=Image.Resampling.BICUBIC, expand=True)
    
    # Card 1 Drop Shadow
    c1_shadow = Image.new("RGBA", card1_rot.size, (0, 0, 0, 0))
    c1_alpha = card1_rot.split()[3]
    c1_shadow.paste((15, 10, 50, 140), (0, 0), mask=c1_alpha)
    c1_shadow = c1_shadow.filter(ImageFilter.GaussianBlur(24))
    
    # Position Card 1
    c1_pos = (120, 100)
    bg.alpha_composite(c1_shadow, (c1_pos[0] + 10, c1_pos[1] + 25))
    bg.alpha_composite(card1_rot, c1_pos)
    
    # Card 2: Front Card (Bottom-Right tilted)
    # Symbols: Panda (match!), Lightning, Pizza, Gem/Heart
    card2_symbols = [
        (panda_path, -0.22, 0.10, 0.46, -8),     # The matching panda, larger!
        (lightning_path, 0.38, -0.32, 0.32, 12),
        (pizza_path, -0.35, -0.38, 0.30, -18),
        (star_path, 0.35, 0.38, 0.26, 30)
    ]
    card2_img = draw_circle_card(card_dim, card2_symbols)
    card2_rot = card2_img.rotate(-10, resample=Image.Resampling.BICUBIC, expand=True)
    
    # Card 2 Drop Shadow
    c2_shadow = Image.new("RGBA", card2_rot.size, (0, 0, 0, 0))
    c2_alpha = card2_rot.split()[3]
    c2_shadow.paste((10, 8, 40, 170), (0, 0), mask=c2_alpha)
    c2_shadow = c2_shadow.filter(ImageFilter.GaussianBlur(32))
    
    # Position Card 2
    c2_pos = (340, 340)
    bg.alpha_composite(c2_shadow, (c2_pos[0] + 12, c2_pos[1] + 35))
    bg.alpha_composite(card2_rot, c2_pos)
    
    # Add sparkling particle bursts near the matching pandas
    sparkles = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sparkles)
    
    def draw_star_burst(cx, cy, r_outer, r_inner, color):
        points = []
        for i in range(8):
            angle = i * math.pi / 4
            r = r_outer if i % 2 == 0 else r_inner
            points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        sdraw.polygon(points, fill=color)
        
    draw_star_burst(470, 370, 24, 8, (255, 230, 0, 240))
    draw_star_burst(440, 330, 14, 5, (255, 255, 255, 220))
    draw_star_burst(530, 390, 16, 6, (255, 215, 0, 200))
    draw_star_burst(880, 180, 20, 7, (255, 255, 255, 180))
    draw_star_burst(160, 780, 18, 6, (255, 230, 120, 190))
    
    bg.alpha_composite(sparkles)
    
    # Apple App Store strictly requires NO alpha channel (RGB format)
    rgb_icon = Image.new("RGB", (W, H), (55, 48, 163))
    rgb_icon.paste(bg, (0, 0), mask=bg.split()[3])
    
    os.makedirs(os.path.dirname(APP_ICON_PATH), exist_ok=True)
    rgb_icon.save(APP_ICON_PATH, "PNG", quality=100)
    print(f"App Icon saved successfully to {APP_ICON_PATH}")

def create_splash_screens():
    W, H = 2732, 2732
    print("Generating 2732x2732 Splash Screen...")
    
    # Clean warm off-white background (#F8FAFC)
    splash = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(splash)
    
    # Large centered circular hero card with Panda
    card_dim = 1100
    card_pad = 60
    card_center = (W // 2, H // 2 - 160)
    
    # Shadow
    shadow = Image.new("RGBA", (card_dim, card_dim), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([card_pad, card_pad, card_dim - card_pad, card_dim - card_pad], fill=(15, 23, 42, 45))
    shadow = shadow.filter(ImageFilter.GaussianBlur(40))
    splash.alpha_composite(shadow, (card_center[0] - card_dim // 2, card_center[1] - card_dim // 2 + 30))
    
    # Card surface
    card = Image.new("RGBA", (card_dim, card_dim), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.ellipse([card_pad, card_pad, card_dim - card_pad, card_dim - card_pad], fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=18)
    
    # Place Panda inside
    panda_path = os.path.join(BASE_DIR, "web", "animals", "panda.png")
    if os.path.exists(panda_path):
        panda = Image.open(panda_path).convert("RGBA")
        p_size = 620
        panda = panda.resize((p_size, p_size), Image.Resampling.LANCZOS)
        card.alpha_composite(panda, (card_dim // 2 - p_size // 2, card_dim // 2 - p_size // 2))
        
    splash.alpha_composite(card, (card_center[0] - card_dim // 2, card_center[1] - card_dim // 2))
    
    # Text: "Spot The Chibi"
    font_title = None
    font_sub = None
    for fpath in ["/System/Library/Fonts/SFCompact.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(fpath):
            try:
                font_title = ImageFont.truetype(fpath, 130)
                font_sub = ImageFont.truetype(fpath, 54)
                break
            except Exception:
                continue
                
    if font_title:
        title_text = "Spot The Chibi"
        bbox = draw.textbbox((0, 0), title_text, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, card_center[1] + card_dim // 2 + 80), title_text, fill=(30, 41, 59, 255), font=font_title)
        
        sub_text = "57-Symbol Matching Party Game"
        sbox = draw.textbbox((0, 0), sub_text, font=font_sub)
        sw = sbox[2] - sbox[0]
        draw.text(((W - sw) // 2, card_center[1] + card_dim // 2 + 240), sub_text, fill=(100, 116, 139, 255), font=font_sub)

    # Save to all 3 Splash image slots
    os.makedirs(SPLASH_DIR, exist_ok=True)
    rgb_splash = splash.convert("RGB")
    for name in ["splash-2732x2732.png", "splash-2732x2732-1.png", "splash-2732x2732-2.png"]:
        out_p = os.path.join(SPLASH_DIR, name)
        rgb_splash.save(out_p, "PNG")
        print(f"Splash screen saved to {out_p}")

if __name__ == "__main__":
    create_app_icon()
    create_splash_screens()
    print("All iOS App Store assets created successfully!")
