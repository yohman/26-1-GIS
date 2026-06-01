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

# Navigation CSS and JS to be inserted
navigation_code = '''
<style>
    /* Navigation styles */
    #nav-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    #nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    #home-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        font-size: 14px;
        transition: transform 0.2s;
    }
    
    #home-btn:hover {
        transform: scale(1.05);
    }
    
    #toggle-filmstrip {
        background: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        font-size: 14px;
        transition: transform 0.2s;
    }
    
    #toggle-filmstrip:hover {
        transform: scale(1.05);
    }
    
    #filmstrip {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
        background: #f5f5f5;
    }
    
    #filmstrip.open {
        max-height: 150px;
    }
    
    #filmstrip-content {
        display: flex;
        gap: 10px;
        padding: 15px;
        overflow-x: auto;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .filmstrip-item {
        flex-shrink: 0;
        cursor: pointer;
        transition: transform 0.2s;
        border: 3px solid transparent;
    }
    
    .filmstrip-item:hover {
        transform: scale(1.1);
        border-color: #667eea;
    }
    
    .filmstrip-item.active {
        border-color: #764ba2;
    }
    
    .filmstrip-item img {
        width: 100px;
        height: 100px;
        object-fit: cover;
        border-radius: 6px;
        display: block;
    }
    
    /* Add top margin to body to account for fixed nav */
    body {
        margin-top: 60px;
    }
</style>

<div id="nav-container">
    <div id="nav-bar">
        <button id="home-btn" onclick="window.location.href='index.html'">🏠 ホーム</button>
        <button id="toggle-filmstrip" onclick="toggleFilmstrip()">📷 他の写真を見る</button>
    </div>
    <div id="filmstrip">
        <div id="filmstrip-content"></div>
    </div>
</div>

<script>
    const currentFile = '{{CURRENT_FILE}}';
    const images = {{IMAGES}};
    const currentImgParam = new URLSearchParams(window.location.search).get('img');
    
    // Create filmstrip
    const filmstripContent = document.getElementById('filmstrip-content');
    images.forEach((img, index) => {
        const item = document.createElement('div');
        item.className = 'filmstrip-item';
        if (currentImgParam === img || (!currentImgParam && index === 0)) {
            item.classList.add('active');
        }
        item.onclick = () => {
            window.location.href = `${currentFile}?img=${img}`;
        };
        item.innerHTML = `<img src="${img}" alt="Thumbnail ${index + 1}">`;
        filmstripContent.appendChild(item);
    });
    
    // Toggle filmstrip
    function toggleFilmstrip() {
        document.getElementById('filmstrip').classList.toggle('open');
    }
    
    // Update image source based on URL parameter
    if (currentImgParam || images.length > 0) {
        const targetImg = currentImgParam || images[0];
        
        // Update image source based on URL parameter
        document.querySelectorAll('img').forEach(img => {
            const src = img.getAttribute('src');
            // Check if src is a simple filename (no path, no prefix numbers)
            if (src && !src.includes('/') && !src.match(/^[0-9]+_[0-9]+_[0-9]+_/)) {
                // Replace with the prefixed version
                const matchingImg = images.find(i => {
                    const simpleName = i.split('_').slice(3).join('_');
                    return src === simpleName || src === i;
                });
                if (matchingImg) {
                    img.setAttribute('src', matchingImg);
                }
            }
        });
    }
</script>
'''

def process_html_file(filepath, images):
    """Add navigation to an HTML file and fix image references"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already processed
        if 'nav-container' in content:
            print(f"Skipping {filepath} - already processed")
            return
        
        # Prepare the navigation code with file-specific data
        filename = os.path.basename(filepath)
        nav_code = navigation_code.replace('{{CURRENT_FILE}}', filename)
        nav_code = nav_code.replace('{{IMAGES}}', str(images).replace("'", '"'))
        
        # Insert navigation right after <body> tag
        if '<body>' in content:
            content = content.replace('<body>', f'<body>\n{nav_code}\n', 1)
        elif '<body' in content:
            # Handle <body with attributes
            content = re.sub(r'(<body[^>]*>)', r'\1\n' + nav_code + '\n', content, count=1)
        else:
            print(f"Warning: No <body> tag found in {filepath}")
            return
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Processed {filepath}")
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    # Get current directory
    current_dir = Path(__file__).parent
    
    print("Starting HTML file updates...\n")
    
    # Process each HTML file
    for html_file, images in file_mapping.items():
        filepath = current_dir / html_file
        if filepath.exists():
            process_html_file(filepath, images)
        else:
            print(f"Warning: {html_file} not found")
    
    print("\n✅ All files processed!")

if __name__ == '__main__':
    main()
