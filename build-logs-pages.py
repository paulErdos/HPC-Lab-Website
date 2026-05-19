#!/usr/bin/env python3 

import os

TEMPLATE_FILE = 'template.log.html'
OUTPUT_FILE = 'log.html'
POSTS_DIR = 'posts-source'

def build_articles():
    # Ensure the articles directory exists
    if not os.path.exists('articles'):
        os.makedirs('articles')
        
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(POSTS_DIR, filename), 'r') as f:
                content = f.read()
            
            slug = filename.replace('.txt', '.html')
            
            # Simple article page structure
            article_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../log-style.css">
    <title>HPC Lab | {filename.replace('.txt', '').replace('-', ' ').title()}</title>
</head>
<body>
<div class="wrapper">
    <nav><a href="../log.html">&larr; BACK TO LOGS</a></nav>
    <pre>{content}</pre>
</div>
</body>
</html>"""
            
            with open(os.path.join('articles', slug), 'w') as f:
                f.write(article_html)

def build_log():
    # Load your skeleton HTML
    with open(TEMPLATE_FILE, 'r') as f:
        template = f.read()

    # Generate tiles
    tiles = []
    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith('.txt'):
            title = filename.replace('.txt', '').replace('-', ' ').title()
            slug = filename.replace('.txt', '.html')
            
            # Simple, clean insertion
            tiles.append(f'''
            <div class="tile">
                <h3>{title}</h3>
                <p>Build log entry for {title}.</p>
                <a href="articles/{slug}">Read Entry</a>
            </div>''')

    # Inject and save
    # Assumes template.log.html has a placeholder like <!-- TILES_HERE -->
    content = template.replace('<!-- TILES_HERE -->', "".join(tiles))
    
    with open(OUTPUT_FILE, 'w') as f:
        f.write(content)

import re


import time

def generate_log_table():
    output_file = 'log_rows.html'
    rows = []
    
    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith('.txt'):
            # Get creation time from the source .txt file
            file_path = os.path.join(POSTS_DIR, filename)
            c_time = os.path.getctime(file_path)
            date = time.strftime('%Y-%m-%d', time.localtime(c_time))
            
            # Use filename for title
            title = filename.replace('.txt', '').replace('-', ' ').title()
            slug = filename.replace('.txt', '.html')
            
            rows.append(f'''        <tr class="log-row">
            <td class="log-date">{date}</td>
            <td><a href="articles/{slug}" class="log-link">{title}</a></td>
        </tr>''')

    with open(output_file, 'w') as f:
        f.write('\n'.join(rows))

if __name__ == "__main__":
    build_articles()
    build_log()
    generate_log_table()
