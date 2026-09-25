import math
import os
from PIL import Image, ImageDraw, ImageFont

def render_card_back():
    img_size = 1000
    center = img_size / 2
    R = 450
    
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer circle border
    draw.ellipse([center - R, center - R, center + R, center + R], fill=(255, 250, 240, 255), outline=(255, 170, 80), width=8)
    
    # Inner decorative dashed / dotted ring
    R_inner = R - 20
    draw.ellipse([center - R_inner, center - R_inner, center + R_inner, center + R_inner], outline=(255, 205, 150), width=4)
    
    # Cute radial pattern of small stars or dots
    for i in range(24):
        ang = i * (2 * math.pi / 24)
        dot_r = R - 40
        x = center + dot_r * math.cos(ang)
        y = center + dot_r * math.sin(ang)
        draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 180, 100))
        
    # Central decorative circle
    R_center = 260
    draw.ellipse([center - R_center, center - R_center, center + R_center, center + R_center], fill=(255, 255, 255), outline=(255, 160, 60), width=6)
    
    # 4 cute animals around the center circle
    corner_animals = [('panda', -math.pi/4), ('cat', math.pi/4), ('frog', 3*math.pi/4), ('fox', -3*math.pi/4)]
    for anim, ang in corner_animals:
        path = os.path.join('chibi_animals', f'{anim}.png')
        if os.path.exists(path):
            im = Image.open(path).convert('RGBA')
            im_resized = im.resize((150, 150), Image.Resampling.LANCZOS)
            x = center + 330 * math.cos(ang)
            y = center + 330 * math.sin(ang)
            w, h = im_resized.size
            img.paste(im_resized, (int(x - w/2), int(y - h/2)), im_resized)
            
    # Try loading a bold font if available, else default
    font_large = None
    font_small = None
    for font_path in [
        "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
        "/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf"
    ]:
        if os.path.exists(font_path):
            try:
                font_large = ImageFont.truetype(font_path, 60)
                font_small = ImageFont.truetype(font_path, 34)
                break
            except Exception:
                continue

    if font_large is None:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw centered text
    # "SPOT"
    text1 = "SPOT"
    bbox1 = draw.textbbox((0, 0), text1, font=font_large)
    w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
    draw.text((center - w1/2, center - 95), text1, fill=(255, 100, 30), font=font_large)

    # "THE"
    text2 = "★ THE ★"
    bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
    draw.text((center - w2/2, center - 20), text2, fill=(255, 160, 40), font=font_small)

    # "CHIBI!"
    text3 = "CHIBI!"
    bbox3 = draw.textbbox((0, 0), text3, font=font_large)
    w3, h3 = bbox3[2] - bbox3[0], bbox3[3] - bbox3[1]
    draw.text((center - w3/2, center + 35), text3, fill=(100, 180, 50), font=font_large)
    
    return img

back_img = render_card_back()
back_img.save("sample_card_back.png")
print("Saved sample_card_back.png")
