#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Define the mapping of HTML files to their images (in order)
file_mapping_ordered = [
    ('1254510229_1_2_index.html', ['1254510229_1_1_photo.jpg']),
    ('1254510336_1_1_index.html', ['1254510336_1_2_photo.jpg']),
    ('1254510435_1_1_index.html', ['1254510435_1_2_photo.jpg.jpg']),
    ('1254510534_1_3_index.html', ['1254510534_1_1_dance.jpg', '1254510534_1_2_photo.jpg']),
    ('1254510865_1_2_index.html', ['1254510865_1_1_photo.jpg']),
    ('1254511136_1_1_gis.html', ['1254511136_1_2_photo.jpg']),
    ('1254511160_1_2_index.html', ['1254511160_1_1_photo.jpg']),
    ('1254511251_1_1_index.html', ['1254511251_1_2_photo.jpg']),
    ('1254511805_1_1_gis.html', ['1254511805_1_2_photo.jpg']),
    ('1254511912_1_1_index.html', ['1254511912_1_2_photo.jpg', '1254511912_1_3_スクリーンショット 2026-05-12 12.14.38.png']),
    ('1254690352_1_3_index.html', ['1254690352_1_1_photo.jpg', '1254690352_1_2_IMG_7968.JPG']),
    ('1254690435_1_1_index.html', ['1254690435_1_2_photo.jpeg']),
    ('1254810059_1_1_zzzk_GIS.html', ['1254810059_1_2_ore.jpg']),
    ('1254810075_1_3_index.html', ['1254810075_1_1_photo.jpg', '1254810075_1_2_IMG20240225123513.jpg']),
    ('1254810124_1_1_gis.html', ['1254810124_1_2_photo.jpg']),
    ('1254810166_1_1_index.html', ['1254810166_1_2_IMG_3715.jpg']),
    ('1254810174_1_3_GIS第三回課題REASE.html', ['1254810174_1_1_imageああ.jpg', '1254810174_1_2_image0.jpg']),
    ('1254810182_1_1_index.html', ['1254810182_1_2_photo.jpeg']),
    ('1254810372_1_1_index.html', ['1254810372_1_2_IMG_4545.JPG']),
    ('1254810405_1_1_index.html', ['1254810405_1_2_photo.jpg']),
    ('1254810512_1_1_index.html', ['1254810512_1_2_IMG_7470.jpeg']),
    ('1254810736_1_1_index.html', ['1254810736_1_2_photo.jpg']),
    ('1254810794_1_1_index.html', ['1254810794_1_2_Amaharashi.JPG', '1254810794_1_3_live.jpg', '1254810794_1_4_me.jpeg']),
    ('1254810926_1_1_index.html', ['1254810926_1_2_IMG_5931.jpeg']),
    ('1254810976_1_1_index.html', ['1254810976_1_2_photo.jpg']),
    ('1254810992_1_1_index.html', ['1254810992_1_2_IMG_2169.jpeg', '1254810992_1_3_scuba.gif']),
    ('1254811049_1_1_index.html', ['1254811049_1_2_photo.jpg']),
    ('1254820222_1_3_index.html', ['1254820222_1_1_6436.jpg']),
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
    # Remove nav-container div and everything inside it
    content = re.sub(r'<div id="nav-container">.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
    
    # Remove navigation styles
    content = re.sub(r'<style>\s*/\* Navigation styles \*/.*?</style>', '', content, flags=re.DOTALL)
    
    # Remove navigation scripts
    content = re.sub(r'<script>\s*const currentFile = .*?</script>', '', content, flags=re.DOTALL)
    
    # Fix body margin if it was added
    content = re.sub(r'body\s*\{[^}]*margin-top:\s*60px[^}]*\}', '', content)
    
    return content

def fix_image_references(content, images):
    """Fix image src attributes to point to correct files"""
    if not images:
        return content
    
    # Create a mapping of simple filenames to full filenames
    image_map = {}
    for img in images:
        # Extract the simple filename (after the third underscore)
        parts = img.split('_')
        if len(parts) >= 4:
            simple_name = '_'.join(parts[3:])
            image_map[simple_name] = img
        # Also map the full filename to itself
        image_map[img] = img
    
    # Find all img tags and fix their src (quoted version)
    def replace_src_quoted(match):
        full_tag = match.group(0)
        src_value = match.group(1)
        
        # Skip if src already has the prefix numbers
        if re.match(r'^\d+_\d+_\d+_', src_value):
            return full_tag
        
        # Skip if it's a URL
        if src_value.startswith('http') or src_value.startswith('//'):
            return full_tag
        
        # Check if we have a mapping for this filename
        if src_value in image_map:
            new_src = image_map[src_value]
            return full_tag.replace(f'src="{src_value}"', f'src="{new_src}"').replace(f"src='{src_value}'", f"src='{new_src}'")
        
        return full_tag
    
    # Find all img tags and fix their src (unquoted version)
    def replace_src_unquoted(match):
        full_tag = match.group(0)
        src_value = match.group(1)
        
        # Skip if src already has the prefix numbers
        if re.match(r'^\d+_\d+_\d+_', src_value):
            return full_tag
        
        # Skip if it's a URL
        if src_value.startswith('http') or src_value.startswith('//'):
            return full_tag
        
        # Check if we have a mapping for this filename
        if src_value in image_map:
            new_src = image_map[src_value]
            return full_tag.replace(f'src={src_value}', f'src="{new_src}"')
        
        return full_tag
    
    # Match img tags with quoted src attribute
    content = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', replace_src_quoted, content)
    
    # Match img tags with unquoted src attribute (e.g., src=dance.jpg)
    content = re.sub(r'<img[^>]*src=([^\s">]+)', replace_src_unquoted, content)
    
    return content

def process_html_file(filepath, images, prev_file, next_file):
    """Process an HTML file: remove old nav, fix images, add minimal navigation buttons"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove old navigation
        content = remove_old_navigation(content)
        
        # Remove any existing home/nav buttons (to prevent duplicates)
        content = re.sub(r'<a href="index\.html" style="position:fixed;top:20px;right:20px[^>]*>HOME</a>\s*', '', content)
        content = re.sub(r'<div style="position:fixed;top:20px;right:20px;display:flex[^>]*>.*?</div>', '', content, flags=re.DOTALL)
        
        # Fix image references
        content = fix_image_references(content, images)
        
        # Create navigation buttons
        nav_buttons = create_nav_buttons(os.path.basename(filepath), prev_file, next_file)
        
        # Add navigation buttons right after <body> tag
        if '<body>' in content:
            content = content.replace('<body>', f'<body>\n{nav_buttons}', 1)
        elif '<body' in content:
            # Handle <body with attributes
            content = re.sub(r'(<body[^>]*>)', r'\1\n' + nav_buttons, content, count=1)
        
        # Remove excessive blank lines
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Processed {filepath}")
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    # Get current directory
    current_dir = Path(__file__).parent
    
    print("Starting minimal HTML file updates with navigation...\n")
    
    # Process each HTML file with prev/next navigation
    for idx, (html_file, images) in enumerate(file_mapping_ordered):
        filepath = current_dir / html_file
        
        # Determine prev and next files
        prev_file = file_mapping_ordered[idx - 1][0] if idx > 0 else None
        next_file = file_mapping_ordered[idx + 1][0] if idx < len(file_mapping_ordered) - 1 else None
        
        if filepath.exists():
            process_html_file(filepath, images, prev_file, next_file)
        else:
            print(f"Warning: {html_file} not found")
    
    print("\n✅ All files processed with minimal design and navigation!")

if __name__ == '__main__':
    main()
