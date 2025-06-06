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

      # listing the video files:
      html_videos = ""

      # Convert the filename into a datatime object:
      for f in video_folder:
        if f.endswith(".mp4"):
          name_only = os.path.splitext(f)[0]   # Remove .mp4
          dt = datetime.strptime(name_only, "%Y%m%d_%H%M%S")
          timestamp = dt.strftime("%B %d, %Y at %I:%M:%S %p")
          month = dt.strftime("%B")

          # Creating the dynamic HTML to display the videos:
          html_videos += f"""

          <li>{month}
              <ul>
                  <li>
                    <a href="/videos/{f}">{timestamp}</a>
                    <video controls width="250">
                      <source src="/videos/{f}" type="video/mp4" />
                    </video>
                  </li>
              </ul>
          </li>
          """
      # Creating the general HTML template for the static elements:
      html_template = """
      <!DOCTYPE html>
      <html>
      <head>
          <title>Super Spy Cam</title>\n
          <script type="text/javascript">

          function makeVideoGoOnScreen(videoObject) {
            
            ///// START --- ERIN PUT ALL YOUR CODE BELOW THIS LINE AND ABOVE END

            console.log('hello world tho');
            console.log(videoObject);
            
            function willpringle(erin) {
              console.log(erin == 'lovely');
            }

            console.log(willpringle("lovely"));



            //// END
          }


          const myPromise = fetch("http://localhost:8000/video-list.json");
          myPromise
            .then(res => res.text())
            .then(txt => makeVideoGoOnScreen(JSON.parse(txt)));

          </script>
      </head>
      <body>
          <h1>Super Spy Cam</h1>
          <h2>Captured Videos:</h2>
          <ul>""" + html_videos + """
          </ul>
      </body>
      </html>
      """

      self.wfile.write(bytes(html_template, 'utf-8'))

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
    
    '''elif self.path == "/wkp":
      self.send_response(200)
      self.send_header('Content-Type', 'text/html')
      self.end_headers()

      # read the file from the hard drive,
      fp = open('./index.html', 'r') # as a string
      html_string = fp.read()
      print(html_string)
      self.wfile.write(bytes(html_string, 'utf-8'))
  '''



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