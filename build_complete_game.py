
import textwrap

def draw_rules_page(c):
    c.saveState()
    PAGE_W, PAGE_H = A4
    
    # Header Banner
    c.setFillColor(colors.HexColor("#FFF7ED"))
    c.roundRect(14*mm, PAGE_H - 42*mm, PAGE_W - 28*mm, 28*mm, 4*mm, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#FDBA74"))
    c.setLineWidth(1)
    c.roundRect(14*mm, PAGE_H - 42*mm, PAGE_W - 28*mm, 28*mm, 4*mm, fill=0, stroke=1)
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#C2410C"))
    c.drawCentredString(PAGE_W / 2.0, PAGE_H - 24*mm, "CHIBI ANIMAL SPOT IT! • GAME RULES")
    
    # Subtitle
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#7C2D12"))
    c.drawCentredString(PAGE_W / 2.0, PAGE_H - 31*mm, "57 Cards • 57 Adorable Animals • 8 Animals Per Card • Exactly 1 Match Between Any 2 Cards")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#9A3412"))
    c.drawCentredString(PAGE_W / 2.0, PAGE_H - 37*mm, "2 to 8 Players  |  Ages 4 to Adult  |  10 - 15 Minutes  |  Party & Family Card Game")
    
    # The Golden Rule Box
    box_y = PAGE_H - 64*mm
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.roundRect(14*mm, box_y, PAGE_W - 28*mm, 18*mm, 3*mm, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#93C5FD"))
    c.setLineWidth(0.8)
    c.roundRect(14*mm, box_y, PAGE_W - 28*mm, 18*mm, 3*mm, fill=0, stroke=1)
    
    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(colors.HexColor("#1D4ED8"))
    c.drawString(18*mm, box_y + 11.5*mm, "★ THE GOLDEN RULE OF THE GAME:")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(18*mm, box_y + 6*mm, "Between any two cards in this deck, there is ALWAYS exactly ONE matching animal (same species & color,")
    c.drawString(18*mm, box_y + 2*mm, "though its size and orientation may vary). Be the first to spot it, shout its name out loud, and make your move!")
    
    # 5 Mini-Games Section
    c.setFont("Helvetica-Bold", 12.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(14*mm, PAGE_H - 71.5*mm, "5 Exciting Ways to Play (Mini-Games)")
    
    games = [
        ("1. THE TOWER (Fill your hand)", 
         "Goal: Collect the most cards.",
         "Setup: Shuffle deck. Deal 1 card face down to each player. Place remaining deck face up in center (The Tower).",
         "Play: All flip cards face up together. Race to spot matching animal between your card and Tower. Shout match and take center card onto your pile! New card is now in play. Continue until empty! Most cards wins!"),
        
        ("2. THE WELL (Empty your hand)", 
         "Goal: Be first to empty your hand.",
         "Setup: Place 1 card face up in center (The Well). Deal all remaining cards equally among players face down.",
         "Play: Flip personal decks face up. Spot match between your top card and center Well card. Shout animal and discard your card on top of Well! Your next card is now exposed. First to empty stack wins!"),
         
        ("3. HOT POTATO (Pass the penalty)", 
         "Goal: Avoid holding cards at round end.",
         "Setup: Deal 1 card face down to each player each mini-round. Set rest of deck aside.",
         "Play: Flip cards face up onto open palm. Spot match with ANY opponent card, shout animal and place your card ON TOP of theirs! They must match new top card to pass pile! Last holding cards loses."),
         
        ("4. THE POISONED GIFT (Help or hinder)", 
         "Goal: Have the fewest cards at end.",
         "Setup: Deal 1 card face down to each player. Place remaining deck face up in center.",
         "Play: Flip cards over. Spot match between center card and ANY rival top card. Shout animal and give center card to them! When center deck runs out, player with fewest cards wins!"),
         
        ("5. TRIPLE SPOT (Grand vision challenge)", 
         "Goal: Spot matching triplets in a grid.",
         "Setup: Deal 9 cards face up on table in a 3x3 grid. Keep remainder of deck nearby.",
         "Play: All search simultaneously for ANY 3 cards sharing the exact same animal. First to spot triplet shouts animal, shows all 3 cards, and claims them! Deal 3 new cards. Most cards wins!")
    ]

    cur_y = PAGE_H - 77.5*mm
    for title, goal, setup, play in games:
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(14*mm, cur_y - 23.5*mm, PAGE_W - 28*mm, 23.5*mm, 2.5*mm, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.6)
        c.roundRect(14*mm, cur_y - 23.5*mm, PAGE_W - 28*mm, 23.5*mm, 2.5*mm, fill=0, stroke=1)
        
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(colors.HexColor("#0284C7"))
        c.drawString(17*mm, cur_y - 4.5*mm, title)
        
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#047857"))
        c.drawRightString(PAGE_W - 17*mm, cur_y - 4.5*mm, goal)
        
        c.setFont("Helvetica", 7.2)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawString(17*mm, cur_y - 9.5*mm, setup)
        
        lines = textwrap.wrap(play, width=120)
        if len(lines) >= 1:
            c.drawString(17*mm, cur_y - 14.5*mm, lines[0])
        if len(lines) >= 2:
            c.drawString(17*mm, cur_y - 19.0*mm, lines[1])
            
        cur_y -= 26.5*mm
        
    tip_box_y = 11*mm
    c.setFillColor(colors.HexColor("#FEFCE8"))
    c.roundRect(14*mm, tip_box_y, PAGE_W - 28*mm, 20*mm, 3*mm, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#FEF08A"))
    c.setLineWidth(0.8)
    c.roundRect(14*mm, tip_box_y, PAGE_W - 28*mm, 20*mm, 3*mm, fill=0, stroke=1)
    
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#854D0E"))
    c.drawString(18*mm, tip_box_y + 14*mm, "✂ PRINTING & ASSEMBLY INSTRUCTIONS:")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#713F12"))
    c.drawString(18*mm, tip_box_y + 9.5*mm, "• Recommended Paper: Print on thick paper or cardstock (200 - 300 gsm) or laminate for extra durability and smooth shuffling.")
    c.drawString(18*mm, tip_box_y + 5.5*mm, "• Cutting: Cut out each circle using scissors or an 84mm (3.3-inch) circle punch. Alternatively, use a straight paper trimmer along the corner crop guides.")
    c.drawString(18*mm, tip_box_y + 1.5*mm, "• Double-Sided Option: Print the optional Card Backs PDF on the reverse side of Pages 1-10 (select 'Flip on Long Edge' in your printer settings).")
    
    c.restoreState()

def draw_visual_key_page(c):
    c.saveState()
    PAGE_W, PAGE_H = A4
    
    # Header Banner
    c.setFillColor(colors.HexColor("#F0FDF4"))
    c.roundRect(14*mm, PAGE_H - 32*mm, PAGE_W - 28*mm, 20*mm, 3*mm, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#86EFAC"))
    c.setLineWidth(1)
    c.roundRect(14*mm, PAGE_H - 32*mm, PAGE_W - 28*mm, 20*mm, 3*mm, fill=0, stroke=1)
    
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#15803D"))
    c.drawCentredString(PAGE_W / 2.0, PAGE_H - 20*mm, "THE 57 CHIBI ANIMALS • VISUAL KEY & CHECKLIST")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#166534"))
    c.drawCentredString(PAGE_W / 2.0, PAGE_H - 26.5*mm, "Official visual naming guide to resolve any disputed calls during fast-paced gameplay!")
    
    cols = 6
    rows = 10
    col_w = (PAGE_W - 28*mm) / cols
    row_h = 24.2*mm
    start_y = PAGE_H - 36*mm
    start_x = 14*mm
    
    for idx, a in enumerate(ANIMALS):
        r = idx // cols
        col = idx % cols
        
        cell_x = start_x + col * col_w
        cell_y = start_y - (r + 1) * row_h
        
        # Soft card box
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.roundRect(cell_x + 1*mm, cell_y + 1*mm, col_w - 2*mm, row_h - 2*mm, 2*mm, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.5)
        c.roundRect(cell_x + 1*mm, cell_y + 1*mm, col_w - 2*mm, row_h - 2*mm, 2*mm, fill=0, stroke=1)
        
        # Index badge
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor("#94A3B8"))
        c.drawString(cell_x + 2.5*mm, cell_y + row_h - 5.5*mm, f"#{idx+1}")
        
        # Animal icon
        icon_path = os.path.join("chibi_animals", f"{a['slug']}.png")
        if os.path.exists(icon_path):
            icon_size = 14*mm
            ix = cell_x + (col_w - icon_size) / 2.0
            iy = cell_y + 5.5*mm
            c.drawImage(icon_path, ix, iy, width=icon_size, height=icon_size, mask='auto')
            
        # Animal name
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#1E293B"))
        c.drawCentredString(cell_x + col_w / 2.0, cell_y + 2.2*mm, a['name'])
        
    # Last 3 slots (indices 57, 58, 59)
    box_x = start_x + 3 * col_w + 1*mm
    box_y = start_y - 10 * row_h + 1*mm
    box_w = 3 * col_w - 2*mm
    box_h = row_h - 2*mm
    
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.roundRect(box_x, box_y, box_w, box_h, 2*mm, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.6)
    c.roundRect(box_x, box_y, box_w, box_h, 2*mm, fill=0, stroke=1)
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawCentredString(box_x + box_w/2.0, box_y + box_h - 5.5*mm, "MATHEMATICALLY PERFECT DESIGN")
    
    c.setFont("Helvetica", 6.8)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawCentredString(box_x + box_w/2.0, box_y + box_h - 10.5*mm, "Finite Projective Plane PG(2, 7) • 57 Cards • 57 Symbols")
    c.drawCentredString(box_x + box_w/2.0, box_y + box_h - 15*mm, "Every pair of cards intersects at exactly ONE animal symbol.")
    c.drawCentredString(box_x + box_w/2.0, box_y + box_h - 19.5*mm, "Total combinations: 1,596 unique card pairs verified!")
    
    # Bottom footnote
    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawCentredString(PAGE_W / 2.0, 7*mm, "Chibi Animal Spot It! • Printable A4 Edition • High Resolution Vector / 300+ DPI")
    
    c.restoreState()


import os
import math
import random
import time
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ---------------------------------------------------------------------------
# 1. Animal Metadata (57 distinct chibi animals)
# ---------------------------------------------------------------------------
ANIMALS = [
    {"slug": "cat", "name": "Cat"},
    {"slug": "dog", "name": "Dog"},
    {"slug": "fox", "name": "Fox"},
    {"slug": "bear", "name": "Bear"},
    {"slug": "panda", "name": "Panda"},
    {"slug": "koala", "name": "Koala"},
    {"slug": "lion", "name": "Lion"},
    {"slug": "tiger", "name": "Tiger"},
    {"slug": "frog", "name": "Frog"},
    {"slug": "monkey", "name": "Monkey"},
    {"slug": "pig", "name": "Pig"},
    {"slug": "cow", "name": "Cow"},
    {"slug": "mouse", "name": "Mouse"},
    {"slug": "rabbit", "name": "Rabbit"},
    {"slug": "hamster", "name": "Hamster"},
    {"slug": "wolf", "name": "Wolf"},
    {"slug": "hedgehog", "name": "Hedgehog"},
    {"slug": "otter", "name": "Otter"},
    {"slug": "sloth", "name": "Sloth"},
    {"slug": "beaver", "name": "Beaver"},
    {"slug": "bat", "name": "Bat"},
    {"slug": "owl", "name": "Owl"},
    {"slug": "penguin", "name": "Penguin"},
    {"slug": "duck", "name": "Duck"},
    {"slug": "rooster", "name": "Rooster"},
    {"slug": "parrot", "name": "Parrot"},
    {"slug": "flamingo", "name": "Flamingo"},
    {"slug": "peacock", "name": "Peacock"},
    {"slug": "crocodile", "name": "Crocodile"},
    {"slug": "turtle", "name": "Turtle"},
    {"slug": "lizard", "name": "Lizard"},
    {"slug": "snake", "name": "Snake"},
    {"slug": "octopus", "name": "Octopus"},
    {"slug": "squid", "name": "Squid"},
    {"slug": "crab", "name": "Crab"},
    {"slug": "dolphin", "name": "Dolphin"},
    {"slug": "whale", "name": "Whale"},
    {"slug": "shark", "name": "Shark"},
    {"slug": "seal", "name": "Seal"},
    {"slug": "tropical_fish", "name": "Tropical Fish"},
    {"slug": "blowfish", "name": "Blowfish"},
    {"slug": "jellyfish", "name": "Jellyfish"},
    {"slug": "bee", "name": "Bee"},
    {"slug": "butterfly", "name": "Butterfly"},
    {"slug": "ladybug", "name": "Ladybug"},
    {"slug": "snail", "name": "Snail"},
    {"slug": "giraffe", "name": "Giraffe"},
    {"slug": "elephant", "name": "Elephant"},
    {"slug": "rhino", "name": "Rhino"},
    {"slug": "hippo", "name": "Hippo"},
    {"slug": "zebra", "name": "Zebra"},
    {"slug": "deer", "name": "Deer"},
    {"slug": "horse", "name": "Horse"},
    {"slug": "unicorn", "name": "Unicorn"},
    {"slug": "llama", "name": "Llama"},
    {"slug": "kangaroo", "name": "Kangaroo"},
    {"slug": "gorilla", "name": "Gorilla"},
]

assert len(ANIMALS) == 57

# ---------------------------------------------------------------------------
# 2. Mathematical Generator PG(2, 7)
# ---------------------------------------------------------------------------
def generate_projective_plane():
    p = 7
    cards = []
    # 49 affine lines
    for m in range(p):
        for c in range(p):
            card = []
            for x in range(p):
                card.append(x * p + ((m * x + c) % p))
            card.append(p * p + m)
            cards.append(card)
    # 7 vertical lines
    for c in range(p):
        card = []
        for y in range(p):
            card.append(c * p + y)
        card.append(p * p + p)
        cards.append(card)
    # 1 line at infinity
    card = []
    for m in range(p):
        card.append(p * p + m)
    card.append(p * p + p)
    cards.append(card)
    
    # Rigorous verification
    assert len(cards) == 57
    for i in range(57):
        assert len(cards[i]) == 8
        assert len(set(cards[i])) == 8
        for j in range(i + 1, 57):
            inter = set(cards[i]) & set(cards[j])
            assert len(inter) == 1, f"Cards {i} and {j} intersection != 1: {inter}"
            
    return cards

# ---------------------------------------------------------------------------
# 3. Dynamic Non-Overlapping Layout Solver
# ---------------------------------------------------------------------------
def solve_layout_no_overlap(seed, canvas_radius=440, safe_margin=55):
    max_boundary = canvas_radius - safe_margin
    rng = random.Random(seed)
    
    # Varied sizes: 1 large (82-88), 4 medium (65-74), 3 small (50-56)
    sizes = [
        rng.uniform(82, 88),
        rng.uniform(70, 75),
        rng.uniform(67, 72),
        rng.uniform(64, 69),
        rng.uniform(62, 66),
        rng.uniform(53, 58),
        rng.uniform(50, 55),
        rng.uniform(48, 53)
    ]
    rng.shuffle(sizes)
    
    pattern = rng.choice(['1_7', '2_6', '3_5'])
    pts = []
    
    if pattern == '1_7':
        pts.append([0.0, 0.0, sizes[0], rng.uniform(-25, 25)])
        rot0 = rng.uniform(0, 2 * math.pi)
        ring_r = 250.0
        for i in range(7):
            ang = rot0 + i * (2 * math.pi / 7) + rng.uniform(-0.10, 0.10)
            r = ring_r + rng.uniform(-15, 15)
            pts.append([r * math.cos(ang), r * math.sin(ang), sizes[i + 1], rng.uniform(-30, 30)])
    elif pattern == '2_6':
        rot0 = rng.uniform(0, 2 * math.pi)
        for i in range(2):
            ang = rot0 + i * math.pi + rng.uniform(-0.12, 0.12)
            r = 95.0 + rng.uniform(-10, 10)
            pts.append([r * math.cos(ang), r * math.sin(ang), sizes[i], rng.uniform(-25, 25)])
        rot2 = rot0 + math.pi / 2 + rng.uniform(-0.15, 0.15)
        for i in range(6):
            ang = rot2 + i * (2 * math.pi / 6) + rng.uniform(-0.10, 0.10)
            r = 265.0 + rng.uniform(-15, 15)
            pts.append([r * math.cos(ang), r * math.sin(ang), sizes[i + 2], rng.uniform(-30, 30)])
    else: # 3_5
        rot0 = rng.uniform(0, 2 * math.pi)
        for i in range(3):
            ang = rot0 + i * (2 * math.pi / 3) + rng.uniform(-0.12, 0.12)
            r = 105.0 + rng.uniform(-10, 10)
            pts.append([r * math.cos(ang), r * math.sin(ang), sizes[i], rng.uniform(-25, 25)])
        rot2 = rot0 + math.pi / 3 + rng.uniform(-0.15, 0.15)
        for i in range(5):
            ang = rot2 + i * (2 * math.pi / 5) + rng.uniform(-0.10, 0.10)
            r = 270.0 + rng.uniform(-15, 15)
            pts.append([r * math.cos(ang), r * math.sin(ang), sizes[i + 3], rng.uniform(-30, 30)])
            
    # Relaxation simulation with clearance
    for it in range(120):
        # Repulsion
        for i in range(8):
            for j in range(i + 1, 8):
                dx = pts[j][0] - pts[i][0]
                dy = pts[j][1] - pts[i][1]
                dist = math.hypot(dx, dy)
                min_dist = pts[i][2] + pts[j][2] + 24.0 # 24px clearance buffer
                if dist < min_dist:
                    if dist < 0.001:
                        dx, dy, dist = 1.0, 0.0, 1.0
                    push = (min_dist - dist) * 0.45
                    ux, uy = dx / dist, dy / dist
                    pts[i][0] -= ux * push
                    pts[i][1] -= uy * push
                    pts[j][0] += ux * push
                    pts[j][1] += uy * push
        # Boundary constraint
        for i in range(8):
            d = math.hypot(pts[i][0], pts[i][1])
            limit = max_boundary - pts[i][2]
            if d > limit:
                pts[i][0] *= limit / d
                pts[i][1] *= limit / d

    return pts

# ---------------------------------------------------------------------------
# 4. Rendering Functions for Cards
# ---------------------------------------------------------------------------
def get_font(size):
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def render_playing_card(symbols, card_idx, seed):
    img_size = 1000
    center = img_size / 2
    R = 475 # Card radius (diameter 950 px on 1000x1000 canvas)
    
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Card circular disc
    draw.ellipse([center - R, center - R, center + R, center + R], fill=(255, 255, 255, 255))
    # Subtle clean circular cut guide
    draw.ellipse([center - R, center - R, center + R, center + R], outline=(200, 205, 215), width=3)
    # Subtle inner decorative ring
    draw.ellipse([center - R + 10, center - R + 10, center + R - 10, center + R - 10], outline=(242, 245, 248), width=2)
    
    # Layout positions
    positions = solve_layout_no_overlap(seed=seed, canvas_radius=R, safe_margin=60)
    
    rng = random.Random(seed + 777)
    shuffled_symbols = list(symbols)
    rng.shuffle(shuffled_symbols)
    
    for sym_idx, pos in zip(shuffled_symbols, positions):
        x, y, radius, tilt = pos
        animal = ANIMALS[sym_idx]
        icon_path = os.path.join("chibi_animals", f"{animal['slug']}.png")
        icon = Image.open(icon_path).convert('RGBA')
        
        diameter = int(radius * 2)
        icon_resized = icon.resize((diameter, diameter), Image.Resampling.LANCZOS)
        if abs(tilt) > 1:
            icon_resized = icon_resized.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=True)
            
        w, h = icon_resized.size
        px = int(center + x - w / 2)
        py = int(center + y - h / 2)
        img.paste(icon_resized, (px, py), icon_resized)
        
    return img

def render_logo_mascot_card():
    img_size = 1000
    center = img_size / 2
    R = 475
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([center - R, center - R, center + R, center + R], fill=(255, 251, 242, 255), outline=(255, 175, 75), width=6)
    draw.ellipse([center - R + 14, center - R + 14, center + R - 14, center + R - 14], outline=(255, 220, 160), width=3)
    
    featured = [('panda', -math.pi/4), ('cat', math.pi/4), ('frog', 3*math.pi/4), ('fox', -3*math.pi/4)]
    for slug, ang in featured:
        p = os.path.join("chibi_animals", f"{slug}.png")
        if os.path.exists(p):
            im = Image.open(p).convert('RGBA').resize((150, 150), Image.Resampling.LANCZOS)
            x = center + 310 * math.cos(ang)
            y = center + 310 * math.sin(ang)
            img.paste(im, (int(x - 75), int(y - 75)), im)
            
    # Central plaque
    draw.ellipse([center - 215, center - 215, center + 215, center + 215], fill=(255, 255, 255, 255), outline=(255, 165, 55), width=5)
    
    f_title = get_font(52)
    f_sub = get_font(28)
    f_extra = get_font(22)
    
    t1 = "CHIBI ANIMAL"
    b1 = draw.textbbox((0, 0), t1, font=f_title)
    draw.text((center - (b1[2]-b1[0])/2, center - 105), t1, fill=(255, 110, 40), font=f_title)
    
    t2 = "SPOT IT!"
    b2 = draw.textbbox((0, 0), t2, font=f_title)
    draw.text((center - (b2[2]-b2[0])/2, center - 40), t2, fill=(60, 175, 80), font=f_title)
    
    t3 = "57 CARDS • 57 ANIMALS"
    b3 = draw.textbbox((0, 0), t3, font=f_sub)
    draw.text((center - (b3[2]-b3[0])/2, center + 25), t3, fill=(110, 130, 150), font=f_sub)
    
    t4 = "Always Exactly 1 Match!"
    b4 = draw.textbbox((0, 0), t4, font=f_extra)
    draw.text((center - (b4[2]-b4[0])/2, center + 65), t4, fill=(160, 110, 210), font=f_extra)
    
    return img

def render_quick_rules_card():
    img_size = 1000
    center = img_size / 2
    R = 475
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([center - R, center - R, center + R, center + R], fill=(245, 252, 255, 255), outline=(70, 170, 240), width=6)
    draw.ellipse([center - R + 14, center - R + 14, center + R - 14, center + R - 14], outline=(180, 225, 255), width=3)
    
    f_head = get_font(44)
    f_body = get_font(25)
    f_bold = get_font(27)
    
    t_head = "HOW TO PLAY"
    b_head = draw.textbbox((0, 0), t_head, font=f_head)
    draw.text((center - (b_head[2]-b_head[0])/2, center - 300), t_head, fill=(30, 130, 210), font=f_head)
    
    steps = [
        ("1. REVEAL", "Turn over 2 cards. There is ALWAYS", "exactly ONE matching animal!"),
        ("2. SPOT IT", "Be the fastest player to spot the", "matching animal between them!"),
        ("3. SHOUT & WIN", "Shout its name out loud to take", "or discard the card! Fast wins!")
    ]
    
    y = center - 200
    for title, l1, l2 in steps:
        draw.text((center - 270, y), title, fill=(230, 90, 40), font=f_bold)
        draw.text((center - 270, y + 38), l1, fill=(60, 70, 80), font=f_body)
        draw.text((center - 270, y + 72), l2, fill=(60, 70, 80), font=f_body)
        y += 135
        
    t_foot = "2 - 8 Players • Ages 4 to Adult"
    b_foot = draw.textbbox((0, 0), t_foot, font=f_body)
    draw.text((center - (b_foot[2]-b_foot[0])/2, center + 270), t_foot, fill=(90, 140, 180), font=f_body)
    
    return img

def render_mini_games_card():
    img_size = 1000
    center = img_size / 2
    R = 475
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([center - R, center - R, center + R, center + R], fill=(254, 247, 255, 255), outline=(190, 95, 240), width=6)
    draw.ellipse([center - R + 14, center - R + 14, center + R - 14, center + R - 14], outline=(230, 190, 255), width=3)
    
    f_head = get_font(44)
    f_body = get_font(24)
    f_bold = get_font(26)
    
    t_head = "5 GAME MODES"
    b_head = draw.textbbox((0, 0), t_head, font=f_head)
    draw.text((center - (b_head[2]-b_head[0])/2, center - 310), t_head, fill=(160, 60, 210), font=f_head)
    
    games = [
        ("• THE TOWER", "Race to claim cards from the center pile."),
        ("• THE WELL", "First player to empty their personal stack wins."),
        ("• HOT POTATO", "Pass matching cards to rivals before time runs out!"),
        ("• POISONED GIFT", "Place matching cards onto opponents' piles!"),
        ("• TRIPLE MATCH", "Find 3 cards sharing the same animal symbol.")
    ]
    
    y = center - 220
    for name, desc in games:
        draw.text((center - 285, y), name, fill=(210, 80, 50), font=f_bold)
        draw.text((center - 260, y + 34), desc, fill=(70, 75, 85), font=f_body)
        y += 92
        
    t_foot = "See Rulebook (Page 11) for Details"
    b_foot = draw.textbbox((0, 0), t_foot, font=f_body)
    draw.text((center - (b_foot[2]-b_foot[0])/2, center + 275), t_foot, fill=(150, 100, 200), font=f_body)
    
    return img

def render_card_back_image():
    img_size = 1000
    center = img_size / 2
    R = 475
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer circle border
    draw.ellipse([center - R, center - R, center + R, center + R], fill=(255, 250, 242, 255), outline=(255, 160, 60), width=7)
    draw.ellipse([center - R + 14, center - R + 14, center + R - 14, center + R - 14], outline=(255, 210, 150), width=3)
    
    # Cute radial dots
    for i in range(24):
        ang = i * (2 * math.pi / 24)
        dot_r = R - 35
        x = center + dot_r * math.cos(ang)
        y = center + dot_r * math.sin(ang)
        draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 180, 100))
        
    # Central decorative circle
    R_center = 220
    draw.ellipse([center - R_center, center - R_center, center + R_center, center + R_center], fill=(255, 255, 255), outline=(255, 150, 45), width=5)
    
    # 4 cute animals around center
    corner_animals = [('panda', -math.pi/4), ('cat', math.pi/4), ('frog', 3*math.pi/4), ('fox', -3*math.pi/4)]
    for anim, ang in corner_animals:
        path = os.path.join('chibi_animals', f'{anim}.png')
        if os.path.exists(path):
            im = Image.open(path).convert('RGBA').resize((140, 140), Image.Resampling.LANCZOS)
            x = center + 310 * math.cos(ang)
            y = center + 310 * math.sin(ang)
            img.paste(im, (int(x - 70), int(y - 70)), im)
            
    f_large = get_font(52)
    f_small = get_font(26)
    
    t1 = "SPOT"
    b1 = draw.textbbox((0, 0), t1, font=f_large)
    draw.text((center - (b1[2]-b1[0])/2, center - 90), t1, fill=(255, 105, 30), font=f_large)
    
    t2 = "~ THE ~"
    b2 = draw.textbbox((0, 0), t2, font=f_small)
    draw.text((center - (b2[2]-b2[0])/2, center - 20), t2, fill=(255, 165, 45), font=f_small)
    
    t3 = "CHIBI!"
    b3 = draw.textbbox((0, 0), t3, font=f_large)
    draw.text((center - (b3[2]-b3[0])/2, center + 30), t3, fill=(90, 180, 45), font=f_large)
    
    return img

# ---------------------------------------------------------------------------
# 5. Build Complete PDFs with ReportLab
# ---------------------------------------------------------------------------
def generate_all():
    print("Step 1: Calculating Projective Plane PG(2, 7)...")
    cards = generate_projective_plane()
    print("Projective plane verified! 57 cards, 8 symbols each.")
    
    os.makedirs("rendered_cards", exist_ok=True)
    
    print("Step 2: Pre-rendering 57 cards + 3 bonus cards + card back...")
    card_image_paths = []
    for i, c_syms in enumerate(cards):
        img_path = f"rendered_cards/card_{i+1:02d}.png"
        card_image_paths.append(img_path)
        if not os.path.exists(img_path):
            img = render_playing_card(c_syms, card_idx=i+1, seed=2000 + i * 31)
            img.save(img_path)
    
    logo_path = "rendered_cards/card_58_logo.png"
    rules_path = "rendered_cards/card_59_rules.png"
    games_path = "rendered_cards/card_60_games.png"
    back_path = "rendered_cards/card_back.png"
    
    render_logo_mascot_card().save(logo_path)
    render_quick_rules_card().save(rules_path)
    render_mini_games_card().save(games_path)
    render_card_back_image().save(back_path)
    
    all_60_cards = card_image_paths + [logo_path, rules_path, games_path]
    card_titles = [f"Card #{i+1}" for i in range(57)] + [
        "Mascot Card", "Quick Rules Card", "Game Modes Card"
    ]
    
    print("Step 3: Creating Master Printable Cards PDF (chibi_animal_spot_it_cards_A4.pdf)...")
    pdf_path = "chibi_animal_spot_it_cards_A4.pdf"
    PAGE_W, PAGE_H = A4
    
    CARD_D_MM = 84.0
    CARD_R_MM = CARD_D_MM / 2.0
    CARD_D_PT = CARD_D_MM * mm
    CARD_R_PT = CARD_D_PT / 2.0
    
    MARGIN_X_MM = 16.0
    MARGIN_Y_MM = 16.0
    GAP_X_MM = 10.0
    GAP_Y_MM = 6.5
    
    c = canvas.Canvas(pdf_path, pagesize=A4)
    
    # 10 pages for 60 cards (6 per page)
    for p_idx in range(10):
        # Header
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, "CHIBI ANIMAL SPOT IT! • 57 Cards Printable Game")
        c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, f"A4 Safe Print • Page {p_idx + 1} of 12")
        
        # Footer
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#94A3B8"))
        c.drawString(MARGIN_X_MM * mm, 10 * mm, "✂ Cut along the circular outline (84mm) or along corner crop marks. Every card pair shares exactly 1 animal!")
        c.drawRightString(PAGE_W - MARGIN_X_MM * mm, 10 * mm, "Standard 84mm (3.3in) Card Diameter")
        
        for r in range(3):
            for col in range(2):
                idx = p_idx * 6 + r * 2 + col
                cx_mm = MARGIN_X_MM + CARD_R_MM + col * (CARD_D_MM + GAP_X_MM)
                cy_mm = 297.0 - (MARGIN_Y_MM + CARD_R_MM + r * (CARD_D_MM + GAP_Y_MM))
                
                cx_pt = cx_mm * mm
                cy_pt = cy_mm * mm
                
                # Card label above
                c.setFont("Helvetica-Bold", 7.5)
                c.setFillColor(colors.HexColor("#64748B"))
                c.drawCentredString(cx_pt, cy_pt + CARD_R_PT + 2.5 * mm, card_titles[idx])
                
                # Precision corner crop marks for straight trimming (L-marks at 4 corners of 86x86mm box)
                box_half = (CARD_D_MM / 2.0 + 1.0) * mm
                mark_len = 3.0 * mm
                c.setStrokeColor(colors.HexColor("#CBD5E1"))
                c.setLineWidth(0.4)
                
                # Top-Left
                c.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half + mark_len, cy_pt + box_half)
                c.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half, cy_pt + box_half - mark_len)
                # Top-Right
                c.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half - mark_len, cy_pt + box_half)
                c.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half, cy_pt + box_half - mark_len)
                # Bottom-Left
                c.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half + mark_len, cy_pt - box_half)
                c.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half, cy_pt - box_half + mark_len)
                # Bottom-Right
                c.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half - mark_len, cy_pt - box_half)
                c.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half, cy_pt - box_half + mark_len)
                
                # Alignment ticks at 12, 3, 6, 9 o'clock
                c.setStrokeColor(colors.HexColor("#94A3B8"))
                c.setLineWidth(0.5)
                c.line(cx_pt, cy_pt + CARD_R_PT + 0.6 * mm, cx_pt, cy_pt + CARD_R_PT + 2.2 * mm)
                c.line(cx_pt, cy_pt - CARD_R_PT - 0.6 * mm, cx_pt, cy_pt - CARD_R_PT - 2.2 * mm)
                c.line(cx_pt - CARD_R_PT - 0.6 * mm, cy_pt, cx_pt - CARD_R_PT - 2.2 * mm, cy_pt)
                c.line(cx_pt + CARD_R_PT + 0.6 * mm, cy_pt, cx_pt + CARD_R_PT + 2.2 * mm, cy_pt)
                
                # Place Card Image
                c.drawImage(all_60_cards[idx], cx_pt - CARD_R_PT, cy_pt - CARD_R_PT, width=CARD_D_PT, height=CARD_D_PT, mask='auto')
                
        c.showPage()
        
    print("Step 4: Appending Rulebook Page (Page 11)...")
    draw_rules_page(c)
    # Add page number to rules page
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, "CHIBI ANIMAL SPOT IT! • Complete Rules & Print Guide")
    c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, "A4 Safe Print • Page 11 of 12")
    c.showPage()
    
    print("Step 5: Appending Visual Animal Key Page (Page 12)...")
    draw_visual_key_page(c)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, "CHIBI ANIMAL SPOT IT! • Visual Animal Key & Checklist")
    c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, "A4 Safe Print • Page 12 of 12")
    c.showPage()
    
    c.save()
    print(f"Master Cards PDF generated successfully: {pdf_path}")
    
    print("Step 6: Creating Duplex Card Backs PDF (chibi_animal_card_backs_A4.pdf)...")
    backs_pdf_path = "chibi_animal_card_backs_A4.pdf"
    cb = canvas.Canvas(backs_pdf_path, pagesize=A4)
    
    for p_idx in range(10):
        # Header
        cb.setFont("Helvetica-Bold", 8)
        cb.setFillColor(colors.HexColor("#64748B"))
        cb.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, "CHIBI ANIMAL SPOT IT! • Card Backs (Duplex Printing)")
        cb.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, f"Back Page {p_idx + 1} of 10")
        
        # Footer
        cb.setFont("Helvetica", 7)
        cb.setFillColor(colors.HexColor("#94A3B8"))
        cb.drawString(MARGIN_X_MM * mm, 10 * mm, "Print duplex with Pages 1-10 (Flip on Long Edge) or cut and paste on reverse side.")
        cb.drawRightString(PAGE_W - MARGIN_X_MM * mm, 10 * mm, "Standard 84mm (3.3in) Card Diameter")
        
        for r in range(3):
            for col in range(2):
                # In duplex flip along long edge:
                # Column 0 on the front aligns with Column 1 on the back, and vice versa!
                # Because X_back = 210 - X_front
                # Our columns are at:
                # Col 0: cx = 16 + 42 = 58 mm
                # Col 1: cx = 210 - 16 - 42 = 152 mm
                # So the card grid is already 100% horizontally symmetric!
                cx_mm = MARGIN_X_MM + CARD_R_MM + col * (CARD_D_MM + GAP_X_MM)
                cy_mm = 297.0 - (MARGIN_Y_MM + CARD_R_MM + r * (CARD_D_MM + GAP_Y_MM))
                
                cx_pt = cx_mm * mm
                cy_pt = cy_mm * mm
                
                # Corner crop marks
                box_half = (CARD_D_MM / 2.0 + 1.0) * mm
                mark_len = 3.0 * mm
                cb.setStrokeColor(colors.HexColor("#CBD5E1"))
                cb.setLineWidth(0.4)
                
                cb.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half + mark_len, cy_pt + box_half)
                cb.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half, cy_pt + box_half - mark_len)
                cb.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half - mark_len, cy_pt + box_half)
                cb.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half, cy_pt + box_half - mark_len)
                cb.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half + mark_len, cy_pt - box_half)
                cb.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half, cy_pt - box_half + mark_len)
                cb.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half - mark_len, cy_pt - box_half)
                cb.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half, cy_pt - box_half + mark_len)
                
                # Alignment ticks
                cb.setStrokeColor(colors.HexColor("#94A3B8"))
                cb.setLineWidth(0.5)
                cb.line(cx_pt, cy_pt + CARD_R_PT + 0.6 * mm, cx_pt, cy_pt + CARD_R_PT + 2.2 * mm)
                cb.line(cx_pt, cy_pt - CARD_R_PT - 0.6 * mm, cx_pt, cy_pt - CARD_R_PT - 2.2 * mm)
                cb.line(cx_pt - CARD_R_PT - 0.6 * mm, cy_pt, cx_pt - CARD_R_PT - 2.2 * mm, cy_pt)
                cb.line(cx_pt + CARD_R_PT + 0.6 * mm, cy_pt, cx_pt + CARD_R_PT + 2.2 * mm, cy_pt)
                
                # Place Card Back Image
                cb.drawImage(back_path, cx_pt - CARD_R_PT, cy_pt - CARD_R_PT, width=CARD_D_PT, height=CARD_D_PT, mask='auto')
                
        cb.showPage()
        
    cb.save()
    print(f"Card Backs PDF generated successfully: {backs_pdf_path}")
    print("ALL DONE!")

if __name__ == "__main__":
    generate_all()
