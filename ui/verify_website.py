# filename: verify_website.py
# execution: true
import os
import json
import glob

def display_directory_structure(startpath, max_depth=3):
    """Display directory structure in a tree-like format"""
    print(f"\nWebsite Directory Structure (max depth: {max_depth}):")
    
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if level > max_depth:
            continue
            
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")

def count_files_by_type(startpath):
    """Count files by extension"""
    file_counts = {}
    for ext in ['.html', '.js', '.json', '.md']:
        file_counts[ext] = len(glob.glob(f"{startpath}/**/*{ext}", recursive=True))
    return file_counts

def verify_json_files(startpath):
    """Verify JSON files are valid"""
    json_files = glob.glob(f"{startpath}/**/*.json", recursive=True)
    print("\nVerifying JSON files:")
    for file_path in json_files:
        try:
            with open(file_path, 'r') as f:
                json.load(f)
            print(f"  ✅ {os.path.relpath(file_path, startpath)} is valid")
        except json.JSONDecodeError:
            print(f"  ❌ {os.path.relpath(file_path, startpath)} is invalid")

def create_simple_server():
    """Create a simple HTTP server script"""
    server_script = """#!/usr/bin/env python3
import http.server
import socketserver
import os

# Change directory to website
os.chdir('website')

# Set up a simple HTTP server
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

print(f"Starting server at http://localhost:{PORT}")
print("Press Ctrl+C to stop the server")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
"""
    with open('start_server.py', 'w') as f:
        f.write(server_script)
    print("\nCreated start_server.py script")

# Main verification
print("KuralHub Website Verification")
print("=" * 30)

# Check if website directory exists
if not os.path.exists('website'):
    print("❌ Website directory not found!")
else:
    print("✅ Website directory exists")

    # Count files
    file_counts = count_files_by_type('website')
    print("\nFile counts:")
    for ext, count in file_counts.items():
        print(f"  {ext}: {count} files")
    
    # Display directory structure
    display_directory_structure('website')
    
    # Verify JSON files
    verify_json_files('website')
    
    # Create simple server
    create_simple_server()
    
    print("\nWebsite verification complete.")
    print("\nTo test the website locally, run:")
    print("  python start_server.py")
    print("Then open http://localhost:8000 in your web browser")