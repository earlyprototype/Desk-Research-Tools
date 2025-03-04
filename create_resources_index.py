#!/usr/bin/env python3
"""
Create an index.html file for the HTML_Resources directory to make it easy to browse
the converted PDF files.
"""

import os
import glob
import sys
import re
from datetime import datetime

def create_index_html(resources_dir, output_file, title="PDF Resources", css_paths=None, js_paths=None):
    """
    Create an index.html file for the resources directory.
    
    Args:
        resources_dir (str): Directory containing HTML files
        output_file (str): Path where index.html will be saved
        title (str): Page title
        css_paths (list): List of CSS files to include
        js_paths (list): List of JavaScript files to include
    """
    # Get all HTML files in the directory
    html_files = glob.glob(os.path.join(resources_dir, "*.html"))
    html_files = [f for f in html_files if os.path.basename(f) != "index.html"]
    
    # Sort files alphabetically
    html_files.sort(key=lambda x: os.path.basename(x).lower())
    
    # Start building the HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
"""
    
    # Add CSS links
    if css_paths and isinstance(css_paths, list):
        for css_path in css_paths:
            if os.path.exists(css_path):
                rel_path = os.path.relpath(css_path, os.path.dirname(output_file))
                html_content += f'    <link rel="stylesheet" href="{rel_path}">\n'
    
    # Add additional CSS
    html_content += """    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .resources-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .resource-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            background-color: #f9f9f9;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .resource-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .resource-card h3 {
            margin-top: 0;
            color: #333;
        }
        .resource-card p {
            color: #666;
            font-size: 0.9em;
        }
        .resource-card a {
            display: inline-block;
            margin-top: 10px;
            color: #0066cc;
            text-decoration: none;
        }
        .resource-card a:hover {
            text-decoration: underline;
        }
        .last-updated {
            text-align: right;
            color: #666;
            font-size: 0.8em;
            margin-top: 30px;
        }
        header {
            margin-bottom: 30px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        nav {
            margin-top: 15px;
        }
        nav a {
            margin-right: 15px;
            color: #333;
            text-decoration: none;
        }
        nav a:hover {
            text-decoration: underline;
        }
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <header>
        <h1>{title}</h1>
        <nav>
            <a href="../index.html">Home</a>
            <a href="../blog/index.html">Blog</a>
        </nav>
    </header>
    
    <main>
        <p>These PDF resources have been converted to HTML format for easier access and reference.</p>
        
        <div class="resources-container">
"""
    
    # Add a card for each HTML file
    for html_file in html_files:
        filename = os.path.basename(html_file)
        name = os.path.splitext(filename)[0]
        
        # Format the name for display (replace underscores with spaces, etc.)
        display_name = re.sub(r'[_\-]', ' ', name)
        
        # Get file size in KB
        try:
            size_kb = os.path.getsize(html_file) / 1024
            size_str = f"{size_kb:.1f} KB"
        except:
            size_str = "Unknown size"
        
        # Get last modified date
        try:
            mod_time = os.path.getmtime(html_file)
            mod_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
        except:
            mod_date = "Unknown date"
        
        html_content += f"""            <div class="resource-card">
                <h3>{display_name}</h3>
                <p>Size: {size_str}</p>
                <p>Modified: {mod_date}</p>
                <a href="{filename}">View Document</a>
            </div>
"""
    
    # Close the main content
    html_content += """        </div>
        
        <p class="last-updated">Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </main>
    
    <footer>
        <p>&copy; FactoryXChange Skills Project</p>
    </footer>
"""
    
    # Add JavaScript
    if js_paths and isinstance(js_paths, list):
        for js_path in js_paths:
            if os.path.exists(js_path):
                rel_path = os.path.relpath(js_path, os.path.dirname(output_file))
                html_content += f'    <script src="{rel_path}"></script>\n'
    
    # Close the HTML
    html_content += """</body>
</html>
"""
    
    # Write the file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created index file at {output_file} with {len(html_files)} resources.")

def main():
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python create_resources_index.py <resources_directory> [output_file] [title]")
        return 1
    
    resources_dir = sys.argv[1]
    
    if not os.path.isdir(resources_dir):
        print(f"Error: {resources_dir} is not a valid directory.")
        return 1
    
    output_file = os.path.join(resources_dir, "index.html")
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    
    title = "PDF Resources"
    if len(sys.argv) >= 4:
        title = sys.argv[3]
    
    # Create the index file
    create_index_html(resources_dir, output_file, title)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 