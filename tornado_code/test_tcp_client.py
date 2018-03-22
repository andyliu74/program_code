# -*- coding: utf-8 -*-

import socket
from bson import BSON
import tornado.ioloop
import tornado.iostream
from gameserver.proto.rpc_pb2 import IServerService_Stub, Request
from gameserver.rpc_channel import RpcChannel
from gameserver.tcp_connection import TCPConnection


class TCPClient(object):
    def __init__(self, host, port, io_loop=None):
        self.host = host
        self.port = port
        self.io_loop = io_loop
        self.shutdown = False
        self.stream = None
        self.sock_fd = None

    def get_stream(self):
        self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(self.sock_fd)
        self.stream.set_close_callback(self.on_close)

    def connect(self):
        self.get_stream()
        self.conn = TCPConnection(self.stream, (self.host, self.port), self.io_loop)
        self.channel = RpcChannel(self.conn)
        self.stub = IServerService_Stub(self.channel)
        self.stream.connect((self.host, self.port), self.send_message)

    def on_receive(self, data):
        self.stream.close()

    def on_close(self):
        if self.shutdown:
            self.io_loop.stop()
        
    def send_message(self):
        request = Request()
        request.method_name = 'test_method_name'
        request.request_proto = BSON.encode({'name': 'andy', 'age': 28})
        self.stub and self.channel and self.stub.call_server(None, request, None)

    def set_shutdown(self):
        self.shutdown = True


def main():
    io_loop = tornado.ioloop.IOLoop.instance()
    c1 = TCPClient("127.0.0.1", 8888, io_loop)
    c2 = TCPClient("127.0.0.1", 8888, io_loop)

    c1.connect()
    c2.connect()

    io_loop.start()

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()
