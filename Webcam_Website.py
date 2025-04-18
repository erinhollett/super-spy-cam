import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

path = os.listdir(r"C:\Users\Erin\webcam website\videos")

class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == "/":
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()

      # listing the video files:
      video_files = [f for f in path if f.endswith(".avi")]
     
      html = '<html><body><ul>\n'
      for f in video_files:
        html += f'<li><a href="/videos/{f}">{f}</a></li>'
      html += "</ul></body></html>"

      self.wfile.write(bytes(html, 'utf-8'))

    # If a user clicks on one of the files:
    elif self.path.startswith("/videos/"):
      self.send_response(200)
      self.send_header('Content-type', 'media/avi')
      self.end_headers()
      
      fp = open(f".{self.path}", "rb")
      self.wfile.write(fp.read())
      fp.close()

    # If the website doesn't load
    else:
      self.send_response(404)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write(b"not found!")


# === CREATING THE SERVER ===
server_address = ('', 8000) 
httpd = HTTPServer(server_address, MyHandler)

print("Server running at http://localhost:8000/")
httpd.serve_forever()