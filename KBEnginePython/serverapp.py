# -*- coding: utf-8 -*-

class ServerApp(object):

	def __init__(self, dispatcher, ninterface, component_type, component_id):
		self._dispatcher = dispatcher
		self._ninterface = ninterface
		self._component_type = component_type
		self._component_id = component_id

	def initialize(self):
		pass

	def run(self):
		self._dispatcher and self._dispatcher.processUtilBreak()