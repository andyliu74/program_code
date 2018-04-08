# -*- coding: utf-8 -*-

import socket
import tornado.ioloop
import tornado.iostream
from proto.rpc_pb2 import IServerService_Stub
from rpc_channel import RpcChannel
from rpc_service import ServerService
from tcp_connection import TCPConnection


class TCPClient(object):
    def __init__(self, host, port, entity_factory, io_loop=None):
        self.host = host
        self.port = port
        self.conn = None
        self.entity_factory = entity_factory
        self._close_callback = None
        self._connect_callback = None

        if io_loop is None:
            self.io_loop = tornado.ioloop.IOLoop.instance()
        else:
            self.io_loop = io_loop

    def connect(self, callback=None):
        sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = tornado.iostream.IOStream(sock_fd)
        self.conn = TCPConnection(stream, (self.host, self.port), self.io_loop)
        channel = RpcChannel(self.conn)
        stub = IServerService_Stub(channel)
        entity = self.entity_factory(self.conn, stub)
        self._entity = entity
        service = ServerService(entity)
        channel.set_rpc_service(service)

        self._connect_callback = callback
        self.conn.set_close_callback(lambda _entity=entity : self._on_connect_close(_entity))
        stream.connect((self.host, self.port), lambda _entity=entity : self._on_connect(_entity))

    def get_entity(self):
        return self._entity

    def set_close_callback(self, callback):
        self._close_callback = callback

    def _on_connect(self, entity):
        entity and entity.on_connect()
        if self._connect_callback:
            callback = self._connect_callback
            callback()
        self._connect_callback = None

        self.conn and self.conn.start()

    def _on_connect_close(self, entity):
        entity and entity.on_connect_close()
        if self._close_callback is not None:
            callback = self._close_callback
            callback()
            self._close_callback = None
        self._connect_callback = None
        self.conn = None

