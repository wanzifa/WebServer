#coding:utf-8
import socket

SERVER_ADDRESS = (HOST, PORT) = '', 8888
#客户端连接服务器的时候，需要排队
#queue参数设置的是队列容量
REQUEST_QUEUE_SIZE = 5

def handle_request(client_connection):
    #clien_connection是一个专门为当下客户端开辟的socket对象
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
    #允许5个客户端连接排队
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port}'.format(port=PORT))

    while True:
        client_connection, client_address = listen_socket.accept()
        handle_request(client_connection)
        client_connection.close()

if __name__ == '__main__':
    serve_forever()
