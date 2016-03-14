#coding:utf-8
"""
省略的示例中的两段不成功的并发服务器代码，直接写这个最终版了哈哈。
下面这段代码将实现一个可以结束掉所有僵尸进程的并发服务器。
"""

#errno模块提供了许多错误对应的符号错误码
import errno
import os
#signal模块可以提供捕捉子进程结束信号的方法
import signal
import socket

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE =1024

#这个函数是捕捉到子进程退出信号后的处理函数
def grim_reaper(signum, frame):
    while True:
        try:
            #注意该函数与os.wait()的区别
            #os.wait()会形成在没有子进程结束的时候阻塞，这时候它什么也不返回，但进程不能干别的事情.
            #waitpid()中写入WNOHANG参数后，它就会在返回完所有的结束的子进程的终止信息之后，返回pid=0，不会阻塞进程.
            #第一个参数设置了waitpid函数不等待特定的子进程，而是等待并处理每一个子进程.
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
""" #注意sendall和send的区别，sendall一次发送完所有的tcp数据
    #而send则不一定会一次性发送完，可能需要分多次发送，所以一般需要一个while函数
    client_connection.sendall(http_response)

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on PORT {port}'.format(port=PORT))
   
    #设置一个信号处理器，用于捕捉并处理已经结束的子进程.
    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            #IOError会返回一个错误对象，这个错误对象的args属性会返回一个错误码和对应的错误信息
            code, msg = e.args
            #EINTR错误会返回一个中断的系统调用的错误码
            if code == errno.EINTR:
                continue
            else:
                raise
        
        #fork函数将会复制现在运行的这个进程，复制产生的这个进程叫做子进程，原来那个进程变成了父进程
        #复制完成后，子进程父进程同步向下运行，子进程里返回的pid是0,父进程返回的是子进程的pid
        pid = os.fork()
        if pid == 0:
            listen_socket.close()
            handle_request(client_connection)
            client_connection.close()
            #退出子进程
            os._exit(0)
        else:
            client_connection.close()

if __name__ == '__main__':
    serve_forever()
