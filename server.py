"""
Sonu Sharma — Personal Portfolio Server
Local development & preview HTTP server providing static asset delivery and REST API endpoints.
"""

import http.server
import socketserver
import os
import json
import urllib.parse
import shutil
import mimetypes
from datetime import datetime, timezone

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Ensure CSS is available in both css/ and chunks/ paths
css_source = os.path.join(DIRECTORY, '_next', 'static', 'css', '2ukvmh6dhhww9.css')
chunks_css = os.path.join(DIRECTORY, '_next', 'static', 'immutable', 'chunks', '2ukvmh6dhhww9.css')
if os.path.exists(css_source) and not os.path.exists(chunks_css):
    os.makedirs(os.path.dirname(chunks_css), exist_ok=True)
    shutil.copy2(css_source, chunks_css)


class PortfolioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # REST API endpoints
        api_mapping = {
            '/api/v1': 'api_v1.json',
            '/api/v1/me': 'api_v1_me.json',
            '/api/v1/skills': 'api_v1_skills.json',
            '/api/v1/experience': 'api_v1_experience.json',
            '/api/v1/projects': 'api_v1_projects.json',
            '/api/v1/education': 'api_v1_education.json',
            '/api/guestbook': 'api_guestbook.json',
            '/api/hit': 'api_hit.json',
        }

        clean_path = path.rstrip('/')
        if clean_path in api_mapping or path in api_mapping:
            fname = api_mapping.get(clean_path, api_mapping.get(path))
            fpath = os.path.join(DIRECTORY, 'api_data', fname)
            if not os.path.exists(fpath):
                fpath = os.path.join(DIRECTORY, 'api', fname)

            if os.path.exists(fpath):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open(fpath, 'rb') as f:
                    self.wfile.write(f.read())
                return

        # CV / Resume download handler
        if path in ['/media/Sonu_Sharma_CV.pdf', '/cv.pdf', '/media/l1BEiug48rCc', '/resume.pdf']:
            cv_path = os.path.join(DIRECTORY, 'media', 'Sonu_Sharma_CV.pdf')
            if not os.path.exists(cv_path):
                cv_path = os.path.join(DIRECTORY, 'cv.pdf')
            if os.path.exists(cv_path):
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                if 'download' in parsed.query:
                    self.send_header('Content-Disposition', 'attachment; filename="Sonu_Sharma_CV.pdf"')
                else:
                    self.send_header('Content-Disposition', 'inline; filename="Sonu_Sharma_CV.pdf"')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open(cv_path, 'rb') as f:
                    self.wfile.write(f.read())
                return

        # Cloudflare email decode fallback
        if 'email-decode' in path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.end_headers()
            self.wfile.write(b'/* email decode */')
            return

        # Favicon fallback
        if path == '/favicon.ico':
            svg_path = os.path.join(DIRECTORY, 'favicon.svg')
            if os.path.exists(svg_path):
                self.send_response(200)
                self.send_header('Content-Type', 'image/svg+xml')
                self.end_headers()
                with open(svg_path, 'rb') as f:
                    self.wfile.write(f.read())
                return

        # Ensure correct MIME types for modern fonts and scripts
        if path.endswith('.woff2'):
            self.send_header_mime = 'font/woff2'
        elif path.endswith('.js'):
            self.send_header_mime = 'application/javascript; charset=utf-8'
        elif path.endswith('.css'):
            self.send_header_mime = 'text/css; charset=utf-8'

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        # Handle guestbook submissions
        if path in ['/api/guestbook', '/api/v1/guestbook']:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            new_entry = None
            try:
                data = json.loads(body) if body else {}
                guestbook_file = os.path.join(DIRECTORY, 'api_data', 'api_guestbook.json')
                if os.path.exists(guestbook_file):
                    with open(guestbook_file, 'r', encoding='utf-8') as f:
                        current = json.load(f)
                    
                    entries = current.get("entries", [])
                    next_id = max((e.get("id", 0) for e in entries), default=0) + 1
                    
                    new_entry = {
                        "id": next_id,
                        "name": data.get("name", "Visitor").strip() or "Visitor",
                        "message": data.get("message", "Visited the portfolio!").strip(),
                        "mood": str(data.get("mood", "200")),
                        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                    }
                    entries.insert(0, new_entry)
                    current["entries"] = entries
                    
                    # Save to both api_data and api directories
                    for fldr in ['api_data', 'api']:
                        target_f = os.path.join(DIRECTORY, fldr, 'api_guestbook.json')
                        if os.path.exists(os.path.dirname(target_f)):
                            with open(target_f, 'w', encoding='utf-8') as f:
                                json.dump(current, f, indent=2)
            except Exception as e:
                print("Error in guestbook POST:", e)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            resp_payload = {
                "status": "ok",
                "id": new_entry["id"] if new_entry else 1,
                "entry": new_entry,
                "message": "Entry added"
            }
            self.wfile.write(json.dumps(resp_payload).encode('utf-8'))
            return

        # Handle visitor hit tracking
        if path == '/api/hit':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"visits": 288}')
            return

        # Handle contact / hire form submissions
        if path in ['/api/hire', '/api/contact']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "message": "Inquiry received"}).encode('utf-8'))
            return

        # Default fallback
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"ok","visits":288}')

    def end_headers(self):
        # Enable CORS and caching headers
        self.send_header('Access-Control-Allow-Origin', '*')
        if hasattr(self, 'send_header_mime'):
            self.send_header('Content-Type', self.send_header_mime)
            del self.send_header_mime
        super().end_headers()


def run_server(port=PORT):
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), PortfolioHandler) as httpd:
        print("=" * 65)
        print("  Sonu Sharma — QA Analyst & Test Automation Portfolio")
        print(f"  Local Dev Server running at: http://localhost:{port}/")
        print("=" * 65)
        print("  Endpoints:")
        print(f"   * UI Portfolio:     http://localhost:{port}/")
        print(f"   * Me API:           http://localhost:{port}/api/v1/me")
        print(f"   * Skills API:       http://localhost:{port}/api/v1/skills")
        print(f"   * Experience API:   http://localhost:{port}/api/v1/experience")
        print(f"   * Projects API:     http://localhost:{port}/api/v1/projects")
        print(f"   * Guestbook API:    http://localhost:{port}/api/guestbook")
        print("=" * 65)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down portfolio server...")


if __name__ == '__main__':
    run_server()
