#!/usr/bin/env python3
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
