import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

video_folder = os.listdir(r"C:\Users\Erin\webcam website\videos")

class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == "/":
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()

      # Convert the filename into a datatime object:
      for f in video_folder:
        if f.endswith(".mp4"):
          name_only = os.path.splitext(f)[0]   # Remove .mp4
          dt = datetime.strptime(name_only, "%Y%m%d_%H%M%S")
          timestamp = dt.strftime("%B %d, %Y at %I:%M:%S %p")
          month = dt.strftime("%B")

      with open("index.html", "rb") as f:
        self.wfile.write(f.read())

    # If a user clicks on one of the files:
    elif self.path.startswith("/videos/"):
      self.send_response(200)
      self.send_header('Content-type', 'media/avi')
      self.end_headers()
      
      fp = open(f".{self.path}", "rb")
      self.wfile.write(fp.read())
      fp.close()

    elif self.path == "/video-list.json":
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()

      video_data = []

      for f in video_folder:
        if f.endswith(".mp4"):
          name_only = os.path.splitext(f)[0]   # Remove .mp4
          # Convert the filename into a datatime object:
          dt = datetime.strptime(name_only, "%Y%m%d_%H%M%S")
          timestamp = dt.strftime("%B %d, %Y at %I:%M:%S %p")

      #str = json.dumps(video_folder)

          video_data.append({
              "filename": f,
              "timestamp": timestamp
          })

      json_response = json.dumps(video_data, indent=4)
      self.wfile.write(bytes(json_response, "utf-8"))

    elif self.path == "/index.js":
      self.send_response(200)
      self.send_header('Content-type', 'text/javascript')
      self.end_headers()

      with open("index.js", "rb") as f:
        self.wfile.write(f.read())

    elif self.path == "/favicon.ico":
      self.send_response(200)
      self.send_header('Content-type', 'image/x-icon')
      self.end_headers()

      with open('./camera_icon.ico', 'rb') as fp:
        self.wfile.write(fp.read())

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