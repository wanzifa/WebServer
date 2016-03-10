#coding:utf-8
"""利用python的socket模块实现一个最简单的web服务器
"""

from socket import *

HOST, PORT = '', 8888

#定义一个面向流的TCP套接字对象
listen_socket = socket(AF_INET, SOCK_STREAM)
#对套接字对象进行设置，实现套接字对象关闭后，端口号立刻可以被重用.
listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#将套接字地址与套接字对象绑定。
listen_socket.bind((HOST, PORT))
#监听TCP连接，最大允许的连接数目为5.
listen_socket.listen(1)
print 'Serving http on port {0}'.format(PORT)
while True:
    #accept()返回一个新的socket对象，和一个用于处理该客户端请求的新套接字地址。
    client_connection, client_address = listen_socket.accept()
    #接收客户端传来的TCP数据
    request = client_connection.recv(1024)
    print request
    http_response = """
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)
    client_connection.close()
