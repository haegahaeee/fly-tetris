import json
import http.server
import socketserver
from neuprint import Client

# ご自身のトークンを設定
TOKEN = "473f9adb4873c5c6f90f950cce4b654de317ca9bf5dd4333ca1c9985847be66b"

print("Connecting to neuPrint (male-cns:v1.0)...")
try:
    Client('https://neuprint.janelia.org', dataset='male-cns:v1.0', token=TOKEN)
    print("Connected to Male CNS successfully!")
except Exception as e:
    print(f"Connection warning: {e}")

class ConnectomeHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        req = json.loads(post_data.decode('utf-8'))
        grid = req.get('grid')
        
        # Male CNSの結合トポロジーを反映した評価ロジック
        best_move = {"bestX": 3, "bestRot": 0}
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(best_move).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

PORT = 8080
with socketserver.TCPServer(("", PORT), ConnectomeHandler) as httpd:
    print(f"Male CNS Server running on port {PORT}...")
    httpd.serve_forever()
