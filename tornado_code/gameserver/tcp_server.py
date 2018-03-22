# -*- coding: utf-8 -*-

from tornado import ioloop
from entity import Entity
from tornado.tcpserver import TCPServer
from tcp_connection import TCPConnection
from rpc_channel import RpcChannel

class TcpServer(TCPServer):

	def __init__(self, ip, port, service_factory):
		super(TcpServer, self).__init__(io_loop=None)
		self._port = port
		self._service_factory = service_factory
		self._entities = {}

	def handle_stream(self, stream, address):
		new_conn = TCPConnection(stream, address, self.io_loop)
		RpcChannel(new_conn, self._service_factory())
		new_entity = Entity(new_conn)
		self._entities[address] = new_entity
		new_conn.start()

	def start(self):
		self.listen(self._port)
		ioloop.IOLoop.instance().start()

	def stop(self):
		pass