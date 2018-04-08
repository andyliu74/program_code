# coding:utf8

import struct
from google.protobuf import service
from rpc_controller import RpcController


class RpcParser(object):

	ST_HEAD = 0
	ST_DATA = 1

	def __init__(self, rpc_service, headfmt, indexfmt):
		self._service = rpc_service
		self._headfmt = headfmt
		self._indexfmt = indexfmt
		self._headsize = struct.calcsize(self._headfmt)
		self._indexsize = struct.calcsize(self._indexfmt)

		self._buff = ''
		self._stat = RpcParser.ST_HEAD
		self._datasize = 0

	def feed(self, data):
		rpc_calls = []
		self._buff += data
		while True:
			if self._stat == RpcParser.ST_HEAD:
				if len(self._buff) < self._headsize:
					break
				head_data = self._buff[:self._headsize]
				self._datasize = struct.unpack(self._headfmt, head_data)[0]
				self._buff = self._buff[self._headsize:]
				self._stat = RpcParser.ST_DATA
			if self._stat == RpcParser.ST_DATA:
				if len(self._buff) < self._datasize:
					break
				index_data = self._buff[:self._indexsize]
				request_data = self._buff[self._indexsize:self._datasize]
				index = struct.unpack(self._indexfmt, index_data)[0]
				service_descriptor = self._service.GetDescriptor()
				method_descriptor = service_descriptor.methods[index]
				request = self._service.GetRequestClass(method_descriptor)()
				request.ParseFromString(request_data)
				if not request.IsInitialized():
					raise AttributeError('invalid request data')
				self._buff = self._buff[self._datasize:]
				self._stat = RpcParser.ST_HEAD
				rpc_calls.append((method_descriptor, request))
		return rpc_calls

class RpcChannel(service.RpcChannel):

	HEAD_FMT = '!I'
	INDEX_FMT = '!H'
	HEAD_LEN = struct.calcsize(HEAD_FMT)
	INDEX_LEN = struct.calcsize(INDEX_FMT)

	def __init__(self, conn, rpc_service=None):
		super(RpcChannel, self).__init__()
		self._conn = conn
		self._conn and self._conn.set_rpc_channel(self)
		self._rpc_service = rpc_service
		self._rpc_controller = RpcController(self)

		self._rpc_parser = None
		if rpc_service is not None:
			self._rpc_parser = RpcParser(rpc_service, RpcChannel.HEAD_FMT, RpcChannel.INDEX_FMT)

	def set_rpc_service(self, rpc_service):
		self._rpc_service = rpc_service
		self._rpc_parser = RpcParser(rpc_service, RpcChannel.HEAD_FMT, RpcChannel.INDEX_FMT)

	def on_disconnected(self):
		self._conn = None

	def disconnect(self):
		self._conn and self._conn.disconnect()

	def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
		index = method_descriptor.index
		data = request.SerializeToString()
		size = RpcChannel.INDEX_LEN + len(data)
		self._conn.write(struct.pack(RpcChannel.HEAD_FMT, size))
		self._conn.write(struct.pack(RpcChannel.INDEX_FMT, index))
		self._conn.write(data)

	def receive(self, data):
		try:
			rpc_calls = self._rpc_parser.feed(data)
		except (AttributeError, IndexError):
			print 'error occured when parsing request, give up and disconnect.'
			self.disconnect()
			return

		if not self._rpc_service:
			return

		for method_descriptor, request in rpc_calls:
			self._rpc_service.CallMethod(method_descriptor, self._rpc_controller, request, None)

