#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Define the mapping of HTML files to their images
file_mapping = {
    '1254510229_1_2_index.html': ['1254510229_1_1_photo.jpg'],
    '1254510336_1_1_index.html': ['1254510336_1_2_photo.jpg'],
    '1254510435_1_1_index.html': ['1254510435_1_2_photo.jpg.jpg'],
    '1254510534_1_3_index.html': ['1254510534_1_1_dance.jpg', '1254510534_1_2_photo.jpg'],
    '1254510865_1_2_index.html': ['1254510865_1_1_photo.jpg'],
    '1254511136_1_1_gis.html': ['1254511136_1_2_photo.jpg'],
    '1254511160_1_2_index.html': ['1254511160_1_1_photo.jpg'],
    '1254511251_1_1_index.html': ['1254511251_1_2_photo.jpg'],
    '1254511805_1_1_gis.html': ['1254511805_1_2_photo.jpg'],
    '1254511912_1_1_index.html': ['1254511912_1_2_photo.jpg', '1254511912_1_3_スクリーンショット 2026-05-12 12.14.38.png'],
    '1254690352_1_3_index.html': ['1254690352_1_1_photo.jpg', '1254690352_1_2_IMG_7968.JPG'],
    '1254690435_1_1_index.html': ['1254690435_1_2_photo.jpeg'],
    '1254810059_1_1_zzzk_GIS.html': ['1254810059_1_2_ore.jpg'],
    '1254810075_1_3_index.html': ['1254810075_1_1_photo.jpg', '1254810075_1_2_IMG20240225123513.jpg'],
    '1254810124_1_1_gis.html': ['1254810124_1_2_photo.jpg'],
    '1254810166_1_1_index.html': ['1254810166_1_2_IMG_3715.jpg'],
    '1254810174_1_3_GIS第三回課題REASE.html': ['1254810174_1_1_imageああ.jpg', '1254810174_1_2_image0.jpg'],
    '1254810182_1_1_index.html': ['1254810182_1_2_photo.jpeg'],
    '1254810372_1_1_index.html': ['1254810372_1_2_IMG_4545.JPG'],
    '1254810405_1_1_index.html': ['1254810405_1_2_photo.jpg'],
    '1254810512_1_1_index.html': ['1254810512_1_2_IMG_7470.jpeg'],
    '1254810736_1_1_index.html': ['1254810736_1_2_photo.jpg'],
    '1254810794_1_1_index.html': ['1254810794_1_2_Amaharashi.JPG', '1254810794_1_3_live.jpg', '1254810794_1_4_me.jpeg'],
    '1254810926_1_1_index.html': ['1254810926_1_2_IMG_5931.jpeg'],
    '1254810976_1_1_index.html': ['1254810976_1_2_photo.jpg'],
    '1254810992_1_1_index.html': ['1254810992_1_2_IMG_2169.jpeg', '1254810992_1_3_scuba.gif'],
    '1254811049_1_1_index.html': ['1254811049_1_2_photo.jpg'],
    '1254820222_1_3_index.html': ['1254820222_1_1_6436.jpg'],
}

def extract_name_from_html(filepath):
    """Extract the name from an HTML file's <h1> tag"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to find <h1> tag
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
        if h1_match:
            name = h1_match.group(1)
            # Clean up the name - remove HTML tags, extra whitespace
            name = re.sub(r'<[^>]+>', '', name)
            name = re.sub(r'\s+', ' ', name).strip()
            
            # Remove common placeholder text
            if 'ここに自分の名前' in name or name == '':
                return None
            
            return name
        
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def main():
    current_dir = Path(__file__).parent
    
    print("const students = [")
    
    for html_file, images in file_mapping.items():
        filepath = current_dir / html_file
        if filepath.exists():
            name = extract_name_from_html(filepath)
            student_id = html_file.split('_')[0]
            first_image = images[0]
            
            if name:
                print(f"    {{id: '{student_id}', name: '{name}', file: '{first_image}', html: '{html_file}'}},")
            else:
                print(f"    {{id: '{student_id}', name: 'Student {student_id}', file: '{first_image}', html: '{html_file}'}},")
    
    print("];")

if __name__ == '__main__':
    main()
