# rr-dev
based on observations made by cloudflare in the excellent blog: https://blog.cloudflare.com/technical-breakdown-http2-rapid-reset-ddos-attack/

no clue if this actually works, but it seems to match the same behavior
mentioned in the blog's pcap, which seems to no longer be available
from their blog link.

## collecting and analyzing
1. start http/2 enabled nginx server:
```
cd server
docker compose up -d
```

2. start capturing traffic in wireshark

3. run poc script:
```
python rr.py
```

4. decode traffic in wireshark using `ssl-keylog.log` as the ssl keyfile
5. compare against the cloudflare blog notes (unless you have the pcap which seems to be gone now)

## notes
server advertises maximum stream concurrency of 128:

![Maximum concurrent streams](.img/maxstreams.png)

1000 stream headers are sent split into two packets:

![Wireshark packet list](.img/packets.png)

>Interestingly, the RST_STREAM for stream 1051 doesn't fit in packet 15, so in packet 16 we see the server respond with a 404 response.  Then in packet 17 the client does send the RST_STREAM, before moving on to sending the remaining 475 requests.

despite exceeding maximum number of advertised streams, the server never sends a RST_FRAME:

![No RST_STREAM frames from server](.img/ynoreset.png)

> No server RST_STREAM frames are seen in this trace, indicating that the server did not observe a concurrent stream violation. 

obviously to weaponize it, it will take some extra effort like implementing concurrency. but don't do
that shit for any reason other than research. i'm saying this explicitly because
we've seen examples of "illegal code" before. i do this solely for research, and fun of
course, because c'mon this shit is so interesting.

## greetz
greetz to psyk0, shifty, and slerig. who needa stop slackin, but i still love em anyway.
