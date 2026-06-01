#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Get all files in directory
all_files = os.listdir('.')

# Get all HTML files
html_files = sorted([f for f in all_files if f.endswith('.html') or f.endswith('.HTML')])
html_files = [f for f in html_files if f != 'index.html' and f != 'gallery.html']

# Store image mapping for each student
student_data = {}

for html_file in html_files:
    # Extract student ID from filename
    match = re.match(r'(\d+)_\d+_\d+_', html_file)
    if not match:
        continue
    
    student_id = match.group(1)
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
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
                simple_name = os.path.basename(img)
                matching_files = [f for f in all_files if f.startswith(student_id) and f.endswith(simple_name)]
                if matching_files:
                    student_images.append(matching_files[0])
        
        if student_images:
            student_data[html_file] = student_images
    
    except Exception as e:
        print(f"✗ Error reading {html_file}: {e}")

def fix_image_references(content, images, student_id):
    """Fix image src attributes to point to correct files"""
    if not images:
        return content
    
    # Create a mapping of simple filenames to full filenames
    image_map = {}
    for img in images:
        # Extract the simple name (without student ID prefix)
        # Try different patterns
        simple_patterns = [
            re.search(r'\d+_\d+_\d+_(.*)', img),  # studentID_1_2_photo.jpg → photo.jpg
            re.match(r'(.*)', img),  # fallback to full name
        ]
        
        for pattern in simple_patterns:
            if pattern:
                simple_name = pattern.group(1) if pattern.lastindex else img
                if simple_name:
                    image_map[simple_name.lower()] = img
                    # Also map without extension
                    name_no_ext = os.path.splitext(simple_name)[0]
                    image_map[name_no_ext.lower()] = img
                break
        
        # Also map the full filename
        image_map[img.lower()] = img
    
    # Fix quoted src attributes
    def replace_src(match):
        quote = match.group(1)
        old_src = match.group(2)
        
        # Skip URLs
        if old_src.startswith('http') or old_src.startswith('data:') or old_src.startswith('//'):
            return match.group(0)
        
        # If already prefixed with student ID, leave it
        if old_src.startswith(student_id):
            return match.group(0)
        
        # Extract filename and try to find match
        simple_name = os.path.basename(old_src)
        simple_lower = simple_name.lower()
        
        # Try to find in image map
        if simple_lower in image_map:
            new_src = image_map[simple_lower]
            return f'src={quote}{new_src}{quote}'
        
        # Try without extension
        name_no_ext = os.path.splitext(simple_lower)[0]
        if name_no_ext in image_map:
            new_src = image_map[name_no_ext]
            return f'src={quote}{new_src}{quote}'
        
        # No match found, leave as is
        return match.group(0)
    
    # Fix both quoted and unquoted src attributes
    content = re.sub(r'src=(["\'])([^"\']+)\1', replace_src, content, flags=re.IGNORECASE)
    
    # Fix unquoted src (rare but exists)
    def replace_unquoted_src(match):
        old_src = match.group(1)
        
        # Skip URLs
        if old_src.startswith('http') or old_src.startswith('data:') or old_src.startswith('//'):
            return match.group(0)
        
        # If already prefixed with student ID, leave it
        if old_src.startswith(student_id):
            return match.group(0)
        
        # Extract filename and try to find match
        simple_name = os.path.basename(old_src)
        simple_lower = simple_name.lower()
        
        # Try to find in image map
        if simple_lower in image_map:
            new_src = image_map[simple_lower]
            return f'src="{new_src}"'
        
        # Try without extension
        name_no_ext = os.path.splitext(simple_lower)[0]
        if name_no_ext in image_map:
            new_src = image_map[name_no_ext]
            return f'src="{new_src}"'
        
        # No match found, add quotes
        return f'src="{old_src}"'
    
    content = re.sub(r'src=([^\s>"\'][^\s>]*)', replace_unquoted_src, content, flags=re.IGNORECASE)
    
    return content

# Process each HTML file
print("Fixing image references in student HTML files...\n")

for html_file, images in student_data.items():
    match = re.match(r'(\d+)_', html_file)
    if not match:
        continue
    
    student_id = match.group(1)
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix image references
        original_content = content
        content = fix_image_references(content, images, student_id)
        
        # Only write if content changed
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {html_file}: Fixed image references")
            print(f"  Images: {', '.join(images)}")
        else:
            print(f"○ {html_file}: No changes needed")
    
    except Exception as e:
        print(f"✗ Error processing {html_file}: {e}")

print("\n✅ Done!")
