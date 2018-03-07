#-- coding: utf-8 -*-


class Channel(object):

	# 普通通道
	CHANNEL_NORMAL = 0,
	# 浏览器web通道
	CHANNEL_WEB = 1,

	def __init__(self, ninterface=None, endpoint=None, protocol_type="TCP", channel_id=0):
		self._ninterface = ninterface
		self._endpoint = endpoint
		self._protocol_type = protocol_type
		self._channel_id = channel_id
		self._receiver_buffer = []
		self._sender_buffer = []

		self._packet_receiver = None

	def initialize(self, ninterface, endpoint, protocol_type="TCP", channel_id=0):
		self._ninterface = ninterface
		self._endpoint = endpoint
		self._protocol_type = protocol_type
		self._channel_id = channel_id

		if self._protocol_type == "TCP":
			if self._packet_receiver:
				self._packet_receiver.get_type() == 
