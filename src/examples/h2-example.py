"""Simple h2 connections
Adapted from "Plain Sockets Example Client"
https://python-hyper.org/projects/h2/en/stable/plain-sockets-example.html
"""
import socket
import ssl
import certifi

import h2.connection
import h2.events


SERVER_NAME = 'localhost'
SERVER_PORT = 443


def make_http2_request():
    # Create a generic socket and SSL configuration
    socket.setdefaulttimeout(15)
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.set_alpn_protocols(['h2'])

    # Required to skip certificate validation
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Dump SSL keys to file
    ctx.keylog_filename = 'h2-keylog.log'

    # Open socket and initiate TLS/SSL connection
    s = socket.create_connection((SERVER_NAME, SERVER_PORT))
    s = ctx.wrap_socket(s, server_hostname=SERVER_NAME)

    # Create HTTP/2 connection
    c = h2.connection.H2Connection()
    c.initiate_connection()
    s.sendall(c.data_to_send())

    # Create and send headers
    headers = [
        (':method', 'GET'),
        (':path', '/'),
        (':authority', SERVER_NAME),
        (':scheme', 'https'),
    ]
    c.send_headers(
        stream_id=1,
        headers=headers,
        end_stream=True
    )
    s.sendall(c.data_to_send())

    # Stream response body
    body = b''
    response_stream_ended = False
    while not response_stream_ended:
        # Read raw socket data
        data = s.recv(65536 * 1024)
        if not data:
            break

        # Feed raw data into h2 and process events
        events = c.receive_data(data)
        for event in events:
            print(event)
            if isinstance(event, h2.events.DataReceived):
                # Update flow control
                c.acknowledge_received_data(event.flow_controlled_length, event.stream_id)
                # Append data to response body
                body += event.data
            if isinstance(event, h2.events.StreamEnded):
                response_stream_ended = True
                break

        # Send pending data to the server
        s.sendall(c.data_to_send())

    print('Response fully received:')
    print(body.decode())

    # Close connection and socket
    c.close_connection()
    s.sendall(c.data_to_send())
    s.close()


def main():
    make_http2_request()


if __name__ == '__main__':
    main()
