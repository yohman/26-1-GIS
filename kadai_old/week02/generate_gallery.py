#!/usr/bin/env python3
import json
import html
from pathlib import Path

# Load the data
with open('webmaps_data.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

# Filter out entries without URLs (keep only those with valid web links)
entries = [e for e in entries if e.get('url')]

print(f"Found {len(entries)} entries with URLs")

# Generate main gallery index.html
gallery_html = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Week 2 Web Maps Gallery</title>
    <style>
        body {
            margin: 0;
            padding: 40px 20px;
            background: #fff;
            font-family: 'Courier New', monospace;
        }
        
        h1 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 40px;
            letter-spacing: 2px;
        }
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .entry {
            text-align: center;
            cursor: pointer;
        }
        
        .entry:hover .thumbnail {
            opacity: 0.8;
        }
        
        .thumbnail {
            width: 100%;
            height: 150px;
            background: #f0f0f0;
            border: 2px solid #000;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
            overflow: hidden;
        }
        
        .thumbnail img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .name {
            font-size: 12px;
            margin-top: 5px;
            color: #000;
        }
    </style>
</head>
<body>
    <h1>YOH'S 2026 REITAKU WEB MAPS GALLERY</h1>
    
    <div class="gallery" id="gallery"></div>
    
    <script>
        const entries = ''' + json.dumps(entries, ensure_ascii=False) + ''';
        
        const gallery = document.getElementById('gallery');
        
        entries.forEach(entry => {
            const div = document.createElement('div');
            div.className = 'entry';
            div.onclick = () => window.location.href = `entry_${entry.id}.html`;
            
            const thumb = document.createElement('div');
            thumb.className = 'thumbnail';
            
            // Use padlet image if available
            if (entry.padlet && (entry.padlet.includes('.png') || entry.padlet.includes('.jpg') || entry.padlet.includes('.jpeg'))) {
                const img = document.createElement('img');
                img.src = entry.padlet;
                img.alt = entry.clean_name;
                img.onerror = function() {
                    thumb.innerHTML = 'NO IMAGE';
                };
                thumb.appendChild(img);
            } else {
                thumb.textContent = 'NO IMAGE';
            }
            
            const name = document.createElement('div');
            name.className = 'name';
            name.textContent = entry.clean_name;
            
            div.appendChild(thumb);
            div.appendChild(name);
            gallery.appendChild(div);
        });
    </script>
</body>
</html>
'''

# Write gallery index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(gallery_html)

print("✅ Created index.html")

# Generate individual entry pages
for idx, entry in enumerate(entries):
    prev_entry = entries[idx - 1] if idx > 0 else None
    next_entry = entries[idx + 1] if idx < len(entries) - 1 else None
    
    # Escape HTML in description
    description_escaped = html.escape(entry['description'])
    
    # Create navigation buttons
    nav_buttons = '<div style="position:fixed;top:20px;right:20px;display:flex;gap:5px;z-index:9999;">'
    
    if prev_entry:
        nav_buttons += f'<a href="entry_{prev_entry["id"]}.html" style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;font-family:\'Courier New\',monospace;font-size:12px;">PREV</a>'
    else:
        nav_buttons += '<span style="background:#666;color:#999;padding:10px 20px;font-family:\'Courier New\',monospace;font-size:12px;">PREV</span>'
    
    nav_buttons += '<a href="index.html" style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;font-family:\'Courier New\',monospace;font-size:12px;">HOME</a>'
    
    if next_entry:
        nav_buttons += f'<a href="entry_{next_entry["id"]}.html" style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;font-family:\'Courier New\',monospace;font-size:12px;">NEXT</a>'
    else:
        nav_buttons += '<span style="background:#666;color:#999;padding:10px 20px;font-family:\'Courier New\',monospace;font-size:12px;">NEXT</span>'
    
    nav_buttons += '</div>'
    
    # Determine if we can show an image
    has_image = entry['padlet'] and (entry['padlet'].endswith('.png') or entry['padlet'].endswith('.jpg') or entry['padlet'].endswith('.jpeg') or '.png?' in entry['padlet'] or '.jpg?' in entry['padlet'] or '.jpeg?' in entry['padlet'])
    
    entry_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(entry['clean_name'])} - Web Map</title>
    <style>
        body {{
            margin: 0;
            padding: 40px 20px;
            background: #fff;
            font-family: 'Courier New', monospace;
            max-width: 800px;
            margin: 80px auto 40px;
        }}
        
        h1 {{
            font-size: 20px;
            margin-bottom: 20px;
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
        }}
        
        .image-container {{
            margin: 20px 0;
            border: 2px solid #000;
            padding: 20px;
            background: #f9f9f9;
        }}
        
        .image-container img {{
            max-width: 100%;
            height: auto;
            display: block;
        }}
        
        .description {{
            margin: 20px 0;
            padding: 20px;
            background: #f9f9f9;
            border: 2px solid #000;
            white-space: pre-wrap;
            font-size: 14px;
            line-height: 1.6;
        }}
        
        .link {{
            margin: 20px 0;
            padding: 20px;
            background: #000;
            border: 2px solid #000;
        }}
        
        .link a {{
            color: #fff;
            text-decoration: none;
            font-size: 14px;
            word-break: break-all;
        }}
        
        .link a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    {nav_buttons}
    
    <h1>{html.escape(entry['clean_name'])}</h1>
'''
    
    if has_image:
        entry_html += f'''
    <div class="image-container">
        <img src="{html.escape(entry['padlet'])}" alt="Web map screenshot" onerror="this.parentElement.innerHTML='<p>Image could not be loaded</p>'">
    </div>
'''
    
    entry_html += f'''
    <div class="description">{description_escaped}</div>
    
    <div class="link">
        <a href="{html.escape(entry['url'])}" target="_blank">→ VISIT WEBSITE: {html.escape(entry['url'][:80])}{'...' if len(entry['url']) > 80 else ''}</a>
    </div>
</body>
</html>
'''
    
    with open(f'entry_{entry["id"]}.html', 'w', encoding='utf-8') as f:
        f.write(entry_html)
    
    print(f"✅ Created entry_{entry['id']}.html - {entry['clean_name']}")

print(f"\n✅ Generated {len(entries)} entry pages")
print("✅ All HTML files created successfully!")
