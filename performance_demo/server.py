import BaseHTTPServer
import random
import re
import string

FORMAT_TO_MIME_TYPE = {
  'img': 'image/svg+xml',
  'iframe': 'text/html'
}

RESPONSE_IMAGE = (
    '''<?xml version="1.0"?>
         <!-- Tick on a green background indicates success. -->
         <svg height="20" width="20" style="stroke: black; stroke-width: 2;"
             xmlns="http://www.w3.org/2000/svg"
             xmlns:xlink="http://www.w3.org/1999/xlink">
         <polygon points="0,0 0,19, 19,19, 19,0" style="fill: lightgreen;" />
         <polyline points="3,10 7,15 15,3" style="fill: none;"/>
        </svg>
      '''
)

RESPONSE_HTML = (
    '''
      <html>
        <head>
          <style>
            body {
              background-color: lightgreen;
              margin: 0;
              overflow: hidden;
            }
          </style>
        </head>
        <body>
          &#9745; <!-- Tick on a green background indicates success. -->
          <script>
            var set_storage = %s;
            if (set_storage) {
              localStorage.setItem(Math.random(), Math.random())
            }
          </script>
          <!-- Padding to make the file larger. %s -->
        </body>
      </html>
    '''
)

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def _random_string(self):
    return "".join(random.choice(string.ascii_lowercase)
                   for i in range(0, 5))

  def do_GET(self):
    # Serve the index page directly.
    if self.path in ["", "/", "/index.html"]:
      self.send_response(200)  # OK
      self.send_header('Content-Type', 'text/html')
      self.end_headers()
      self.wfile.write(file('index.html').read())
      return

    # Serve the various resources.
    if 'resource' in self.path:
      self.send_response(200)

      # Mime type.
      resource_format = re.match('.*format=([^&]+)', self.path).group(1)
      self.send_header('Content-Type', FORMAT_TO_MIME_TYPE[resource_format])

      # Append the Set-Cookie header if the resource was supposed
      # to set cookies.
      resource_type = re.match('.*type=([^&]+)', self.path).group(1)
      if resource_type in ['add', 'both']:
        self.send_header('Set-Cookie',
                         self._random_string() + "=" + self._random_string())

      # Append the Clear-Site-Data header if requested.
      if resource_type in ['clear', 'both']:
        self.send_header('Clear-Site-Data', '"cookies", "storage", "cache"')
      self.end_headers()

      # File contents.
      if resource_format == "iframe":
        # If the resource requested is supposed to add data, complete the HTML
        # template accordingly. Then, pad the file with a lot of data (so that
        # cache grows more quickly), and random data (in case the user agent
        # has a mechanism to deduplicate the same resource being cached multiple
        # times, even if from different URLs).
        add_storage = 'true' if resource_type in ['add', 'both'] else 'false'
        padding = (100000 * 'padding123') + self._random_string()

        self.wfile.write(RESPONSE_HTML % (add_storage, padding))
        return
      elif resource_format == "img":
        self.wfile.write(RESPONSE_IMAGE)
        return

    # Bad request.
    self.send_response(400)

if __name__ == '__main__':
  httpd = BaseHTTPServer.HTTPServer(('', 8000), RequestHandler)
  httpd.serve_forever()

