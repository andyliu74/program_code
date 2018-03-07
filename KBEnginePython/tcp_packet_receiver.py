# -*- coding: utf-8 -*-

from packet_receiver import PacketReceiver


class TCPPacketReceiver(PacketReceiver):

	def __init__(self, endpoint=None, networkinterface=None):
		super(TCPPacketReceiver, self).__init__(endpoint, networkinterface)

	def processFilteredPacket(self, channel, packet):
		pass

	def processRecv(self, expecting_packet):
		channel = self.get_channel()
		if not channel or channel.isCondemn():
			return False

		

	def checkSocketErrors(self, len, expecting_packet):
		pass

	def onGetError(self, channel):
		pass