# -*- coding: utf-8 -*-


class Packet(object):

	def __init__(self, msgID=0, isTCPPacket=True, size=0):
		self._data = ''
		self._size = size
		self._msgid = msgID
		self._is_tcp_packet = isTCPPacket

	def recvFromEndPoint(self, endpoint):
		pass

	def set_size(self, size):
		self._size = size

	def isEmpty(self):
		return len(self._data) <= 0

	def isFull(self):
		return len(self._data) == self._size

	def resetPacket(self):
		self._data = ''
		self._msgid = 0
		self._is_tcp_packet = True


class TCPPacket(Packet):

	def recvFromEndPoint(self, endpoint):
		if self._size > len(self._data):
			new_data = endpoint.recv(self._size - len(self._data))
			self._data = ''.join([self._data, new_data])
