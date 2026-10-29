#!/usr/bin/env python3
"""Generate Android launcher icons for Wildwood Survival and set manifest references."""
from pathlib import Path
import re, subprocess, sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw

root = Path("app/src/main")
manifest = root / "AndroidManifest.xml"
if not manifest.exists():
    raise SystemExit("AndroidManifest.xml not found")

# Create a polished, simple survival-game icon at every legacy launcher density.
sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}
def draw_icon(size):
    im = Image.new("RGB", (size, size), "#17372b")
    d = ImageDraw.Draw(im)
    # rounded-square background
    d.rounded_rectangle((1, 1, size-2, size-2), radius=int(size*.22), fill="#17372b", outline="#dca64a", width=max(1,size//32))
    # sunset
    d.ellipse((size*.56, size*.12, size*.84, size*.40), fill="#f4c35c")
    # layered forest mountains
    d.polygon([(0,size*.67),(size*.26,size*.29),(size*.48,size*.67)], fill="#3f8150")
    d.polygon([(size*.22,size*.69),(size*.53,size*.22),(size*.88,size*.69)], fill="#275d3b")
    d.polygon([(0,size*.73),(size*.34,size*.53),(size*.62,size*.75),(size,size*.48),(size,size),(0,size)], fill="#10251d")
    # sword blade and handle
    d.polygon([(size*.32,size*.76),(size*.62,size*.37),(size*.69,size*.43),(size*.40,size*.81)], fill="#b8f4f4", outline="#e9ffff")
    d.line((size*.35,size*.72,size*.49,size*.81), fill="#d7a04a", width=max(2,size//11))
    d.line((size*.27,size*.80,size*.43,size*.64), fill="#d7a04a", width=max(2,size//10))
    # tiny leaf highlight
    d.ellipse((size*.12,size*.17,size*.27,size*.27), fill="#83c65b")
    return im

for folder, size in sizes.items():
    out = root / "res" / folder
    out.mkdir(parents=True, exist_ok=True)
    icon = draw_icon(size)
    icon.save(out / "ic_launcher.png")
    icon.save(out / "ic_launcher_round.png")

text = manifest.read_text(encoding="utf-8")
app_match = re.search(r"<application\b[^>]*>", text, flags=re.S)
if not app_match:
    raise SystemExit("Could not find <application> tag in AndroidManifest.xml")
tag = app_match.group(0)
tag = re.sub(r'\s+android:icon="[^"]*"', "", tag)
tag = re.sub(r'\s+android:roundIcon="[^"]*"', "", tag)
tag = tag[:-1] + '\n        android:icon="@mipmap/ic_launcher"\n        android:roundIcon="@mipmap/ic_launcher_round">'
text = text[:app_match.start()] + tag + text[app_match.end():]
manifest.write_text(text, encoding="utf-8")
print("Wildwood Survival launcher icons generated and AndroidManifest.xml updated.")
