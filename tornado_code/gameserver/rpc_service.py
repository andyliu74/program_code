# -*- coding: utf-8 -*-

from bson import BSON
from proto.rpc_pb2 import IServerService


# 被调用方的Service要自己实现具体的rpc处理逻辑
class ServerService(IServerService):

	def __init__(self, entity):
		super(ServerService, self).__init__()
		self._entity = entity

	def call_server(self, rpc_controller, request, callback):
		method_name = request.method_name
		method_params = BSON(request.request_proto).decode()
		try:
			method = getattr(self._entity, method_name, None)
			params = method_params.get('param', [])
			method and method(*params)
		except:
			print 'call_server %s error.' % method_name
