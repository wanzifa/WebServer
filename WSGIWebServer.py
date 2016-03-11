#coding:utf-8
"""
编写一个可以提供WSGI接口的web服务器
Web服务器一旦遵循了WSGI协议，就可以与所有的现代Python Web框架无缝对接！
从此Web服务器就可以和Python Web框架愉快地生活在一起，无障碍交流！
"""

from socket import *
import StringIO
import sys

class WSGIServer(object):

    #IP地址遵循IPv4协议
    address_family = AF_INET
    #传输层协议选取TCP协议(stream就是“面向流”的协议的暗示)
    socket_type = SOCK_STREAM
    #最多允许服务器建立1个连接
    request_queue_size = 1

    def __init__(self, server_address):
        #创建一个socket对象,和webserver.py里面的实现方法一样
        self.listen_socket = listen_socket = socket(
            self.address_family,
            self.socket_type
        )
        #对当前套接字对象进行设置，指定它一旦运行结束就立刻释放它绑定的端口号
        listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        #绑定套接字地址
        listen_socket.bind(server_address)
        #设置允许套接字对象建立的连接数为1
        listen_socket.listen(self.request_queue_size)
        #得到服务器自己的ip地址和端口号
        host, port = self.listen_socket.getsockname()[:2]
        #将使用点号分隔的ip地址转换为一个完整的域名
        self.server_name = getfqdn(host)
        self.server_port = port
        #建立一个空列表，里面下面会装Http头部进去哟～～
        self.heaers_set = []

    def set_app(self, application):
        #把框架里面的应用传进来
        self.application = application

    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            #创建一个新的与客户端之间的连接
            self.client_connection, client_address = listen_socket.accept()
            self.handle_one_request()

    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)
        print (''.join(
            '{line}\n'.format(line=line)
            for line in request_data.splitlines()
        ))
        self.parse_request(request_data)
        
        #获取环境字典
        env = self.get_environ()
        
        #此处application方法会返回一个响应
        result = self.application(env, self.start_response)
        
        #将响应传入下面一个专门处理响应的函数中
        self.finish_response(result)

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        #将请求内容拆分
        (self.request_method,
         self.path,
         self.request_version
        ) = request_line.split()

    def get_environ(self):
        env = {}
        env['wsgi.version'] = (1,0)
        env['wsgi.url_scheme'] = 'http'
        #StringIO对象和file文件对象挺像的，这里实例化这个对象应该是为了方便对它进行文件化的操作
        env['wsgi.input'] = StringIO.StringIO(self.request_data)
        #系统错误输出
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.run_once'] = False
        #下面是CGI规范所需的一些参数
        env['REQUEST_METHOD'] = self.request_method
        env['PATH_INFO'] = self.path
        env['SERVER_NAME'] = self.server_name
        env['SERVER_PORT'] = str(self.server_port)
        return env

    def start_response(self, status, response_headers, exc_info=None):
        #加入必要的服务器头部
        server_headers = [
                ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
                ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{0}, {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data
            print (''.join(
                '{line}\n'.format(line=line)
                for line in response.splitlines()
            ))
            #向客户端返回数据
            self.client_connection.sendall(response)
        finally:
            #关闭针对客户端建立的套接字对象
            self.client_connection.close()

SERVER_ADDRESS = (HOST, PORT) = '',8888

def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    #和import作用相同
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print('WSGIServer:Serving HTTP on port {port}...\n'.format(port=PORT))
    httpd.serve_forever()  
