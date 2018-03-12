# -*- coding: utf-8 -*-

from packet import TCPPacket
from packet_receiver import PacketReceiver


class TCPPacketReceiver(PacketReceiver):

	def __init__(self, endpoint=None, networkinterface=None):
		super(TCPPacketReceiver, self).__init__(endpoint, networkinterface)

	def processFilteredPacket(self, channel, packet):
		packet and channel.addReceiveWindow(packet)
		return True

	def processRecv(self, expecting_packet):
		channel = self.get_channel()
		if not channel or channel.isCondemn():
			return False

		packet = TCPPacket()
		length = packet.recvFromEndPoint(self._endpoint)
		if length < 0:
			self.onGetError(channel)
			return False
		elif length == 0:
			return False

		if not self.processPacket(channel, packet):
			print "processRecv failed"

		return True

	def checkSocketErrors(self, len, expecting_packet):
		pass

	def onGetError(self, channel):
		print 'onGetError:', channel
		channel.get_network_interface().deregisterChannel(channel)
		channel.destroy()

	def get_type(self):
		return PacketReceiver.TCP_PACKET_RECEIVER