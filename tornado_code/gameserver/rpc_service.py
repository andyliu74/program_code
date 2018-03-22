# -*- coding: utf-8 -*-

from bson import BSON
from proto.rpc_pb2 import IServerService


# 被调用方的Service要自己实现具体的rpc处理逻辑
class ServerService(IServerService):

	def call_server(self, rpc_controller, request, callback):
		print 'call_server:'
		print rpc_controller.rpc_channel
		print request.method_name
		method_params = BSON(request.request_proto).decode()
		print method_params
