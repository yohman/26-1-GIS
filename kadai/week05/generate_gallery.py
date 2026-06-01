#!/usr/bin/env python
"""
Week 05 Gallery Generator
Fixes file references and generates gallery with navigation

Usage: Run this script from the week05 folder whenever new files are added
       python generate_gallery.py
"""
import os
import re
import json
import openpyxl
from datetime import datetime
from collections import defaultdict

# Change to data directory
os.chdir('data')

# Find Excel file dynamically
excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~')]
if not excel_files:
    print("ERROR: No Excel file found in data folder!")
    exit(1)
excel_file = excel_files[0]

# Read Excel file for student names and dates
print(f"Reading Excel file: {excel_file}")
wb = openpyxl.load_workbook(excel_file)
ws = wb.active

student_info = {}
for row in ws.iter_rows(min_row=2, values_only=True):  # Skip header
    student_id = str(row[0])
    full_name = row[1]  # Format: "Name (Kana)"
    submit_date = row[6]
    comment = row[8] if len(row) > 8 else None  # Column 8 has the comment with Padlet link
    
    # Extract name and katakana - split by Japanese opening parenthesis
    name = f"Student {student_id}"
    katakana = ""
    
    if full_name:
        # Try to split by both ASCII and Japanese parentheses
        if '（' in full_name:
            parts = full_name.split('（')
            name = parts[0].strip()
            if len(parts) > 1:
                katakana = parts[1].rstrip('）').strip()
        elif '(' in full_name:
            parts = full_name.split('(')
            name = parts[0].strip()
            if len(parts) > 1:
                katakana = parts[1].rstrip(')').strip()
        else:
            name = full_name.strip()
    
    # Format date (submit_date is already a string from Excel)
    if submit_date and hasattr(submit_date, 'strftime'):
        date_str = submit_date.strftime('%Y-%m-%d')
    elif isinstance(submit_date, str):
        date_str = submit_date
    else:
        date_str = 'No date'
    
    # Extract Padlet link from comment
    padlet_url = None
    if comment and isinstance(comment, str):
        # Find padlet.com URL in the comment
        padlet_match = re.search(r'https?://padlet\.com/[^\s\n]+', comment)
        if padlet_match:
            padlet_url = padlet_match.group(0)
    
    student_info[student_id] = {
        'name': name,
        'katakana': katakana,
        'date': date_str,
        'padlet': padlet_url
    }

print(f"Loaded {len(student_info)} student records")

# Get all files
files = [f for f in os.listdir('.') if not f.startswith('.') and not f.endswith('.xlsx')]

# Group files by student ID
students = defaultdict(list)
for file in files:
    parts = file.split('_')
    if len(parts) >= 3:
        student_id = parts[0]
        students[student_id].append(file)

# Process each student's files
print("\nProcessing student files...")
for student_id, student_files in sorted(students.items()):
    html_files = [f for f in student_files if f.endswith('.html') or f.endswith('.HTML')]
    css_files = [f for f in student_files if f.endswith('.css')]
    image_files = [f for f in student_files if any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif'])]
    js_files = [f for f in student_files if f.endswith('.js')]
    data_files = [f for f in student_files if any(f.lower().endswith(ext) for ext in ['.csv', '.json', '.geojson', '.txt', '.xml'])]
    
    if not html_files:
        continue
    
    # Process each HTML file (prefer index files)
    index_files = [f for f in html_files if 'index' in f.lower()]
    html_file = index_files[0] if index_files else html_files[0]
    
    print(f"  Processing {html_file}...")
    
    # Read HTML content
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"    Error reading {html_file}: {e}")
        continue
    
    # Clean any existing navigation (start fresh)
    # Remove ALL navigation divs using a helper function to handle nested divs properly
    import re as regex
    
    def remove_navigation_blocks(html_content):
        """Remove all navigation blocks by finding the opening div and matching closing div"""
        marker = 'position:fixed;top:20px;right:20px;z-index:9999'
        cleaned = html_content
        changes_made = False
        
        while marker in cleaned:
            # Find the start of the navigation div
            start_pos = cleaned.find(f'<div style="{marker}')
            if start_pos == -1:
                break
            
            # Find the opening tag end
            opening_tag_end = cleaned.find('>', start_pos)
            if opening_tag_end == -1:
                break
            
            # Count div depth to find the matching closing tag
            depth = 1
            pos = opening_tag_end + 1
            while pos < len(cleaned) and depth > 0:
                if cleaned[pos:pos+4] == '<div':
                    depth += 1
                    pos += 4
                elif cleaned[pos:pos+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        # Found the matching closing tag
                        end_pos = pos + 6
                        cleaned = cleaned[:start_pos] + cleaned[end_pos:]
                        changes_made = True
                        break
                    pos += 6
                else:
                    pos += 1
            
            if depth > 0:
                # Couldn't find matching closing tag, break to avoid infinite loop
                break
        
        return cleaned, changes_made
    
    content, nav_cleaned = remove_navigation_blocks(content)
    
    # Also remove any orphaned button divs that might be left over
    import re as regex
    orphan_pattern = r'^\s*<div style="display:flex;gap:5px;">.*?</div>\s*</div>\s*$'
    old_content = content
    content = regex.sub(orphan_pattern, '', content, flags=regex.MULTILINE | regex.DOTALL)
    if content != old_content:
        nav_cleaned = True
    
    if nav_cleaned:
        print(f"    Cleaned old navigation from {html_file}")
    
    modified = nav_cleaned  # Track if we need to write the file
    
    # Fix CSS references
    if css_files:
        for pattern in ['href="style.css"', "href='style.css'"]:
            if pattern in content:
                css_file = css_files[0]
                quote = '"' if '"' in pattern else "'"
                content = content.replace(pattern, f'href={quote}{css_file}{quote}')
                modified = True
                print(f"    Fixed CSS: style.css -> {css_file}")
    
    # Fix image references
    # Look for src="filename.ext" or src='filename.ext' patterns
    for img_file in image_files:
        # Extract just the original filename (without student ID prefix)
        parts = img_file.split('_')
        if len(parts) >= 3:
            # Get everything after the student_id_number_
            original_name = '_'.join(parts[3:])
            
            # Fix both quoted versions
            for quote in ['"', "'"]:
                patterns = [
                    f'src={quote}{original_name}{quote}',
                    f'src={quote}./{original_name}{quote}',
                ]
                for pattern in patterns:
                    if pattern in content:
                        content = content.replace(pattern, f'src={quote}{img_file}{quote}')
                        modified = True
                        print(f"    Fixed image: {original_name} -> {img_file}")
    
    # Fix JS references
    if js_files:
        for js_file in js_files:
            parts = js_file.split('_')
            if len(parts) >= 3:
                original_name = '_'.join(parts[3:])
                for quote in ['"', "'"]:
                    patterns = [
                        f'src={quote}{original_name}{quote}',
                        f'src={quote}./{original_name}{quote}',
                    ]
                    for pattern in patterns:
                        if pattern in content:
                            content = content.replace(pattern, f'src={quote}{js_file}{quote}')
                            modified = True
                            print(f"    Fixed JS: {original_name} -> {js_file}")
    
    # Fix data file references (CSV, JSON, GeoJSON, TXT, XML)
    if data_files:
        for data_file in data_files:
            parts = data_file.split('_')
            if len(parts) >= 3:
                original_name = '_'.join(parts[3:])
                
                # Fix both quoted versions in various contexts
                for quote in ['"', "'"]:
                    patterns = [
                        # fetch() calls
                        f'fetch({quote}{original_name}{quote})',
                        f'fetch({quote}./{original_name}{quote})',
                        # Direct string references
                        f'{quote}{original_name}{quote}',
                        f'{quote}./{original_name}{quote}',
                    ]
                    for pattern in patterns:
                        replacement_pattern = pattern.replace(original_name, data_file)
                        if pattern in content:
                            content = content.replace(pattern, replacement_pattern)
                            modified = True
                            print(f"    Fixed data file: {original_name} -> {data_file}")
    
    # Write back if modified
    if modified:
        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"    Error writing {html_file}: {e}")

# Generate gallery data
print("\nGenerating gallery data...")
gallery_students = []

for student_id, student_files in sorted(students.items()):
    html_files = [f for f in student_files if f.endswith('.html') or f.endswith('.HTML')]
    image_files = [f for f in student_files if any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif'])]
    
    # Find HTML file (prefer index)
    html_file = None
    if html_files:
        index_files = [f for f in html_files if 'index' in f.lower()]
        html_file = index_files[0] if index_files else html_files[0]
    
    # Find image file (prefer photo)
    image_file = None
    if image_files:
        photo_files = [f for f in image_files if 'photo' in f.lower()]
        image_file = photo_files[0] if photo_files else image_files[0]
    
    # Get student info
    info = student_info.get(student_id, {'name': f'Student {student_id}', 'katakana': '', 'date': 'No date', 'padlet': None})
    
    gallery_students.append({
        'id': student_id,
        'name': info['name'],
        'katakana': info.get('katakana', ''),
        'date': info['date'],
        'html': f'data/{html_file}' if html_file else None,
        'image': f'data/{image_file}' if image_file else None,
        'padlet': info.get('padlet')
    })

# Add navigation buttons to each HTML file
print("\nAdding navigation buttons...")

# Filter to only students with HTML
students_with_html = [s for s in gallery_students if s['html']]

for i, student in enumerate(students_with_html):
    html_file = student['html'].replace('data/', '')
    
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        continue
    
    # Determine prev and next (only among students with HTML)
    prev_student = students_with_html[i - 1] if i > 0 else students_with_html[-1]
    next_student = students_with_html[i + 1] if i < len(students_with_html) - 1 else students_with_html[0]
    
    # Create navigation HTML with student info (including Padlet link if available)
    padlet_link = ''
    if student.get('padlet'):
        padlet_link = f'<div style="font-size:10px;margin-top:5px;"><a href="{student["padlet"]}" target="_blank" style="color:#4CAF50;text-decoration:none;">→ PADLET POST</a></div>'
    
    # Format name display with katakana
    name_display = student['name']
    if student.get('katakana'):
        name_display = f"{student['name']}<br><span style='font-size:9px;color:#999;'>{student['katakana']}</span>"
    
    nav_html = '''<div style="position:fixed;top:20px;right:20px;z-index:9999;">
    <div style="background:#000;color:#fff;padding:10px 20px;margin-bottom:5px;font-family:'Courier New',monospace;font-size:11px;text-align:center;">
        <div style="font-size:10px;color:#999;margin-bottom:3px;">{id}</div>
        <div style="font-size:12px;margin-bottom:3px;">{name}</div>
        <div style="font-size:10px;color:#ccc;">{date}</div>{padlet}
    </div>
    <div style="display:flex;gap:5px;">'''.format(
        id=student['id'],
        name=name_display,
        date=student['date'],
        padlet=padlet_link
    )
    
    prev_file = os.path.basename(prev_student['html'].replace('data/', ''))
    nav_html += f'<a href="{prev_file}" style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;font-family:\'Courier New\',monospace;font-size:12px;">PREV</a>'
    
    nav_html += '<a href="../index.html" style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;font-family:\'Courier New\',monospace;font-size:12px;">HOME</a>'
    
    next_file = os.path.basename(next_student['html'].replace('data/', ''))
    nav_html += f'<a href="{next_file}" style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;font-family:\'Courier New\',monospace;font-size:12px;">NEXT</a>'
    
    nav_html += '</div></div>'
    
    # Insert navigation after <body> tag
    if '<body>' in content:
        content = content.replace('<body>', f'<body>\n{nav_html}\n', 1)
    elif '<body' in content.lower():
        # Handle <body with attributes
        content = re.sub(r'(<body[^>]*>)', r'\1\n' + nav_html + '\n', content, count=1, flags=re.IGNORECASE)
    else:
        # No body tag, add to beginning
        content = nav_html + '\n' + content
    
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Added navigation to {html_file}")
    except Exception as e:
        print(f"  Error writing {html_file}: {e}")

# Write gallery data
gallery_data = {
    'students': gallery_students,
    'generated': datetime.now().isoformat()
}

with open('gallery_data.json', 'w', encoding='utf-8') as f:
    json.dump(gallery_data, f, indent=2, ensure_ascii=False)

print(f"\nGenerated gallery data with {len(gallery_students)} students")
print("Gallery data saved to gallery_data.json")
print("\nDone!")
