#!/usr/bin/env python3
"""Rebuild the Week 2 gallery from gallery_entries.json and local thumbnails."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
entries = json.loads((ROOT / 'gallery_entries.json').read_text())
esc = html.escape
cards = []
for e in entries:
    title, name, url = esc(e['title']), esc(e['name']), esc(e['url'], quote=True)
    image = ROOT / 'thumbnails' / f"{e['id']}.png"
    if url:
        preview = (f'<img src="thumbnails/{e["id"]}.png" alt="{title}のウェブサイト" loading="lazy" width="900" height="600">'
                   if image.exists() else '<span class="placeholder">プレビューを取得できませんでした</span>')
        thumb = f'<a class="thumbnail" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{title}（新しいタブで開く）">{preview}<span class="open">サイトを開く ↗</span></a>'
        note = '<p class="note">サイトのトップページにリンク</p>' if e.get('url_note') else ''
    else:
        thumb = '<div class="thumbnail unavailable"><span class="placeholder">リンク未提出<br><small>Website link not provided</small></span></div>'
        note = ''
    desc = e['description']
    if desc == 'No data': desc = '観察コメント未提出 / No observation provided'
    cards.append(f'''<article class="entry">
{thumb}
<h2>{title}</h2><p class="name">{name}</p>{note}
<div class="description" tabindex="0" role="region" aria-label="{name}の観察コメント">{esc(desc)}</div>
</article>''')
page = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Week 2 Web Maps Gallery</title>
<style>
*{box-sizing:border-box}body{margin:0;padding:36px 28px 64px;background:#fff;color:#171717;font-family:Arial,"Noto Sans JP",sans-serif;line-height:1.6}
header{max-width:1360px;margin:0 auto 36px;display:flex;align-items:flex-start;justify-content:space-between;gap:24px}h1{font-family:'Courier New',monospace;font-size:clamp(20px,2.8vw,30px);line-height:1.3;letter-spacing:.04em;margin:10px 0}header p{font-size:13px;color:#666;margin:0}.home{background:#000;color:white;padding:10px 20px;text-decoration:none;font:12px 'Courier New',monospace;flex-shrink:0}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,310px),1fr));gap:40px 28px;max-width:1360px;margin:auto}.entry{min-width:0}.thumbnail{display:block;position:relative;aspect-ratio:3/2;background:#efefef;overflow:hidden;color:#555;text-decoration:none;border:1px solid #ddd}.thumbnail img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}.thumbnail:hover img{opacity:.85}.open{position:absolute;bottom:10px;right:10px;background:#000;color:white;padding:5px 10px;font-size:12px}.placeholder{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;font-size:14px}.placeholder small{font-size:11px;color:#777}.unavailable{border-style:dashed}
h2{font-size:17px;line-height:1.5;overflow-wrap:anywhere;margin:15px 0 4px}.name{font-size:13px;color:#666;margin:0 0 12px}.note{font-size:11px;color:#777;margin:-6px 0 10px}.description{height:230px;overflow:auto;overscroll-behavior:contain;scrollbar-gutter:stable;white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px;line-height:1.85;border-top:1px solid #ddd;padding:12px 8px 8px 0}.description:focus-visible,.thumbnail:focus-visible,.home:focus-visible{outline:2px solid #111;outline-offset:4px}
@media(max-width:600px){body{padding:24px 18px 40px}header{gap:12px}.gallery{gap:32px}.description{height:220px}}
</style>
</head><body>
<header><div><h1>YOH'S 2026 REITAKU<br>WEB MAPS GALLERY</h1><p>WEEK 2 · 気になるウェブ地図と学生の観察</p></div><a class="home" href="../index.html">HOME</a></header>
<main class="gallery">
''' + '\n'.join(cards) + '\n</main></body></html>\n'
(ROOT / 'index.html').write_text(page)
print(f'Built {len(entries)} entries')
