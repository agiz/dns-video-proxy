dns-video-proxy
===============

Hijack popular video hosting sites and get stream with youtube-dl.

```
+-----------+                +------------+         
|           |   youtube.com  | /etc/hosts |         
|  browser  +-------1--------> bind,      |         
|           <-------2--------+ dnsmasq... |         
+--^--+-----+   127.0.0.2    +------------+         
   |  |                                             
   |  |     +---------------+        +--------------+
   |  |     |  http server  +----5--->  youtube-dl  |
   |  +--3--> 127.0.0.2:443 <----6---+ original url |
   +-----4--+               | stream |              |
       204  +-------------+-+        +--------------+
                          |                         
                          |                         
                          +----7---> mpv/mplayer    
```

### Steps

- 1. Browser issues DNS request for youtube.com.
- 2. DNS request is intercepted with your local DNS daemon.
- 3. http(s) request is transfered to 127.0.0.2.
- 4. http response 204 (no content) is issued immediately.
- 5. Original url is passed to youtube-dl.
- 6. url of the stream is sent back to http server.
- 7. Server starts your favorite player.

### Important

Server needs (self signed) certificate.

### /etc/hosts example

```127.0.0.2 youtube.com```

### Start

run http-video-server.bat
