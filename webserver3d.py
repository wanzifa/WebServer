"""
与服务器3c的代码几乎没有什么区别
需要注意的是serve_forever里面父进程里客户端套接字对象这次没有被及时的关闭
"""

#coding:utf-8
import os 
import socket

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(
            'Child PID:{pid}.Parent PID {ppid}'.format(
                pid=os.getpid(),
                ppid=os.getppid(),
        )
    )
    print(request.decode())
    http_response = """
HTTP/1.1 200 OK

Hello world!
"""
    client_connection.sendall(http_response)

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port}....'.format(port=PORT))
    print('Parent PID (PPID):{pid}\n'.format(pid=os.getpid()))
    
    clients = []
    while True:
        client_connection, client_address = listen_socket.accept()
        clients.append(client_connection)
        pid = os.fork()
        if pid == 0:
            listen_socket.close()
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:
            #把关闭为客户端专门创建的socket的对象的操作注释掉了
            #client_connection.close()
            print(len(clients))

if __name__ == '__main__':
    serve_forever()

