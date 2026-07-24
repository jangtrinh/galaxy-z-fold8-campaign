from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).resolve().parents[1] / "assets"

CUTOUTS = {
    "hero-open-chroma.png": "hero-open.png",
    "view-folded-chroma.png": "view-folded.png",
    "ratio-motion-chroma.png": "ratio-motion.png",
    "commerce-ghost-chroma.png": "commerce-ghost.png",
}


def remove_green(source: Path, destination: Path) -> None:
    image = Image.open(source).convert("RGBA")
    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, _ = pixels[x, y]
            dominance = green - max(red, blue)

            if dominance >= 72:
                alpha = 0
            elif dominance <= 20:
                alpha = 255
            else:
                alpha = round(255 * (72 - dominance) / 52)

            if alpha < 255:
                green = min(green, max(red, blue) + 8)

            pixels[x, y] = (red, green, blue, alpha)

    image.save(destination, optimize=True)


for source_name, destination_name in CUTOUTS.items():
    remove_green(ASSETS / source_name, ASSETS / destination_name)

system = Image.open(ASSETS / "system-exploded.png").convert("RGB")
# Remove the left-side hallucinated typography while retaining the equipment field.
system = system.crop((310, 0, system.width, system.height))
system.save(ASSETS / "system-lab.jpg", quality=92, optimize=True)

for source_name in CUTOUTS:
    (ASSETS / source_name).unlink()

rejected = ASSETS / "ratio-rest-chroma.png"
if rejected.exists():
    rejected.unlink()

old_system = ASSETS / "system-exploded.png"
if old_system.exists():
    old_system.unlink()

rejected_hero = ASSETS / "hero-open-rejected.png"
if rejected_hero.exists():
    rejected_hero.unlink()

print("processed", len(CUTOUTS), "cutouts and system crop")
