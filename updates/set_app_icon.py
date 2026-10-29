#!/usr/bin/env python3
"""Create a dependency-free Android vector launcher icon for Wildwood Survival."""
from pathlib import Path
import re

root = Path("app/src/main")
manifest = root / "AndroidManifest.xml"
if not manifest.exists():
    raise SystemExit("AndroidManifest.xml not found")

drawable = root / "res" / "drawable"
drawable.mkdir(parents=True, exist_ok=True)
icon_xml = '''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="#17372B" android:pathData="M0,0h108v108h-108z"/>
    <path android:fillColor="#DCA64A" android:pathData="M0,0h108v5h-108z M0,103h108v5h-108z M0,0h5v108h-5z M103,0h5v108h-5z"/>
    <path android:fillColor="#F4C35C" android:pathData="M73,12a15,15 0,1 0,0.1 0z"/>
    <path android:fillColor="#3F8150" android:pathData="M0,70 L27,29 L52,70 Z"/>
    <path android:fillColor="#275D3B" android:pathData="M23,75 L57,23 L93,75 Z"/>
    <path android:fillColor="#10251D" android:pathData="M0,77 L35,56 L66,78 L108,51 L108,108 L0,108 Z"/>
    <path android:fillColor="#B8F4F4" android:strokeColor="#E9FFFF" android:strokeWidth="1.5" android:pathData="M31,78 L66,34 L73,40 L39,84 Z"/>
    <path android:fillColor="#D7A04A" android:pathData="M31,75 L48,86 L43,92 L26,81 Z"/>
    <path android:fillColor="#83C65B" android:pathData="M14,19 C20,11 29,15 29,22 C23,28 17,26 14,19 Z"/>
</vector>
'''
(drawable / "ic_launcher.xml").write_text(icon_xml, encoding="utf-8")

text = manifest.read_text(encoding="utf-8")
app_match = re.search(r"<application\b[^>]*>", text, flags=re.S)
if not app_match:
    raise SystemExit("Could not find <application> tag in AndroidManifest.xml")
tag = app_match.group(0)
tag = re.sub(r'\s+android:icon="[^"]*"', "", tag)
tag = re.sub(r'\s+android:roundIcon="[^"]*"', "", tag)
tag = tag[:-1] + '\n        android:icon="@drawable/ic_launcher"\n        android:roundIcon="@drawable/ic_launcher">'
text = text[:app_match.start()] + tag + text[app_match.end():]
manifest.write_text(text, encoding="utf-8")
print("Wildwood Survival vector launcher icon generated; no external Python packages required.")
