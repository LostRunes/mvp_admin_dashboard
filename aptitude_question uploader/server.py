import os
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from supabase import create_client

# ---------------------------------------------------------
# LOAD CREDENTIALS
# ---------------------------------------------------------
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "supabase", ".env"))
if os.path.exists(env_path):
    load_dotenv(env_path)

SUPABASE_URL = os.getenv("SOURCE_SUPABASE_URL", "https://hoihnpzdlivaoywrshmk.supabase.co")
SUPABASE_KEY = os.getenv("SOURCE_SUPABASE_SERVICE_KEY")

if not SUPABASE_KEY:
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvaWhucHpkbGl2YW95d3JzaG1rIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMwNzUyMCwiZXhwIjoyMDkyODgzNTIwfQ.yAOUceRqgb6mxcq_p9GDHhq34vriYlk2uZY-qOPOBsY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------------------------------------
# HTTP API HANDLER
# ---------------------------------------------------------
class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging to keep output clean, but print errors
        if args and len(args) > 1 and str(args[1]).startswith(('4', '5')):
            print(f"Error request: {format % args}")

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # 1. API: Get all topics
        if path == "/api/topics":
            try:
                res = supabase.table("aptitude_topics").select("*").order("name").execute()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res.data).encode())
            except Exception as e:
                self.send_error_response(str(e))

        # 2. API: Get questions for a topic (with options)
        elif path == "/api/questions":
            query = parse_qs(parsed_url.query)
            topic_id = query.get("topic_id", [None])[0]
            if not topic_id:
                self.send_error_response("Missing topic_id parameter", 400)
                return

            try:
                # Select questions and their related options (ordered by id)
                res = supabase.table("aptitude_questions")\
                    .select("id, question_text, explanation, aptitude_options(id, option_text, is_correct)")\
                    .eq("topic_id", topic_id)\
                    .order("id")\
                    .execute()
                
                # Sort option records internally so they line up (A, B, C, D)
                for question in res.data:
                    if "aptitude_options" in question:
                        question["aptitude_options"].sort(key=lambda x: x["id"])

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res.data).encode())
            except Exception as e:
                self.send_error_response(str(e))

        # 3. Serve index.html
        elif path == "/" or path == "/index.html":
            try:
                index_path = os.path.join(os.path.dirname(__file__), "index.html")
                with open(index_path, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_error_response(f"Failed to load index.html: {e}", 500)

        # 4. 404 handler
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def send_error_response(self, msg, code=500):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"error": msg}).encode())

# ---------------------------------------------------------
# RUN SERVER
# ---------------------------------------------------------
def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    url = f"http://localhost:{port}"
    print("=========================================================")
    print("APTITUDE EXPLORER LOCAL SERVER")
    print(f"Running at: {url}")
    print("Press Ctrl+C to stop.")
    print("=========================================================")
    
    # Automatically open the web browser
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()

if __name__ == "__main__":
    run()
