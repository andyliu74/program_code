# -*- coding: utf-8 -*-

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
				pass
			else:
				pass