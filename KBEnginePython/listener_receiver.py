# -*- coding: utf-8 -*-

from channel import Channel
from interfaces import InputNotificationHandler


class ListenerReceiver(InputNotificationHandler):

	def __init__(self, endpoint, networkinterface):
		self._endpoint = endpoint
		self._networkinterface = networkinterface

	def handleInputNotification(self, fd):
		tick_count = 0
		while tick_count < 256:
			new_endpoint = self._endpoint.accept()
			if new_endpoint:
				print 'new_client'
				new_channel = Channel()
				if not new_channel.initialize(self._networkinterface, new_endpoint):
					print "ListenerReceiver::handleInputNotification: initialize() is failed!"
					new_channel.destroy()
					return
				if not self._networkinterface.registerChannel(new_channel):
					print "ListenerReceiver::handleInputNotification: registerChannel() is failed!"
					new_channel.destroy()
					return
			else:
				if tick_count == 0:
					print "PacketReceiver::handleInputNotification: accept endpoint()! channelSize="
				break
			tick_count += 1
		return