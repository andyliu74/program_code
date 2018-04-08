# -*- coding: utf-8 -*-

from bson import BSON
from gameserver.proto.rpc_pb2 import Request


class ServerEntity(object):

	def __init__(self, conn, stub):
		self._conn = conn
		self._stub = stub

	def get_address(self):
		return self._conn.address if self._conn else None

	def call_client(self, method_name, *args):
		if not self._stub:
			print 'call_client %s error no stub.' % method_name
			return

		request = Request()
		request.method_name = method_name
		request.request_proto = BSON.encode({'param': args})
		self._stub.call_server(None, request, None)

	def on_connect(self):
		print 'connected to the client.', self._conn.address

	def on_connect_close(self):
		print 'connect is close.'
