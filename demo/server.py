import http.server
import re

class RequestHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    # Cache-Control: only-if-cached indicates that the browser should never
    # fetch the resource over network. Unfortunately, this is not widely
    # supported. If such a request reaches the server, simply ignore it.
    if 'cache-control' in self.headers:
      if self.headers['cache-control'] == 'only-if-cached':
        return

    self.send_response(200)  # OK
    self.send_header('Content-Type', 'text/html')
    self.send_header('Cache-Control', 'max-age=86400')
    self.end_headers()

    # The '?resource=<number>' requests are used to populate the cache.
    if re.match('^/\?resource=\d+', self.path):
      self.wfile.write('resource')
      return

    # Otherwise, just serve index.html, as that is the only page we have.
    self.wfile.write(open('index.html', "r").read().encode())

  def do_POST(self):
    # Serve index.html as usual, but with Clear-Site-Data as instructed
    # through the POST attributes.

    # Input: "types=cookies&types=cache"
    post_data = self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8")
    # Transformation: ['cookies', 'cache']
    datatypes = re.findall('types=([^&]+)', post_data)
    # Output: '"cookies","cache"'
    datatypes = ','.join('"%s"' % datatype for datatype in datatypes)

    self.send_response(200)  # OK
    self.send_header('Content-Type', 'text/html');
    self.send_header('Clear-Site-Data', datatypes)
    self.end_headers()

    self.wfile.write(open('index.html', "r").read().encode())


if __name__ == "__main__":
  httpd = http.server.HTTPServer(('', 8000), RequestHandler)
  httpd.serve_forever()
