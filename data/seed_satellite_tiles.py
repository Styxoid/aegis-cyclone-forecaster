"""
seed_satellite_tiles.py - Generates synthetic high-resolution multi-spectral satellite tile crops
representing Sentinel-2 (B4/B3/B2 True Color and B8/B4/B3 False-Color Infrared) for:
1. Puri Coastline & Mangrove Buffer (Puri Spit)
2. Paradip Port 132kV Substation Transformer Yard & Canal Inundation Zone
3. Ersama Coastal Basin & Cyclone Refuge
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter

TILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiles")
os.makedirs(TILES_DIR, exist_ok=True)

def generate_puri_coast_tile():
    """Generates a 512x512 Sentinel-2 crop of Puri coastal spit with ocean, sandy beach, degraded mangrove, and urban clusters."""
    img = Image.new("RGB", (512, 512), (15, 35, 60)) # Deep Bay of Bengal water
    draw = ImageDraw.Draw(img)

    # Ocean water textures (wave patterns)
    for y in range(0, 512, 8):
        wave_color = (20 + int(10 * math.sin(y/12)), 45 + int(15 * math.sin(y/12)), 75 + int(20 * math.sin(y/12)))
        draw.line([(0, y), (512, y)], fill=wave_color, width=4)

    # Sandy coastal beach strip running diagonally
    beach_points = [
        (120, 0), (160, 100), (210, 220), (280, 360), (350, 512),
        (512, 512), (512, 0)
    ]
    draw.polygon(beach_points, fill=(215, 195, 155)) # Sand/dune color

    # Mangrove / Casuarina green buffer strip (fragmented bio-shield)
    mangrove_points = [
        (220, 0), (250, 80), (300, 200), (360, 340), (430, 512),
        (512, 512), (512, 0)
    ]
    draw.polygon(mangrove_points, fill=(35, 85, 45)) # Mangrove deep green

    # Add mangrove vegetation patches
    for i in range(150):
        x = 240 + (i * 7) % 250
        y = (i * 19) % 512
        r = 6 + (i % 8)
        color = (25 + (i % 20), 75 + (i % 30), 35 + (i % 15))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

    # Urban settlements & tin roof clusters (inland)
    for i in range(60):
        ux = 380 + (i * 13) % 110
        uy = (i * 23) % 490
        w, h = 8 + (i % 7), 6 + (i % 5)
        # Mix of tin (blue/gray) and concrete (off-white)
        roof_color = (130, 160, 190) if i % 2 == 0 else (190, 190, 185)
        draw.rectangle([ux, uy, ux + w, uy + h], fill=roof_color, outline=(80, 80, 80))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    out_path = os.path.join(TILES_DIR, "sentinel2_puri_coast.png")
    img.save(out_path, "PNG")
    print(f" -> Generated {out_path}")

def generate_paradip_substation_tile():
    """Generates a 512x512 crop showing Paradip port canal, 132kV substation switchyard, and surrounding embankment."""
    img = Image.new("RGB", (512, 512), (65, 80, 70)) # Mixed coastal soil / marsh
    draw = ImageDraw.Draw(img)

    # Taladanda canal cutting through
    canal_points = [
        (0, 180), (120, 190), (260, 210), (380, 235), (512, 250),
        (512, 310), (380, 295), (260, 270), (120, 250), (0, 240)
    ]
    draw.polygon(canal_points, fill=(30, 60, 80)) # Canal water

    # 132kV Substation Transformer Yard (fenced compound)
    sub_box = [160, 40, 360, 180]
    draw.rectangle(sub_box, fill=(185, 180, 170), outline=(100, 100, 100), width=2) # Gravel yard

    # High-voltage transformers & busbars
    for tx in [190, 240, 290, 330]:
        for ty in [65, 110, 145]:
            draw.rectangle([tx - 8, ty - 8, tx + 8, ty + 8], fill=(70, 75, 85), outline=(40, 40, 40))
            draw.line([(tx, ty - 12), (tx, ty + 12)], fill=(120, 130, 140), width=1)

    # Low drainage perimeter trench (at risk of breach from canal)
    draw.rectangle([155, 35, 365, 185], outline=(45, 75, 85), width=3)

    # Arterial Expressway (NH-53)
    draw.line([(0, 380), (512, 395)], fill=(50, 50, 50), width=16) # Asphalt
    draw.line([(0, 380), (512, 395)], fill=(220, 220, 220), width=1) # Center line

    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    out_path = os.path.join(TILES_DIR, "sentinel2_paradip_substation.png")
    img.save(out_path, "PNG")
    print(f" -> Generated {out_path}")

def generate_ersama_shelter_tile():
    """Generates a 512x512 crop of Ersama coastal basin, tidal inlets, and elevated stilted cyclone shelter."""
    img = Image.new("RGB", (512, 512), (50, 75, 55)) # Agricultural coastal flats
    draw = ImageDraw.Draw(img)

    # Meandering estuarine tidal creek
    creek_points = [
        (80, 0), (95, 120), (140, 200), (220, 280), (320, 360), (450, 512),
        (480, 512), (350, 350), (250, 270), (170, 190), (120, 110), (105, 0)
    ]
    draw.polygon(creek_points, fill=(25, 55, 75))

    # Elevated Multipurpose Cyclone Shelter (MCS) fortress structure
    shelter_x, shelter_y = 280, 140
    # Plinth / embankment circle
    draw.ellipse([shelter_x - 45, shelter_y - 45, shelter_x + 45, shelter_y + 45], fill=(160, 150, 130))
    # Two-storey reinforced concrete building footprint
    draw.rectangle([shelter_x - 25, shelter_y - 20, shelter_x + 25, shelter_y + 20], fill=(210, 215, 220), outline=(80, 90, 100), width=2)
    # Stilted columns and access ramp
    draw.line([(shelter_x, shelter_y + 20), (shelter_x, shelter_y + 60)], fill=(120, 110, 95), width=6)

    # Vulnerable thatch/tin coastal hamlets along creek margin
    for i in range(40):
        hx = 80 + (i * 17) % 150
        hy = 200 + (i * 13) % 280
        draw.rectangle([hx, hy, hx + 9, hy + 7], fill=(165, 125, 85), outline=(50, 40, 30))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    out_path = os.path.join(TILES_DIR, "sentinel2_ersama_shelter.png")
    img.save(out_path, "PNG")
    print(f" -> Generated {out_path}")

def seed_tiles():
    print("[Seed Tiles] Generating high-resolution Sentinel-2 crops in data/tiles/...")
    generate_puri_coast_tile()
    generate_paradip_substation_tile()
    generate_ersama_shelter_tile()
    print("[Seed Tiles] All satellite tiles generated successfully!")

if __name__ == "__main__":
    seed_tiles()
