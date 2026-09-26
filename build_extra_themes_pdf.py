import os, sys, math, random, json, textwrap
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from concurrent.futures import ThreadPoolExecutor

from build_complete_game import generate_projective_plane, solve_layout_no_overlap, get_font

PAGE_W, PAGE_H = A4
CARD_D_MM = 84.0
CARD_R_MM = CARD_D_MM / 2.0
CARD_D_PT = CARD_D_MM * mm
CARD_R_PT = CARD_D_PT / 2.0

BACK_IMG_D_MM = CARD_D_MM * (1000.0 / 900.0)
BACK_IMG_R_MM = BACK_IMG_D_MM / 2.0
BACK_IMG_D_PT = BACK_IMG_D_MM * mm
BACK_IMG_R_PT = BACK_IMG_D_PT / 2.0

MARGIN_X_MM = 16.0
MARGIN_Y_MM = 16.0
GAP_X_MM = 10.0
GAP_Y_MM = 6.5

cards_indices = generate_projective_plane()

with open('web/cards.js') as f:
    cards_code = f.read()

def get_theme_symbols(theme_id):
    start = cards_code.find(f"id: '{theme_id}'")
    sym_start = cards_code.find('symbols: [', start) + len('symbols: ')
    bracket_count = 0
    i = sym_start
    while i < len(cards_code):
        if cards_code[i] == '[': bracket_count += 1
        elif cards_code[i] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                break
        i += 1
    return json.loads(cards_code[sym_start:i+1])

THEME_CONFIGS = [
    {
        'id': 'space',
        'name': 'SPACE & GALAXY',
        'sub': 'Rockets, Aliens, Planets & Cosmic Mysteries',
        'folder': 'space',
        'symbols': get_theme_symbols('space'),
        'title': 'SPOT THE GALAXY! • 57 Cards Printable Game',
        'pdf_path': 'PDFs/space_spot_it_cards_A4_duplex.pdf',
        'header_color': '#4F46E5',
        'bg_header': '#EEF2FF',
        'mascot': 'space/rocket.png',
        'back_title': 'GALAXY!'
    },
    {
        'id': 'vehicles',
        'name': 'VEHICLES & TRAVEL',
        'sub': 'Cars, Trains, Airplanes, Ships & City Transport',
        'folder': 'vehicles',
        'symbols': get_theme_symbols('vehicles'),
        'title': 'SPOT THE RIDE! • 57 Cards Printable Game',
        'pdf_path': 'PDFs/vehicles_spot_it_cards_A4_duplex.pdf',
        'header_color': '#0284C7',
        'bg_header': '#F0F9FF',
        'mascot': 'vehicles/car.png',
        'back_title': 'RIDE!'
    }
]

def render_theme_playing_card(symbols_meta, folder, symbols, card_idx, seed):
    img_size = 1000
    center = img_size / 2
    R = 475
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([center - R, center - R, center + R, center + R], fill=(255, 255, 255, 255))
    draw.ellipse([center - R, center - R, center + R, center + R], outline=(200, 205, 215), width=3)
    draw.ellipse([center - R + 10, center - R + 10, center + R - 10, center + R - 10], outline=(242, 245, 248), width=2)
    
    positions = solve_layout_no_overlap(seed=seed, canvas_radius=R, safe_margin=60)
    rng = random.Random(seed + 777)
    shuffled_symbols = list(symbols)
    rng.shuffle(shuffled_symbols)
    
    for sym_idx, pos in zip(shuffled_symbols, positions):
        x, y, radius, tilt = pos
        item = symbols_meta[sym_idx]
        icon_path = os.path.join(folder, f"{item['slug']}.png")
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

def render_theme_bonus_cards(cfg, temp_dir):
    img = Image.new('RGBA', (1000, 1000), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    R = 475
    draw.ellipse([500 - R, 500 - R, 500 + R, 500 + R], fill=(255, 255, 255, 255), outline=(220, 224, 230), width=4)
    mascot = Image.open(cfg['mascot']).convert('RGBA').resize((360, 360), Image.Resampling.LANCZOS)
    img.paste(mascot, (320, 220), mascot)
    f_title = get_font(52)
    f_sub = get_font(28)
    t = cfg['title'].split('•')[0].strip()
    bb = draw.textbbox((0, 0), t, font=f_title)
    draw.text((500 - (bb[2]-bb[0])/2, 620), t, fill=(30, 41, 59), font=f_title)
    t2 = '57 Cards • 8 Symbols/Card'
    bb2 = draw.textbbox((0, 0), t2, font=f_sub)
    draw.text((500 - (bb2[2]-bb2[0])/2, 700), t2, fill=(100, 116, 139), font=f_sub)
    c58_path = os.path.join(temp_dir, 'card_58_mascot.png')
    img.save(c58_path)
    
    from build_complete_game import render_quick_rules_card, render_mini_games_card
    c59_path = os.path.join(temp_dir, 'card_59_rules.png')
    render_quick_rules_card().save(c59_path)
    c60_path = os.path.join(temp_dir, 'card_60_games.png')
    render_mini_games_card().save(c60_path)
    return [c58_path, c59_path, c60_path]

def render_theme_back_image(cfg, temp_dir):
    img_size = 1000
    center = 500
    R_cut = 450
    R_bleed = 485
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([center - R_bleed, center - R_bleed, center + R_bleed, center + R_bleed], fill=(254, 250, 245, 255))
    draw.ellipse([center - R_cut, center - R_cut, center + R_cut, center + R_cut], fill=(255, 255, 255, 255), outline=(230, 235, 240), width=3)
    
    mascot = Image.open(cfg['mascot']).convert('RGBA').resize((280, 280), Image.Resampling.LANCZOS)
    img.paste(mascot, (center - 140, center - 180), mascot)
    
    f_large = get_font(52)
    f_sub = get_font(24)
    t = cfg['back_title']
    bb = draw.textbbox((0, 0), t, font=f_large)
    draw.text((center - (bb[2]-bb[0])/2, center + 120), t, fill=(30, 41, 59), font=f_large)
    
    t2 = 'SPOT IT!'
    bb2 = draw.textbbox((0, 0), t2, font=f_sub)
    draw.text((center - (bb2[2]-bb2[0])/2, center + 185), t2, fill=(100, 116, 139), font=f_sub)
    
    back_path = os.path.join(temp_dir, 'card_back_bleed.png')
    img.save(back_path)
    return back_path

def build_pdf_for_theme(cfg):
    print(f"\n--- Generating {cfg['name']} Master Duplex PDF ---")
    temp_dir = f"temp_rendered_{cfg['id']}"
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(os.path.dirname(cfg['pdf_path']), exist_ok=True)
    
    # 1. Render all 57 cards
    card_paths = []
    for i, syms in enumerate(cards_indices):
        p = os.path.join(temp_dir, f"card_{i+1:02d}.png")
        card_paths.append(p)
        if not os.path.exists(p):
            card_img = render_theme_playing_card(cfg['symbols'], cfg['folder'], syms, i, seed=1000 + i*13)
            card_img.save(p)
    
    # 2. Render bonus cards and back
    bonus_paths = render_theme_bonus_cards(cfg, temp_dir)
    bleed_back_path = render_theme_back_image(cfg, temp_dir)
    
    all_60_cards = card_paths + bonus_paths
    card_titles = [f"Card #{i+1}" for i in range(57)] + [
        "Theme Mascot Card", "Quick Rules Card", "Game Modes Card"
    ]
    
    # 3. Create ReportLab PDF
    c = canvas.Canvas(cfg['pdf_path'], pagesize=A4)
    c.setTitle(cfg['title'])
    c.setAuthor("Antigravity Spot It Generator")
    
    for sheet_idx in range(10):
        # Front Page
        p_front = sheet_idx * 2 + 1
        c.saveState()
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, cfg['title'])
        c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, f"A4 Duplex Ready • Sheet {sheet_idx + 1} (Front) • Page {p_front} of 22")
        
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#94A3B8"))
        c.drawString(MARGIN_X_MM * mm, 10 * mm, "✂ Cut along the circular outline (84mm) or corner crop marks. Every card pair shares exactly 1 symbol!")
        c.drawRightString(PAGE_W - MARGIN_X_MM * mm, 10 * mm, "Standard 84mm (3.3in) Card Diameter")
        
        for r in range(3):
            for col in range(2):
                idx = sheet_idx * 6 + r * 2 + col
                cx_mm = MARGIN_X_MM + CARD_R_MM + col * (CARD_D_MM + GAP_X_MM)
                cy_mm = 297.0 - (MARGIN_Y_MM + CARD_R_MM + r * (CARD_D_MM + GAP_Y_MM))
                cx_pt = cx_mm * mm
                cy_pt = cy_mm * mm
                
                c.setFont("Helvetica-Bold", 7.5)
                c.setFillColor(colors.HexColor("#64748B"))
                c.drawCentredString(cx_pt, cy_pt + CARD_R_PT + 2.5 * mm, card_titles[idx])
                
                # Corner crop marks
                box_half = (CARD_D_MM / 2.0 + 1.0) * mm
                mark_len = 3.0 * mm
                c.setStrokeColor(colors.HexColor("#CBD5E1"))
                c.setLineWidth(0.4)
                c.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half + mark_len, cy_pt + box_half)
                c.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half, cy_pt + box_half - mark_len)
                c.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half - mark_len, cy_pt + box_half)
                c.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half, cy_pt + box_half - mark_len)
                c.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half + mark_len, cy_pt - box_half)
                c.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half, cy_pt - box_half + mark_len)
                c.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half - mark_len, cy_pt - box_half)
                c.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half, cy_pt - box_half + mark_len)
                
                # Alignment ticks
                c.setStrokeColor(colors.HexColor("#94A3B8"))
                c.setLineWidth(0.5)
                c.line(cx_pt, cy_pt + CARD_R_PT + 0.6 * mm, cx_pt, cy_pt + CARD_R_PT + 2.2 * mm)
                c.line(cx_pt, cy_pt - CARD_R_PT - 0.6 * mm, cx_pt, cy_pt - CARD_R_PT - 2.2 * mm)
                c.line(cx_pt - CARD_R_PT - 0.6 * mm, cy_pt, cx_pt - CARD_R_PT - 2.2 * mm, cy_pt)
                c.line(cx_pt + CARD_R_PT + 0.6 * mm, cy_pt, cx_pt + CARD_R_PT + 2.2 * mm, cy_pt)
                
                c.drawImage(all_60_cards[idx], cx_pt - CARD_R_PT, cy_pt - CARD_R_PT, width=CARD_D_PT, height=CARD_D_PT, mask='auto')
                
        c.restoreState()
        c.showPage()
        
        # Back Page
        p_back = sheet_idx * 2 + 2
        c.saveState()
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, cfg['title'])
        c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, f"A4 Duplex Ready • Sheet {sheet_idx + 1} (Back) • Page {p_back} of 22")
        
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#94A3B8"))
        c.drawString(MARGIN_X_MM * mm, 10 * mm, "Mirrored layout for Duplex Printing (Flip on Long Edge). Includes +3mm bleed protection.")
        c.drawRightString(PAGE_W - MARGIN_X_MM * mm, 10 * mm, "Standard 84mm (3.3in) Card Diameter")
        
        for r in range(3):
            for col in range(2):
                front_col = 1 - col
                front_idx = sheet_idx * 6 + r * 2 + front_col
                matching_title = f"{card_titles[front_idx]} (Back)"
                
                cx_mm = MARGIN_X_MM + CARD_R_MM + col * (CARD_D_MM + GAP_X_MM)
                cy_mm = 297.0 - (MARGIN_Y_MM + CARD_R_MM + r * (CARD_D_MM + GAP_Y_MM))
                cx_pt = cx_mm * mm
                cy_pt = cy_mm * mm
                
                c.setFont("Helvetica-Bold", 7)
                c.setFillColor(colors.HexColor("#94A3B8"))
                c.drawCentredString(cx_pt, cy_pt + CARD_R_PT + 2.5 * mm, matching_title)
                
                # Corner crop marks
                box_half = (CARD_D_MM / 2.0 + 1.0) * mm
                mark_len = 3.0 * mm
                c.setStrokeColor(colors.HexColor("#CBD5E1"))
                c.setLineWidth(0.4)
                c.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half + mark_len, cy_pt + box_half)
                c.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half, cy_pt + box_half - mark_len)
                c.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half - mark_len, cy_pt + box_half)
                c.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half, cy_pt + box_half - mark_len)
                c.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half + mark_len, cy_pt - box_half)
                c.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half, cy_pt - box_half + mark_len)
                c.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half - mark_len, cy_pt - box_half)
                c.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half, cy_pt - box_half + mark_len)
                
                # Alignment ticks
                c.setStrokeColor(colors.HexColor("#94A3B8"))
                c.setLineWidth(0.5)
                c.line(cx_pt, cy_pt + CARD_R_PT + 0.6 * mm, cx_pt, cy_pt + CARD_R_PT + 2.2 * mm)
                c.line(cx_pt, cy_pt - CARD_R_PT - 0.6 * mm, cx_pt, cy_pt - CARD_R_PT - 2.2 * mm)
                c.line(cx_pt - CARD_R_PT - 0.6 * mm, cy_pt, cx_pt - CARD_R_PT - 2.2 * mm, cy_pt)
                c.line(cx_pt + CARD_R_PT + 0.6 * mm, cy_pt, cx_pt + CARD_R_PT + 2.2 * mm, cy_pt)
                
                c.drawImage(bleed_back_path, cx_pt - BACK_IMG_R_PT, cy_pt - BACK_IMG_R_PT, width=BACK_IMG_D_PT, height=BACK_IMG_D_PT, mask='auto')
                
        c.restoreState()
        c.showPage()
    
    # 4. Sheet 11 (Pages 21-22): Rules and Symbol Dictionary
    # Page 21: Rules
    c.saveState()
    c.setFillColor(colors.HexColor(cfg['bg_header']))
    c.roundRect(14*mm, PAGE_H - 42*mm, PAGE_W - 28*mm, 28*mm, 4*mm, fill=1, stroke=0)
    c.drawImage(cfg['mascot'], 18*mm, PAGE_H - 39*mm, width=22*mm, height=22*mm, mask='auto')
    
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor(cfg['header_color']))
    c.drawString(45*mm, PAGE_H - 24*mm, cfg['title'].split('•')[0].strip())
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(45*mm, PAGE_H - 32*mm, f"{cfg['sub']} • 57 Cards • 8 Symbols per Card")
    
    # Golden rule box
    c.setFillColor(colors.HexColor("#FEF3C7"))
    c.roundRect(14*mm, PAGE_H - 66*mm, PAGE_W - 28*mm, 20*mm, 3*mm, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#F59E0B"))
    c.setLineWidth(1)
    c.roundRect(14*mm, PAGE_H - 66*mm, PAGE_W - 28*mm, 20*mm, 3*mm, fill=0, stroke=1)
    
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#92400E"))
    c.drawString(20*mm, PAGE_H - 53*mm, "★ THE GOLDEN RULE OF THE GAME:")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(20*mm, PAGE_H - 60*mm, "Between ANY TWO CARDS in this deck, there is ALWAYS EXACTLY ONE matching symbol!")
    
    rules = [
        ("Game Mode 1: The Tower (Most Popular)",
         "Deal 1 card face-down to each player. Place remaining 55 cards face-up in the center. On 'GO!', flip your card. Spot the matching symbol between your card and center card, shout it out, and grab the center card. Player with most cards wins!"),
        ("Game Mode 2: The Well",
         "Place 1 card face-up in the center. Deal remaining cards evenly to players as face-down draw piles. On 'GO!', flip your top card. First to match and shout places their card onto center pile. First to empty their pile wins!"),
        ("Game Mode 3: Hot Potato",
         "Each player holds 1 card face-up in their hand. Spot match with ANY opponent, shout it, and place your card in their hand! They now hold both. Continue until one player gets stuck with all cards!"),
        ("Game Mode 4: The Poisoned Gift",
         "Center pile face-up, players each have 1 face-up card. Match center card with an OPPONENT's card and give them the center card as a penalty! Player with fewest cards wins!")
    ]
    
    y = PAGE_H - 76*mm
    for title, desc in rules:
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(14*mm, y - 24*mm, PAGE_W - 28*mm, 22*mm, 2.5*mm, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.5)
        c.roundRect(14*mm, y - 24*mm, PAGE_W - 28*mm, 22*mm, 2.5*mm, fill=0, stroke=1)
        
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(colors.HexColor("#1E293B"))
        c.drawString(18*mm, y - 6*mm, title)
        
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#475569"))
        lines = textwrap.wrap(desc, width=105)
        for li, line in enumerate(lines[:3]):
            c.drawString(18*mm, y - 11.5*mm - li*3.8*mm, line)
        y -= 26*mm
        
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, f"{cfg['title']} • Complete Rules Guide")
    c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, "A4 Duplex Ready • Sheet 11 (Front) • Page 21 of 22")
    c.restoreState()
    c.showPage()
    
    # Page 22: Visual Symbol Dictionary
    c.saveState()
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor(cfg['header_color']))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 18 * mm, f"Complete 57 Symbol Dictionary: {cfg['name']}")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 22.5 * mm, "Official reference names for settling disputed calls during fast-paced rounds.")
    
    cols = 6
    rows = 10
    start_x = MARGIN_X_MM * mm
    start_y = PAGE_H - 27 * mm
    col_w = (PAGE_W - 2 * MARGIN_X_MM * mm) / cols
    row_h = (PAGE_H - 38 * mm) / rows
    
    for idx, sym in enumerate(cfg['symbols']):
        r = idx // cols
        col = idx % cols
        cell_x = start_x + col * col_w
        cell_y = start_y - (r + 1) * row_h
        
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.roundRect(cell_x + 1*mm, cell_y + 1*mm, col_w - 2*mm, row_h - 2*mm, 2*mm, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.5)
        c.roundRect(cell_x + 1*mm, cell_y + 1*mm, col_w - 2*mm, row_h - 2*mm, 2*mm, fill=0, stroke=1)
        
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor("#94A3B8"))
        c.drawString(cell_x + 2.5*mm, cell_y + row_h - 5.5*mm, f"#{idx+1}")
        
        icon_path = os.path.join(cfg['folder'], f"{sym['slug']}.png")
        if os.path.exists(icon_path):
            icon_size = 14*mm
            ix = cell_x + (col_w - icon_size) / 2.0
            iy = cell_y + 5.5*mm
            c.drawImage(icon_path, ix, iy, width=icon_size, height=icon_size, mask='auto')
            
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#1E293B"))
        c.drawCentredString(cell_x + col_w / 2.0, cell_y + 2.2*mm, sym['name'])
        
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, f"{cfg['title']} • Visual Symbol Dictionary")
    c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, "A4 Duplex Ready • Sheet 11 (Back) • Page 22 of 22")
    c.restoreState()
    c.showPage()
    
    c.save()
    print(f"Successfully generated {cfg['pdf_path']}!")

for cfg in THEME_CONFIGS:
    build_pdf_for_theme(cfg)
