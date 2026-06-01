#!/usr/bin/env python3
import csv
import html
import re
import json

def extract_urls(text):
    """Extract all URLs from text"""
    if not text:
        return []
    url_pattern = r'https?://[^\s,<>"\')\]]+(?:[,][^\s<>"\')\]]+)*'
    urls = re.findall(url_pattern, text)
    return urls

def is_google_or_padlet(url):
    """Check if URL is from googleapis or padlet"""
    return 'googleapis.com' in url or 'padlet' in url

def get_urls(title, description, padlet_url):
    """
    Extract both the actual web map URL and screenshot URL
    Returns: (actual_url, screenshot_url)
    
    Logic:
    1. If padlet is an image URL (.png, .jpg, etc.), use it as screenshot
    2. Otherwise, padlet is the actual web map URL
    3. Extract non-image URLs from title/description as actual_url (preferred)
    """
    actual_url = ''
    screenshot_url = ''
    
    # First, check if padlet is an image
    if padlet_url:
        is_image = any(ext in padlet_url.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif'])
        if is_image:
            screenshot_url = padlet_url
        else:
            actual_url = padlet_url
    
    # Check title for URLs
    title_urls = extract_urls(title)
    for url in title_urls:
        is_image = any(ext in url.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif'])
        if is_image:
            if not screenshot_url:
                screenshot_url = url
        else:
            # Non-image URL in title - use as actual URL
            actual_url = url
    
    # Check description for URLs
    desc_urls = extract_urls(description)
    for url in desc_urls:
        is_image = any(ext in url.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif'])
        if is_image:
            # Image URL in description
            if not screenshot_url:
                screenshot_url = url
        else:
            # Non-image URL in description - prefer this over padlet if not already set
            if not actual_url or actual_url == padlet_url:
                actual_url = url
            # If description has more complete version, use it
            elif actual_url and actual_url in url and len(url) > len(actual_url):
                actual_url = url
    
    return actual_url, screenshot_url

# Read the CSV file
entries = []
entry_id = 1
with open('week2 web maps3.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Skip empty rows
        if not (row['title'].strip() or row['description'].strip() or row['author'].strip()):
            continue
            
        # Get both actual URL and screenshot URL
        url, screenshot = get_urls(row['title'], row['description'], row['padlet'])
        
        # Clean author name (extract name without student ID)
        author = row['author']
        clean_name = re.sub(r'\s*\([^)]*\)', '', author).strip()
        clean_name = re.sub(r'\s*\d{10,}.*$', '', clean_name).strip()
        if not clean_name:
            clean_name = author
        
        entries.append({
            'id': entry_id,
            'title': row['title'],
            'description': row['description'],
            'url': url,
            'screenshot': screenshot,
            'padlet': row['padlet'],
            'author': author,
            'clean_name': clean_name
        })
        entry_id += 1

print(f"✅ Found {len(entries)} entries")

# Generate individual entry pages
for idx, entry in enumerate(entries):
    prev_entry = entries[idx - 1] if idx > 0 else None
    next_entry = entries[idx + 1] if idx < len(entries) - 1 else None
    
    # Escape HTML in description but preserve line breaks
    description_escaped = html.escape(entry['description']).replace('\n', '<br>')
    
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
    
    # Create iframe or image display
    content_display = ''
    display_url = entry['url'] if entry['url'] else entry['screenshot']
    screenshot_fallback = entry['screenshot']  # Keep screenshot for fallback
    
    if display_url:
        # Check if URL is an image
        if any(display_url.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
            content_display = f'<img src="{html.escape(display_url)}" style="max-width:100%;height:auto;border:2px solid #000;margin-bottom:20px;" alt="Screenshot">'
        else:
            # If we have both URL and screenshot, show screenshot by default with option to try embedding
            if screenshot_fallback:
                content_display = f'''<div id="content-container" style="margin-bottom:20px;">
    <img src="{html.escape(screenshot_fallback)}" style="max-width:100%;height:auto;border:2px solid #000;" alt="Screenshot">
    <div style="background:#f0f0f0;padding:10px;border:2px solid #000;margin-top:10px;font-size:12px;">
        <button onclick="tryEmbed()" style="background:#000;color:#fff;border:none;padding:8px 16px;font-family:'Courier New',monospace;cursor:pointer;font-size:12px;">▶ Try to embed website</button>
        <span style="margin-left:10px;color:#666;">May not work if the website blocks embedding</span>
    </div>
</div>
<script>
function tryEmbed() {{
    var container = document.getElementById('content-container');
    var embedUrl = {json.dumps(display_url)};
    var fallbackUrl = {json.dumps(screenshot_fallback)};
    
    container.innerHTML = '<iframe id="embed-iframe" src="' + embedUrl + '" style="width:100%;height:600px;border:2px solid #000;"></iframe>' +
        '<div style="background:#f0f0f0;padding:10px;border:2px solid #000;margin-top:10px;font-size:12px;">' +
        '<button onclick="showScreenshot()" style="background:#000;color:#fff;border:none;padding:8px 16px;font-family:\'Courier New\',monospace;cursor:pointer;font-size:12px;">◀ Back to screenshot</button>' +
        '</div>';
}}

function showScreenshot() {{
    var container = document.getElementById('content-container');
    var fallbackUrl = {json.dumps(screenshot_fallback)};
    
    container.innerHTML = '<img src="' + fallbackUrl + '" style="max-width:100%;height:auto;border:2px solid #000;" alt="Screenshot">' +
        '<div style="background:#f0f0f0;padding:10px;border:2px solid #000;margin-top:10px;font-size:12px;">' +
        '<button onclick="tryEmbed()" style="background:#000;color:#fff;border:none;padding:8px 16px;font-family:\'Courier New\',monospace;cursor:pointer;font-size:12px;">▶ Try to embed website</button>' +
        '<span style="margin-left:10px;color:#666;">May not work if the website blocks embedding</span>' +
        '</div>';
}}
</script>'''
            else:
                # No screenshot available, just show iframe
                content_display = f'<div id="content-container" style="margin-bottom:20px;"><iframe src="{html.escape(display_url)}" style="width:100%;height:600px;border:2px solid #000;"></iframe></div>'
    
    # For the link, prefer actual URL over screenshot
    link_url = entry['url'] if entry['url'] else entry['screenshot']
    
    entry_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(entry["title"])} - {html.escape(entry["clean_name"])}</title>
    <style>
        body {{
            margin: 0;
            padding: 60px 20px 20px 20px;
            background: #fff;
            font-family: 'Courier New', monospace;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        h1 {{
            font-size: 20px;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        
        .author {{
            font-size: 14px;
            color: #666;
            margin-bottom: 30px;
        }}
        
        .description {{
            font-size: 14px;
            margin-bottom: 30px;
            white-space: pre-wrap;
            background: #f5f5f5;
            padding: 20px;
            border: 1px solid #ddd;
        }}
        
        .url {{
            font-size: 14px;
            margin-bottom: 20px;
        }}
        
        .url a {{
            color: #0066cc;
            text-decoration: none;
            font-weight: bold;
        }}
        
        .url a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    {nav_buttons}
    
    <div class="container">
        <h1>{html.escape(entry["title"])}</h1>
        <div class="author">by {html.escape(entry["author"])}</div>
        
        {content_display}
        
        <div class="url">
            <a href="{html.escape(link_url) if link_url else '#'}" target="_blank">View Web Map →</a>
        </div>
        
        <div class="description">
            {description_escaped}
        </div>
    </div>
</body>
</html>
'''
    
    with open(f'entry_{entry["id"]}.html', 'w', encoding='utf-8') as f:
        f.write(entry_html)
    
    print(f"✅ Created entry_{entry['id']}.html - {entry['title'][:30]}...")

print(f"\n✅ Done! Generated {len(entries)} entry pages")

# Save entries data for index generation
entries_for_index = []
for entry in entries:
    entries_for_index.append({
        'id': entry['id'],
        'title': entry['title'],
        'clean_name': entry['clean_name'],
        'screenshot': entry['screenshot'],
        'padlet': entry['padlet']  # Include padlet URL as fallback for thumbnails
    })

with open('gallery_data.json', 'w', encoding='utf-8') as f:
    json.dump(entries_for_index, f, ensure_ascii=False, indent=2)

print(f"✅ Saved gallery data to gallery_data.json")
