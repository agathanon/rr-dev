# rr-dev

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

## notes
no clue if this actually works, but it seems to match the same behavior
mentioned in the cloudflare blog.

greets to psyk0, slerig, and all the other juggalols out there
