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
5. compare against the cloudflare blog notes (unless you have the pcap which seems to be gone now)

## notes
no clue if this actually works, but it seems to match the same behavior
mentioned in the cloudflare blog.

obviously to weaponize it, it will take some extra effort like multithreading but i sure as fuck
am not releasing a weaponized version fo free.

greets to psyk0, slerig, and all the other juggalols out there
