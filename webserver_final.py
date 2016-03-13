#coding:utf-8
"""
省略的示例中的两段不成功的并发服务器代码，直接写这个最终版了哈哈。
下面这段代码将实现一个可以结束掉所有僵尸进程的并发服务器。
"""

import errno
import os
import signal
import socket

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE =1024

def grim_reaper(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,
                os.WNOHANG
            )
        except OSError:
            return

        if pid == 0:
            return

def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_response = """
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on PORT {port}'.format(port=PORT))

    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            if code == errno.EINTR:
                continue
            else:
                raise

        pid = os.fork()
        if pid == 0:
            listen_socket.close()
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:
            client_connection.close()

if __name__ == '__main__':
    serve_forever()
