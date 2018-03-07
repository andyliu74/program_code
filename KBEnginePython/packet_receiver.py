# -*- coding: utf-8 -*-

# from channel import Channel
from interfaces import InputNotificationHandler


class PacketReceiver(InputNotificationHandler):

	TCP_PACKET_RECEIVER = 0
	UDP_PACKET_RECEIVER = 1

	RECV_STATE_INTERRUPT = -1
	RECV_STATE_BREAK = 0
	RECV_STATE_CONTINUE = 1

	def __init__(self, endpoint=None, networkinterface=None):
		self._channel = None
		self._endpoint = endpoint
		self._networkinterface = networkinterface

	def handleInputNotification(self, fd):
		if self.processRecv(True):
			while self.processRecv(False):
				pass
		return 0

	def processPacket(self, channel, packet):
		if self._channel:
			self._channel.onPacketReceived(packet.get_length())
			if channel.get_filter():
				return channel.get_filter().recv(channel, self, packet)
		return self.processFilteredPacket(channel, packet)

	def processFilteredPacket(self, channel, packet):
		raise NotImplementedError()

	def get_type(self):
		raise NotImplementedError()

	def get_endpoint(self):
		return self._endpoint

	def get_dispatcher(self):
		if self._networkinterface:
			return self._networkinterface.get_dispatcher()
		return None

	def set_endpoint(self, endpoint):
		self._endpoint = endpoint
		self._channel = None

	def get_network_interface(self):
		return self._networkinterface

	def get_channel(self):
		if self._channel:
			if self._channel.isDestroyed():
				return None
			return self._channel
		if self._endpoint and self._networkinterface:
			return self._networkinterface.findChannel(self._endpoint.get_addr())
		return None