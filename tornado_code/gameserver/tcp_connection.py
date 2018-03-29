# -*- coding: utf-8 -*-

from tornado import stack_context

class TCPConnection(object):

	def __init__(self, stream, address, io_loop):
		self.stream = stream
		self.io_loop = io_loop
		self.address = address
		self.address_family = stream.socket.family

		self._close_callback = None
		self._write_callback = None
		self._method_callback = None

		self.stream.set_close_callback(self._on_connection_close)
		self._receive_callback = stack_context.wrap(self._on_receive_data)

		self._rpc_channel = None

	def start(self):
		self.stream.read_until_close(streaming_callback=self._receive_callback)

	def write(self, data, callback=None):
		if self.stream.closed():
			return
		self._write_callback = stack_context.wrap(callback)
		self.stream.write(data, self._on_write_complete)

	def set_close_callback(self, callback):
		self._close_callback = stack_context.wrap(callback)

	def set_method_callback(self, callback):
		self._method_callback = stack_context.wrap(callback)

	def get_rpc_channel(self):
		return self._rpc_channel

	def set_rpc_channel(self, rpc_channel):
		self._rpc_channel = rpc_channel

	def disconnect(self):
		self.stream.close()
		self._write_callback = None
		self._close_callback = None
		self._method_callback = None
		self._rpc_channel and self._rpc_channel.on_disconnected()
		self._rpc_channel = None

	def _on_receive_data(self, data):
		self._rpc_channel and self._rpc_channel.receive(data)

	def _on_write_complete(self):
		if self._write_callback is not None:
			callback = self._write_callback
			self._write_callback = None
			callback()

	def _on_connection_close(self):
		if self._close_callback is not None:
			callback = self._close_callback
			self._close_callback = None
			callback()
		self.disconnect()
