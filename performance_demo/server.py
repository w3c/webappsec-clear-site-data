import random
import re
import string
import webapp2

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

class RequestHandler(webapp2.RequestHandler):
  def _random_string(self):
    return "".join(random.choice(string.ascii_lowercase)
                   for i in range(0, 5))

  def get(self):
    self.response.set_status(200)

    # Mime type.
    resource_format = re.match('.*format=([^&]+)', self.request.path_qs).group(1)
    self.response.headers['Content-Type'] = FORMAT_TO_MIME_TYPE[resource_format]

    # Append the Set-Cookie header if the resource was supposed
    # to set cookies.
    resource_type = re.match('.*type=([^&]+)', self.request.path_qs).group(1)
    if resource_type in ['add', 'both']:
      self.response.headers['Set-Cookie'] = (self._random_string() + "=" +
                                             self._random_string())

    # Append the Clear-Site-Data header if requested.
    if resource_type in ['clear', 'both']:
      data_types = (
          self.request.path_qs.split('clear=')[1].split('&')[0].split(','))
      self.response.headers['Clear-Site-Data'] = ', '.join(
          '"%s"' % data_type for data_type in data_types)

    # File contents.
    if resource_format == "iframe":
      # If the resource requested is supposed to add data, complete the HTML
      # template accordingly. Then, pad the file with a lot of data (so that
      # cache grows more quickly), and random data (in case the user agent
      # has a mechanism to deduplicate the same resource being cached multiple
      # times, even if from different URLs).
      add_storage = 'true' if resource_type in ['add', 'both'] else 'false'
      padding = (100000 * 'padding123') + self._random_string()

      self.response.write(RESPONSE_HTML % (add_storage, padding))
      return
    elif resource_format == "img":
      self.response.write(RESPONSE_IMAGE)
      return

    # Bad request.
    self.response.set_status(400)

app = webapp2.WSGIApplication([('/resource', RequestHandler)])
