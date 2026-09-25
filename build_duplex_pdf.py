import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image

PAGE_W, PAGE_H = A4

CARD_D_MM = 84.0
CARD_R_MM = CARD_D_MM / 2.0
CARD_D_PT = CARD_D_MM * mm
CARD_R_PT = CARD_D_PT / 2.0

# Bleed settings for card backs
# 1000px image has R_cut=450 (84mm) and R_bleed=485 (90.5mm)
# So image size on paper to make cut circle exactly 84mm:
# img_width = 84.0 * (1000.0 / 900.0) = 93.33 mm
BACK_IMG_D_MM = CARD_D_MM * (1000.0 / 900.0)
BACK_IMG_R_MM = BACK_IMG_D_MM / 2.0
BACK_IMG_D_PT = BACK_IMG_D_MM * mm
BACK_IMG_R_PT = BACK_IMG_D_PT / 2.0

MARGIN_X_MM = 16.0
MARGIN_Y_MM = 16.0
GAP_X_MM = 10.0
GAP_Y_MM = 6.5

def draw_front_page(c, p_idx, all_60_cards, card_titles, total_pages_str):
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, "CHIBI ANIMAL SPOT IT! • 57 Cards Printable Game")
    c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, f"A4 Duplex Ready • Sheet {p_idx + 1} (Front) • Page {p_idx*2 + 1} of {total_pages_str}")
    
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN_X_MM * mm, 10 * mm, "✂ Cut along the circular outline (84mm) or corner crop marks. Every card pair shares exactly 1 animal!")
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
            
            # Corner crop marks for straight cuts (86x86mm box)
            box_half = (CARD_D_MM / 2.0 + 1.0) * mm
            mark_len = 3.0 * mm
            c.setStrokeColor(colors.HexColor("#CBD5E1"))
            c.setLineWidth(0.4)
            
            # 4 Corners
            c.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half + mark_len, cy_pt + box_half)
            c.line(cx_pt - box_half, cy_pt + box_half, cx_pt - box_half, cy_pt + box_half - mark_len)
            c.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half - mark_len, cy_pt + box_half)
            c.line(cx_pt + box_half, cy_pt + box_half, cx_pt + box_half, cy_pt + box_half - mark_len)
            c.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half + mark_len, cy_pt - box_half)
            c.line(cx_pt - box_half, cy_pt - box_half, cx_pt - box_half, cy_pt - box_half + mark_len)
            c.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half - mark_len, cy_pt - box_half)
            c.line(cx_pt + box_half, cy_pt - box_half, cx_pt + box_half, cy_pt - box_half + mark_len)
            
            # Alignment ticks at 12, 3, 6, 9 o'clock
            c.setStrokeColor(colors.HexColor("#94A3B8"))
            c.setLineWidth(0.5)
            c.line(cx_pt, cy_pt + CARD_R_PT + 0.6 * mm, cx_pt, cy_pt + CARD_R_PT + 2.2 * mm)
            c.line(cx_pt, cy_pt - CARD_R_PT - 0.6 * mm, cx_pt, cy_pt - CARD_R_PT - 2.2 * mm)
            c.line(cx_pt - CARD_R_PT - 0.6 * mm, cy_pt, cx_pt - CARD_R_PT - 2.2 * mm, cy_pt)
            c.line(cx_pt + CARD_R_PT + 0.6 * mm, cy_pt, cx_pt + CARD_R_PT + 2.2 * mm, cy_pt)
            
            # Draw Front Card Image (84mm x 84mm)
            c.drawImage(all_60_cards[idx], cx_pt - CARD_R_PT, cy_pt - CARD_R_PT, width=CARD_D_PT, height=CARD_D_PT, mask='auto')

def draw_back_page(c, p_idx, card_titles, total_pages_str, bleed_back_path):
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, "CHIBI ANIMAL SPOT IT! • Card Backs (Duplex Mirrored)")
    c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, f"A4 Duplex Ready • Sheet {p_idx + 1} (Back) • Page {p_idx*2 + 2} of {total_pages_str}")
    
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN_X_MM * mm, 10 * mm, "Mirrored layout for Duplex Printing (Flip on Long Edge). Includes +3mm bleed protection.")
    c.drawRightString(PAGE_W - MARGIN_X_MM * mm, 10 * mm, "Standard 84mm (3.3in) Card Diameter")
    
    for r in range(3):
        for col in range(2):
            # DUPLEX FLIP HORIZONTAL SYMMETRY:
            # When sheet flips along long edge (x -> W - x),
            # Front Col 0 (left) lands on Back Col 1 (right).
            # Front Col 1 (right) lands on Back Col 0 (left).
            front_col = 1 - col
            front_idx = p_idx * 6 + r * 2 + front_col
            matching_title = f"{card_titles[front_idx]} (Back)"
            
            cx_mm = MARGIN_X_MM + CARD_R_MM + col * (CARD_D_MM + GAP_X_MM)
            cy_mm = 297.0 - (MARGIN_Y_MM + CARD_R_MM + r * (CARD_D_MM + GAP_Y_MM))
            
            cx_pt = cx_mm * mm
            cy_pt = cy_mm * mm
            
            # Label
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
            
            # Draw Bleed Back Image (extends to BACK_IMG_D_PT with cut circle at CARD_D_PT)
            c.drawImage(bleed_back_path, cx_pt - BACK_IMG_R_PT, cy_pt - BACK_IMG_R_PT, width=BACK_IMG_D_PT, height=BACK_IMG_D_PT, mask='auto')

def build_all_duplex():
    from build_complete_game import draw_rules_page, draw_visual_key_page
    
    # 1. Ensure bleed card back is rendered
    bleed_back_path = "rendered_cards/card_back_bleed.png"
    from test_bleed_back import render_bleed_card_back
    render_bleed_card_back().save(bleed_back_path)
    
    card_image_paths = [f"rendered_cards/card_{i+1:02d}.png" for i in range(57)]
    logo_path = "rendered_cards/card_58_logo.png"
    rules_path = "rendered_cards/card_59_rules.png"
    games_path = "rendered_cards/card_60_games.png"
    
    all_60_cards = card_image_paths + [logo_path, rules_path, games_path]
    card_titles = [f"Card #{i+1}" for i in range(57)] + [
        "Mascot Card", "Quick Rules Card", "Game Modes Card"
    ]
    
    # 2. Build Duplex Interleaved Master PDF (22 Pages)
    duplex_pdf_path = "chibi_animal_spot_it_cards_A4_duplex.pdf"
    print(f"Building {duplex_pdf_path}...")
    c = canvas.Canvas(duplex_pdf_path, pagesize=A4)
    
    # Sheets 1 to 10 (Front then Back interleaved)
    for p_idx in range(10):
        # Front Page (Odd)
        draw_front_page(c, p_idx, all_60_cards, card_titles, total_pages_str="22")
        c.showPage()
        
        # Back Page (Even)
        draw_back_page(c, p_idx, card_titles, total_pages_str="22", bleed_back_path=bleed_back_path)
        c.showPage()
        
    # Sheet 11 (Double-sided Rulebook):
    # Front: Rules & 5 Mini-Games
    draw_rules_page(c)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, "CHIBI ANIMAL SPOT IT! • Complete Rules & Print Guide")
    c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, "A4 Duplex Ready • Sheet 11 (Front) • Page 21 of 22")
    c.showPage()
    
    # Back: The 57 Animals Visual Key & Checklist
    draw_visual_key_page(c)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN_X_MM * mm, PAGE_H - 11 * mm, "CHIBI ANIMAL SPOT IT! • Visual Animal Key & Checklist")
    c.drawRightString(PAGE_W - MARGIN_X_MM * mm, PAGE_H - 11 * mm, "A4 Duplex Ready • Sheet 11 (Back) • Page 22 of 22")
    c.showPage()
    
    c.save()
    print(f"Master Duplex PDF generated successfully: {duplex_pdf_path}")
    
    # 3. Also update the dedicated Card Backs PDF (10 pages) with the new bleed & mirrored layout
    backs_pdf_path = "chibi_animal_card_backs_A4.pdf"
    print(f"Updating {backs_pdf_path}...")
    cb = canvas.Canvas(backs_pdf_path, pagesize=A4)
    for p_idx in range(10):
        draw_back_page(cb, p_idx, card_titles, total_pages_str="10", bleed_back_path=bleed_back_path)
        cb.showPage()
    cb.save()
    print(f"Updated {backs_pdf_path} successfully!")

if __name__ == "__main__":
    build_all_duplex()
