# -*- coding: utf-8 -*-

class InputNotificationHandler(object):

	def handleInputNotification(self, fd):
		raise NotImplementedError()


class OutputNotificationHandler(object):

	def handleOutputNotification(self, fd):
		raise NotImplementedError()