import math
import random
import os
from PIL import Image, ImageDraw

def render_sample(card_symbols, animal_files, seed=123, card_idx=1):
    random.seed(seed)
    # Card image size: 600 x 600 px (300 DPI for 2-inch circle or 180 DPI for 84mm)
    img_size = 600
    center = img_size / 2
    R = 270 # Card radius in pixels
    
    # Create RGBA canvas
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw card background: white circle with soft pastel border or clean outline
    # Card circle
    draw.ellipse([center - R, center - R, center + R, center + R], fill=(255, 255, 255, 255), outline=(220, 224, 230), width=4)
    # Subtle inner decorative ring
    draw.ellipse([center - R + 8, center - R + 8, center + R - 8, center + R - 8], outline=(240, 243, 246), width=2)
    
    # Choose layout pattern
    pattern = random.choice(['1_7', '2_6', '3_5'])
    positions = []
    
    if pattern == '1_7':
        # 1 central
        positions.append((0, 0, random.uniform(85, 95), random.uniform(-25, 25)))
        rot0 = random.uniform(0, 2 * math.pi)
        ring_r = random.uniform(160, 175)
        for i in range(7):
            ang = rot0 + i * (2 * math.pi / 7) + random.uniform(-0.1, 0.1)
            r = ring_r + random.uniform(-8, 8)
            size = random.uniform(65, 80)
            tilt = random.uniform(-35, 35)
            positions.append((r * math.cos(ang), r * math.sin(ang), size, tilt))
    elif pattern == '2_6':
        rot0 = random.uniform(0, 2 * math.pi)
        r_in = random.uniform(65, 75)
        for i in range(2):
            ang = rot0 + i * math.pi + random.uniform(-0.1, 0.1)
            size = random.uniform(75, 90)
            tilt = random.uniform(-30, 30)
            positions.append((r_in * math.cos(ang), r_in * math.sin(ang), size, tilt))
        rot2 = rot0 + math.pi / 2 + random.uniform(-0.2, 0.2)
        for i in range(6):
            ang = rot2 + i * (2 * math.pi / 6) + random.uniform(-0.1, 0.1)
            r = random.uniform(175, 185)
            size = random.uniform(60, 75)
            tilt = random.uniform(-35, 35)
            positions.append((r * math.cos(ang), r * math.sin(ang), size, tilt))
    else: # 3_5
        rot0 = random.uniform(0, 2 * math.pi)
        r_in = random.uniform(70, 80)
        for i in range(3):
            ang = rot0 + i * (2 * math.pi / 3) + random.uniform(-0.1, 0.1)
            size = random.uniform(70, 85)
            tilt = random.uniform(-30, 30)
            positions.append((r_in * math.cos(ang), r_in * math.sin(ang), size, tilt))
        rot2 = rot0 + math.pi / 3 + random.uniform(-0.2, 0.2)
        for i in range(5):
            ang = rot2 + i * (2 * math.pi / 5) + random.uniform(-0.1, 0.1)
            r = random.uniform(180, 190)
            size = random.uniform(60, 75)
            tilt = random.uniform(-35, 35)
            positions.append((r * math.cos(ang), r * math.sin(ang), size, tilt))
            
    # Relaxation iterations to prevent overlaps
    coords = [[p[0], p[1], p[2], p[3]] for p in positions]
    for step in range(30):
        for i in range(8):
            for j in range(i + 1, 8):
                dx = coords[j][0] - coords[i][0]
                dy = coords[j][1] - coords[i][1]
                dist = math.hypot(dx, dy)
                min_dist = coords[i][2] + coords[j][2] + 4 # clearance
                if dist < min_dist and dist > 0.001:
                    push = (min_dist - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    coords[i][0] -= ux * push
                    coords[i][1] -= uy * push
                    coords[j][0] += ux * push
                    coords[j][1] += uy * push
        for i in range(8):
            d = math.hypot(coords[i][0], coords[i][1])
            max_d = R - coords[i][2] - 12
            if d > max_d and d > 0:
                coords[i][0] *= max_d / d
                coords[i][1] *= max_d / d

    # Shuffle symbols so they map to random slots
    syms = list(card_symbols)
    random.shuffle(syms)
    
    # Paste animal images
    for idx, (sym, pos) in enumerate(zip(syms, coords)):
        x, y, radius, tilt = pos
        animal_name = animal_files[sym]
        path = os.path.join('chibi_animals', f'{animal_name}.png')
        icon = Image.open(path).convert('RGBA')
        
        diameter = int(radius * 2)
        icon_resized = icon.resize((diameter, diameter), Image.Resampling.LANCZOS)
        if abs(tilt) > 1:
            icon_resized = icon_resized.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=True)
            
        w, h = icon_resized.size
        paste_x = int(center + x - w / 2)
        paste_y = int(center + y - h / 2)
        img.paste(icon_resized, (paste_x, paste_y), icon_resized)
        
    # Draw tiny card number in small faint text at top or bottom edge
    # draw.text((center - 10, center + R - 20), f"#{card_idx}", fill=(180, 190, 200))
    return img

animal_list = [
    'cat', 'dog', 'fox', 'bear', 'panda', 'koala', 'lion', 'tiger',
    'frog', 'monkey', 'pig', 'cow', 'mouse', 'rabbit', 'hamster', 'wolf',
    'hedgehog', 'otter', 'sloth', 'beaver', 'bat', 'owl', 'penguin', 'duck',
    'rooster', 'parrot', 'flamingo', 'peacock', 'crocodile', 'turtle', 'lizard', 'snake',
    'octopus', 'squid', 'crab', 'dolphin', 'whale', 'shark', 'seal', 'tropical_fish',
    'blowfish', 'jellyfish', 'bee', 'butterfly', 'ladybug', 'snail', 'giraffe', 'elephant',
    'rhino', 'hippo', 'zebra', 'deer', 'horse', 'unicorn', 'llama', 'kangaroo', 'gorilla'
]

# Let's test with 8 symbols
sample_symbols = [0, 4, 8, 12, 16, 20, 24, 28] # cat, panda, frog, mouse, hedgehog, bat, rooster, crocodile
img = render_sample(sample_symbols, animal_list, seed=42)
img.save('sample_card_1.png')
print("Sample card saved to sample_card_1.png")
