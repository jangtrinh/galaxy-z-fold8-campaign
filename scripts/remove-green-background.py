#!/usr/bin/env python3
# pyright: reportGeneralTypeIssues=false, reportArgumentType=false
"""Normalize generated hero plates and remove the product's uniform green matte."""

from pathlib import Path
from PIL import Image

TARGET = (1672, 941)
BACKGROUND_SOURCE = Path("assets/hero-layers/hero-background-plate-wide.png")
BACKGROUND_OUTPUT = Path("assets/hero-layers/hero-background-layer.png")
PRODUCT_SOURCE = Path("assets/hero-layers/hero-product-green-matte.png")
PRODUCT_OUTPUT = Path("assets/hero-layers/hero-product-cutout.png")


def pad_to_target(image: Image.Image, fill: tuple[int, ...]) -> Image.Image:
    """Pad a near-target image by extending its last row/column."""
    width, height = image.size
    if width > TARGET[0] or height > TARGET[1]:
        image = image.crop((0, 0, min(width, TARGET[0]), min(height, TARGET[1])))
        width, height = image.size
    canvas = Image.new(image.mode, TARGET, fill)
    canvas.paste(image, (0, 0))
    if width < TARGET[0]:
        edge = image.crop((width - 1, 0, width, height)).resize((TARGET[0] - width, height))
        canvas.paste(edge, (width, 0))
    if height < TARGET[1]:
        edge = canvas.crop((0, height - 1, TARGET[0], height)).resize((TARGET[0], TARGET[1] - height))
        canvas.paste(edge, (0, height))
    return canvas


background = pad_to_target(Image.open(BACKGROUND_SOURCE).convert("RGB"), (255, 101, 79))
background.save(BACKGROUND_OUTPUT, optimize=True)

product = pad_to_target(Image.open(PRODUCT_SOURCE).convert("RGBA"), (0, 255, 0, 255))
processed = []
for red, green, blue, _ in product.getdata():
    chroma_excess = green - max(red, blue)
    if green < 80 or chroma_excess <= 24:
        alpha = 255
    elif chroma_excess >= 150:
        alpha = 0
    else:
        alpha = round(255 * (150 - chroma_excess) / 126)
    if alpha < 255:
        green = min(green, max(red, blue) + 8)
    processed.append((red, green, blue, alpha))

product.putdata(processed)
product.save(PRODUCT_OUTPUT, optimize=True)

alpha_values = list(product.getchannel("A").getdata())
width, height = product.size
corners = [alpha_values[0], alpha_values[width - 1], alpha_values[(height - 1) * width], alpha_values[-1]]
alpha_range = min(alpha_values), max(alpha_values)
if background.size != TARGET or product.size != TARGET:
    raise SystemExit(f"Unexpected dimensions: background={background.size}, product={product.size}")
if any(corners):
    raise SystemExit(f"Corners are not transparent: {corners}")
if alpha_range != (0, 255):
    raise SystemExit(f"Expected transparent and opaque pixels, got {alpha_range}")

print(
    "HERO_LAYERS_OK "
    f"size={width}x{height} corners={corners} "
    f"transparent={alpha_values.count(0)} opaque={alpha_values.count(255)}"
)
