#!/usr/bin/env python3
import csv
import re

def extract_urls(text):
    """Extract all URLs from text"""
    if not text:
        return []
    # Pattern to match URLs
    url_pattern = r'https?://[^\s,<>"\')\]]+(?:\?[^\s<>"\')\]]*)?'
    urls = re.findall(url_pattern, text)
    return urls

def is_google_or_padlet(url):
    """Check if URL is from googleapis or padlet"""
    return 'googleapis.com' in url or 'padlet' in url

def get_best_url(title, description, padlet_url):
    """
    Extract the best URL to use:
    1. First check title and description for non-Google/Padlet URLs
    2. If none found, use the existing padlet_url
    """
    # Combine title and description
    combined_text = f"{title} {description}"
    
    # Extract all URLs
    all_urls = extract_urls(combined_text)
    
    # Filter out Google/Padlet URLs
    non_google_padlet_urls = [url for url in all_urls if not is_google_or_padlet(url)]
    
    # If we found a non-Google/Padlet URL, use the first one
    if non_google_padlet_urls:
        return non_google_padlet_urls[0]
    
    # Otherwise, keep the original padlet URL
    return padlet_url

# Read the CSV
input_file = 'week2 web maps.csv'
output_file = 'week2 web maps.csv'

rows = []
changes = []

with open(input_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        original_url = row['padlet']
        new_url = get_best_url(row['title'], row['description'], row['padlet'])
        
        if new_url != original_url:
            changes.append({
                'line': i,
                'title': row['title'][:50],
                'old': original_url[:60] if original_url else 'None',
                'new': new_url[:60]
            })
        
        row['padlet'] = new_url
        rows.append(row)

# Write back to CSV
with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
    fieldnames = ['title', 'description', 'padlet', 'author']
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)

# Print summary
print(f"✅ Processed {len(rows)} entries")
print(f"✅ Found {len(changes)} entries with alternative URLs\n")

if changes:
    print("Changes made:")
    for change in changes:
        print(f"\nRow {change['line']}: {change['title']}...")
        print(f"  OLD: {change['old']}...")
        print(f"  NEW: {change['new']}...")
