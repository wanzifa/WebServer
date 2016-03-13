import argparse
import errno
import os
import socket

SERVER_ADDRESS = '', 8888
REQUEST = """
GET /hello HTTP/1.1
Host: localhost:8888

"""

def main(max_clients, max_conns):
    socks = []
    for client_num in range(max_clients):
        pid = os.fork()
        if pid == 0:
            for connection_num in range(max_conns):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(SERVER_ADDRESS)
                sock.sendall(REQUEST)
                socks.append(sock)
                print(connection_num)
        os._exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test client for LSBAWS',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
            '--max-conns',
            type=int,
            default=1024,
            help='Maximum number of connections per client.'
    )
    parser.add_argument(
            '--max-clients',
            type=int,
            default=1,
            help='Maximum number of clients.'
    )
    args = parser.parse_args()
    print args
    main(args.max_clients, args.max_conns)
