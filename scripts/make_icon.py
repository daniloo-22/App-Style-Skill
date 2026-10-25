"""Turn a generated app icon (webp/png/jpg) into build/icon.png (1024) and build/icon.ico.

Usage: python make_icon.py <image> <project-build-dir> [--trim]

--trim   makes a white/near-white background outside the rounded tile transparent
         (flood fill from the corners), for images exported on a solid backdrop.

Also writes icon-preview.png next to the icons: the icon at 16/24/32/48/256 px side by side,
to check it still reads at taskbar size.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]


def trim_background(im: Image.Image) -> Image.Image:
    im = im.copy()
    w, h = im.size
    sentinel = (255, 0, 255, 0)
    for corner in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        r, g, b, a = im.getpixel(corner)
        if a > 0 and min(r, g, b) > 235:
            ImageDraw.floodfill(im, corner, sentinel, thresh=18)
    px = im.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == sentinel:
                px[x, y] = (0, 0, 0, 0)
    return im


def square(im: Image.Image, margin: float = 0.04) -> Image.Image:
    # Crop to the visible tile, then centre it on a square canvas with a small margin.
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    w, h = im.size
    side = max(w, h)
    pad = int(side * margin)
    canvas = Image.new("RGBA", (side + 2 * pad, side + 2 * pad), (0, 0, 0, 0))
    canvas.paste(im, ((side - w) // 2 + pad, (side - h) // 2 + pad), im)
    return canvas


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        sys.exit(1)
    src, out_dir = Path(args[0]), Path(args[1])
    out_dir.mkdir(parents=True, exist_ok=True)

    im = Image.open(src).convert("RGBA")
    if "--trim" in sys.argv:
        im = trim_background(im)
    icon = square(im).resize((1024, 1024), Image.LANCZOS)

    icon.save(out_dir / "icon.png")
    icon.save(out_dir / "icon.ico", sizes=[(s, s) for s in ICO_SIZES])

    preview_sizes = [16, 24, 32, 48, 256]
    gap = 24
    sheet = Image.new("RGBA", (sum(preview_sizes) + gap * (len(preview_sizes) + 1), 256 + 2 * gap), (250, 249, 245, 255))
    x = gap
    for s in preview_sizes:
        thumb = icon.resize((s, s), Image.LANCZOS)
        sheet.paste(thumb, (x, gap + (256 - s) // 2), thumb)
        x += s + gap
    sheet.save(out_dir / "icon-preview.png")

    print(f"ok: {out_dir / 'icon.png'}, {out_dir / 'icon.ico'}, {out_dir / 'icon-preview.png'}")


if __name__ == "__main__":
    main()
