# -*- coding: utf-8 -*-

from endpoint import EndPointClosedException


class Packet(object):

	PACKET_MAX_SIZE_TCP = 1460
	PACKET_MAX_SIZE_UDP = 1472

	def __init__(self, msgID=0, isTCPPacket=True, size=0):
		self._data = ''
		self._size = size
		self._msgid = msgID
		self._encrypted = False
		self._is_tcp_packet = isTCPPacket

	def recvFromEndPoint(self, endpoint):
		raise NotImplementedError()

	def get_size(self):
		return self._size

	def set_size(self, size):
		self._size = size

	def isEmpty(self):
		return len(self._data) == 0

	def resetPacket(self):
		self._msgid = 0
		self._encrypted = False
		self._is_tcp_packet = True

	def isTCPPacket(self):
		return self._is_tcp_packet

	def get_encrypted(self):
		return self._encrypted

	def get_msgid(self):
		return self._msgid

	def get_length(self):
		return len(self._data)


class TCPPacket(Packet):

	def __init__(self, msgID=0, isTCPPacket=True, size=Packet.PACKET_MAX_SIZE_TCP):
		super(TCPPacket, self).__init__(msgID, isTCPPacket, size)

	def recvFromEndPoint(self, endpoint):
		assert self._size > len(self._data)
		try:
			new_data = endpoint.recv(self._size - len(self._data))
			self._data = ''.join([self._data, new_data])
			return len(new_data)
		except EndPointClosedException:
			return -1


class PacketFilter(object):

	def send(self, channel, sender, packet):
		return sender.processFilterPacket(channel, packet)

	def recv(self, channel, receiver, packet):
		return receiver.processFilteredPacket(channel, packet)
