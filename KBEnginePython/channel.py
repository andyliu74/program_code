#-- coding: utf-8 -*-

import time

# from packet import PacketFilter
from packet_receiver import PacketReceiver
from tcp_packet_receiver import TCPPacketReceiver

class Channel(object):

	# 普通通道
	CHANNEL_NORMAL = 0,
	# 浏览器web通道
	CHANNEL_WEB = 1,

	g_receivered_packet_num = 0
	g_receivered_bytes_num = 0

	def __init__(self, ninterface=None, endpoint=None, protocol_type="TCP", channel_id=0):
		self._ninterface = ninterface
		self._endpoint = endpoint
		self._protocol_type = protocol_type
		self._channel_id = channel_id

		self._packet_filter = None

		self._receiver_buffer = []
		self._sender_buffer = []

		self._packet_receiver = None
		self._packet_sender = None

		self._last_receivered_time = 0
		self._receivered_packet_num = 0
		self._receivered_bytes_num = 0
		self._last_tick_receivered_bytes = 0

	def initialize(self, ninterface, endpoint, protocol_type="TCP", channel_id=0):
		self._ninterface = ninterface
		self._endpoint = endpoint
		self._protocol_type = protocol_type
		self._channel_id = channel_id

		if self._protocol_type == "TCP":
			if self._packet_receiver:
				if self._packet_receiver.get_type() == PacketReceiver.UDP_PACKET_RECEIVER:
					self._packet_receiver = TCPPacketReceiver(self._endpoint, self._ninterface)
			else:
				self._packet_receiver = TCPPacketReceiver(self._endpoint, self._ninterface)

			assert self._packet_receiver.get_type() == PacketReceiver.TCP_PACKET_RECEIVER

			self._ninterface.get_dispatcher().registerReadFileDescriptor(self._endpoint, self._packet_receiver)
		else:
			pass

		self._packet_receiver.set_endpoint(self._endpoint)
		self._packet_sender and self._packet_sender.set_endpoint(self._endpoint)

		return True

	def onPacketReceived(self, length):
		self._last_receivered_time = time.time()
		self._receivered_packet_num += 1
		Channel.g_receivered_packet_num += 1

		if length > 0:
			Channel.g_receivered_bytes_num += length
			self._receivered_bytes_num += length
			self._last_tick_receivered_bytes += length

		pass

	def addReceiveWindow(self, packet):
		print 'addReceiveWindow:', self._receivered_packet_num, packet.get_size()
		self._receiver_buffer.append(packet)
		pass

	def get_filter(self):
		return self._packet_filter

	def set_filter(self, packet_filter):
		self._packet_filter = packet_filter

	def get_endpoint(self):
		return self._endpoint

	def get_network_interface(self):
		return self._ninterface

	def destroy(self):
		if len(self._receiver_buffer) > 0:
			pass
		self._receiver_buffer = []

		self._packet_filter = None
		self._packet_receiver = None
		self._packet_sender = None

		self._last_receivered_time = 0
		self._receivered_packet_num = 0
		self._receivered_bytes_num = 0
		self._last_tick_receivered_bytes = 0

		if self._ninterface:
			self._ninterface.get_dispatcher().deregisterWriteFileDescriptor(self._endpoint)
			self._ninterface.get_dispatcher().deregisterReadFileDescriptor(self._endpoint)
		self._ninterface = None

		if self._endpoint:
			self._endpoint.close()
		self._endpoint = None

	def isExternal(self):
		return True

	def isCondemn(self):
		return False