# -*- coding: utf-8 -*-

from tornado import ioloop
from tornado.tcpserver import TCPServer
from tcp_connection import TCPConnection
from rpc_channel import RpcChannel
from gameserver.rpc_service import ServerService
from gameserver.proto.rpc_pb2 import IServerService_Stub


class TcpServer(TCPServer):

	def __init__(self, ip, port, entity_factory):
		super(TcpServer, self).__init__(io_loop=None)
		self._ip = ip
		self._port = port
		self._entity_factory = entity_factory
		self._entities = {}
		self._connections = {}

	def handle_stream(self, stream, address):
		new_conn = TCPConnection(stream, address, self.io_loop)
		new_channel = RpcChannel(new_conn)
		new_stub = IServerService_Stub(new_channel)
		new_entity = self._entity_factory(new_conn, new_stub)
		new_service = ServerService(new_entity)
		new_channel.set_rpc_service(new_service)
		self._connections[address] = new_conn
		self._entities[address] = new_entity

		new_conn.set_close_callback(lambda _addr=address, _entity=new_entity: self._handle_connection_close(_addr, _entity))
		new_entity.on_connect()
		new_conn.start()

	def get_connection(self, addr):
		return self._connections.get(addr, None)

	def get_entity(self, addr):
		return self._entities.get(addr, None)

	def _handle_connection_close(self, addr, entity):
		entity and entity.on_connect_close()
		self._connections.pop(addr)
		self._entities.pop(addr)

	def start(self):
		self.listen(self._port)
		ioloop.IOLoop.instance().start()
