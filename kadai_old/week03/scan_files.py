#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Get all files in directory
all_files = os.listdir('.')

# Get all HTML files
html_files = sorted([f for f in all_files if f.endswith('.html') or f.endswith('.HTML')])
html_files = [f for f in html_files if f != 'index.html' and f != 'gallery.html']

students = []

for html_file in html_files:
    # Extract student ID from filename
    match = re.match(r'(\d+)_\d+_\d+_', html_file)
    if not match:
        continue
    
    student_id = match.group(1)
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract name from h1 tag
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        name = 'Unknown'
        if h1_match:
            name = h1_match.group(1)
            # Clean HTML tags and whitespace
            name = re.sub(r'<[^>]+>', '', name)
            name = ' '.join(name.split())
        
        # Find all image references
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        img_matches = re.findall(img_pattern, content, re.IGNORECASE)
        
        # Filter and map images
        student_images = []
        for img in img_matches:
            # Skip URLs and data URIs
            if img.startswith('http') or img.startswith('data:') or img.startswith('//'):
                continue
            
            # Check if image starts with student ID (already prefixed)
            if img.startswith(student_id):
                student_images.append(img)
            else:
                # Try to find the actual file with student ID prefix
                # Look for files that match pattern: studentID_*_*_imagename
                simple_name = os.path.basename(img)
                matching_files = [f for f in all_files if f.startswith(student_id) and f.endswith(simple_name)]
                if matching_files:
                    student_images.append(matching_files[0])
        
        # Use first image as thumbnail, or try to find photo variant
        thumbnail = None
        if student_images:
            # Prefer images with 'photo' in the name
            photo_imgs = [img for img in student_images if 'photo' in img.lower()]
            if photo_imgs:
                thumbnail = photo_imgs[0]
            else:
                thumbnail = student_images[0]
        
        if thumbnail:
            students.append({
                'id': student_id,
                'name': name,
                'file': thumbnail,
                'html': html_file,
                'all_images': student_images
            })
            print(f"✓ {student_id}: {name}")
            print(f"  HTML: {html_file}")
            print(f"  Thumbnail: {thumbnail}")
            if len(student_images) > 1:
                print(f"  Other images: {', '.join(student_images[1:])}")
        else:
            print(f"⚠ {student_id}: {name} - No images found")
            print(f"  HTML: {html_file}")
    
    except Exception as e:
        print(f"✗ Error reading {html_file}: {e}")

print(f"\n✅ Found {len(students)} students with images")

# Generate JavaScript array
print("\n// JavaScript array for index.html:")
print("const students = [")
for student in students:
    # Escape single quotes in names
    safe_name = student['name'].replace("'", "\\'")
    print(f"    {{id: '{student['id']}', name: '{safe_name}', file: '{student['file']}', html: '{student['html']}'}},")
print("];")
