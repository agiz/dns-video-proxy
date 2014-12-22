import sys
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer
from SocketServer import ThreadingMixIn
import ssl
import subprocess
import threading
import urllib
import urllib2
import urlparse

yt_ip = '194.152.31.227'
"""TOOD: Query DNS Server to resolve?"""

headers = { 'Host' : 'www.youtube.com' }

class MyHandler(SimpleHTTPRequestHandler):
  def do_POST(self):
    parsedParams = urlparse.urlparse(self.path)
    yt_ip_url = 'https://' + yt_ip + '' + parsedParams.path
    req = urllib2.Request(yt_ip_url, parsedParams.query, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    self.send_response(200)
    self.wfile.write(the_page)

  def do_GET(self):
    parsedParams = urlparse.urlparse(self.path)
    yt_parsed = urlparse.parse_qs(parsedParams.query)
    yt_id = ''
    if 'passthrough' in yt_parsed or 'opt_out_ackd' in yt_parsed or \
        'has_verified' in yt_parsed or 'video_id' in yt_parsed or \
        'persist_hl' in yt_parsed:
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      yt_ip_url = 'https://' + yt_ip + '' + parsedParams.path + '?'\
          + parsedParams.query
      req = urllib2.Request(yt_ip_url)
      req.add_header('Host', 'www.youtube.com')
      response = urllib2.urlopen(req)
      the_page = response.read()
      self.wfile.write(the_page)
    else:
      yt_id = ''
      if 'v' not in yt_parsed:
        yt_id = ''
      else:
        yt_id = yt_parsed['v'][0]
        yt_url = 'https://www.youtube.com/watch?v=' + yt_id + '&passthrough=1'
        stdout, stderr = subprocess.Popen(['youtube-dl', '-g', yt_url],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        video_url = stdout.strip()
        subprocess.Popen(['mpv.exe', '--vo=direct3d_shaders', video_url],
            stdout=subprocess.PIPE)
      self.send_response(204)

def test(HandlerClass=MyHandler, ServerClass=BaseHTTPServer.HTTPServer):
  protocol = "HTTP/1.0"
  host = ''
  port = 8000
  cert = ''
  if len(sys.argv) > 1:
    cert = sys.argv[1]
  if len(sys.argv) > 2:
    arg = sys.argv[2]
    if ':' in arg:
      host, port = arg.split(':')
      port = int(port)
    else:
      try:
        port = int(sys.argv[2])
      except:
        host = sys.argv[2]

  server_address = (host, port)

  HandlerClass.protocol_version = protocol
  httpd = ThreadedHTTPServer(server_address, HandlerClass)

  sa = httpd.socket.getsockname()
  httpd.socket = ssl.wrap_socket(httpd.socket, certfile=cert, server_side=True)
  print "Serving HTTP on", sa[0], "port", sa[1], "..."
  httpd.serve_forever()

class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
  """ This class allows to handle requests in separated threads.
    No further content needed, don't touch this. """

if __name__ == "__main__":
  test()
