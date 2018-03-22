# -*- coding: utf-8 -*-

class Entity(object):

	def __init__(self, client=None):
		self.client = client
		self.client.set_method_callback(self._on_method_callback)

	def _on_method_callback(self, data):
		try:
			pass
		except:
			print '_on_method_callback error'
