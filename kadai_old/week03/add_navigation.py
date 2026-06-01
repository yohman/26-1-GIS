#!/usr/bin/env python3
import os
import re

# Ordered list of HTML files based on the scan results
ordered_files = [
    '1254510229_1_2_index.html',
    '1254510336_1_1_index.html',
    '1254510435_1_1_index.html',
    '1254510534_1_3_index.html',
    '1254510865_1_2_index.html',
    '1254511136_1_1_gis.html',
    '1254511160_1_2_index.html',
    '1254511251_1_1_index.html',
    '1254511805_1_1_gis.html',
    '1254511912_1_1_index.html',
    '1254690352_1_3_index.html',
    '1254690435_1_1_index.html',
    '1254810059_1_1_zzzk_GIS.html',
    '1254810075_1_3_index.html',
    '1254810124_1_1_gis.html',
    '1254810140_1_1_inedx.HTML',
    '1254810166_1_1_index.html',
    '1254810174_1_3_GIS第三回課題REASE.html',
    '1254810182_1_1_index.html',
    '1254810372_1_1_index.html',
    '1254810405_1_1_index.html',
    '1254810512_1_1_index.html',
    '1254810736_1_1_index.html',
    '1254810794_1_1_index.html',
    '1254810801_1_2_index.html',
    '1254810827_1_1_index.html',
    '1254810926_1_1_index.html',
    '1254810976_1_1_index.html',
    '1254810992_1_1_index.html',
    '1254811049_1_1_index.html',
    '1254820222_1_3_index.html',
]

def create_nav_buttons(current_file, prev_file, next_file):
    """Create navigation buttons HTML"""
    nav_html = '<div style="position:fixed;top:20px;right:20px;display:flex;gap:5px;z-index:9999;">'
    
    if prev_file:
        nav_html += f'<a href="{prev_file}" style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;font-family:\'Courier New\',monospace;font-size:12px;">PREV</a>'
    else:
        nav_html += '<span style="background:#666;color:#999;padding:10px 20px;font-family:\'Courier New\',monospace;font-size:12px;">PREV</span>'
    
    nav_html += '<a href="index.html" style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;font-family:\'Courier New\',monospace;font-size:12px;">HOME</a>'
    
    if next_file:
        nav_html += f'<a href="{next_file}" style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;font-family:\'Courier New\',monospace;font-size:12px;">NEXT</a>'
    else:
        nav_html += '<span style="background:#666;color:#999;padding:10px 20px;font-family:\'Courier New\',monospace;font-size:12px;">NEXT</span>'
    
    nav_html += '</div>'
    return nav_html

def remove_old_navigation(content):
    """Remove old navigation elements"""
    # Remove any existing navigation divs with position:fixed at top-right
    content = re.sub(r'<div style="position:fixed;top:20px;right:20px[^>]*>.*?</div>', '', content, flags=re.DOTALL)
    return content

print("Adding navigation buttons to student HTML files...\n")

for i, html_file in enumerate(ordered_files):
    if not os.path.exists(html_file):
        print(f"⚠ {html_file}: File not found, skipping")
        continue
    
    # Determine prev and next files
    prev_file = ordered_files[i-1] if i > 0 else None
    next_file = ordered_files[i+1] if i < len(ordered_files)-1 else None
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove old navigation
        content = remove_old_navigation(content)
        
        # Create new navigation
        nav_html = create_nav_buttons(html_file, prev_file, next_file)
        
        # Insert navigation after <body> tag
        if '<body' in content.lower():
            # Find the body tag (case insensitive, multiline)
            body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE | re.DOTALL)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n    ' + nav_html + '\n' + content[insert_pos:]
        
        # Write updated content
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {html_file}")
        if prev_file:
            print(f"  ← {prev_file}")
        if next_file:
            print(f"  → {next_file}")
    
    except Exception as e:
        print(f"✗ Error processing {html_file}: {e}")

print("\n✅ Done! Added navigation to all student pages.")
