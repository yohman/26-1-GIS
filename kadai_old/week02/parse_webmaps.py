#!/usr/bin/env python3
import csv
import re
import json

def extract_url_from_text(text):
    """Extract URL from text using regex"""
    if not text:
        return None
    
    # Look for URLs starting with http or https
    url_pattern = r'https?://[^\s,"\'\n]+'
    match = re.search(url_pattern, text)
    if match:
        url = match.group(0)
        # Clean up common trailing characters
        url = re.sub(r'[,。、；!?]+$', '', url)
        return url
    return None

def clean_author_name(author):
    """Extract clean author name, remove student IDs"""
    if not author:
        return "Unknown"
    
    # Remove parentheses with student IDs
    name = re.sub(r'\([^)]*\)', '', author)
    # Remove leading/trailing whitespace
    name = name.strip()
    # If empty after cleanup, return original
    return name if name else author

# Read CSV and extract data
entries = []
with open('week2 web maps.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader, 1):
        title = row.get('title', '').strip()
        description = row.get('description', '').strip()
        padlet = row.get('padlet', '').strip()
        author = row.get('author', '').strip()
        
        # Extract URL from description
        url = extract_url_from_text(description)
        
        # If no URL in description, try the padlet field (but prefer description)
        if not url and padlet.startswith('http'):
            url = padlet
        
        # Clean author name
        clean_name = clean_author_name(author)
        
        entry = {
            'id': idx,
            'title': title if title else f"Entry {idx}",
            'description': description,
            'url': url,
            'padlet': padlet,
            'author': author,
            'clean_name': clean_name
        }
        
        entries.append(entry)
        
        print(f"{idx}. {clean_name}: {title}")
        print(f"   URL: {url}")
        print()

# Save to JSON for later use
with open('webmaps_data.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print(f"✅ Extracted {len(entries)} entries")
print(f"✅ Saved to webmaps_data.json")
