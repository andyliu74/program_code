# -*- coding: utf-8 -*-

from endpoint import EndPoint
from listener_receiver import ListenerReceiver


class NetworkInterface(object):

	def __init__(self, dispatcher, extlistening_min_port, extlistening_max_port, extlistening_interface, 
					intlistening_port, intlistening_interface):
		self._dispatcher = dispatcher
		self._extlistening_min_port = extlistening_min_port
		self._extlistening_max_port = extlistening_max_port
		self._extlistening_interface = extlistening_interface

		self._intlistening_port = intlistening_port
		self._intlistening_interface = intlistening_interface

		self._ext_endpoint = EndPoint()
		self._int_endpoint = EndPoint()

		self._external_listener_receiver = None
		self._internal_listener_receiver = None

		self._channel_map = {}
		self._ext_channel_num = 0

		if self.isExternal():
			self._external_listener_receiver = ListenerReceiver(self._ext_endpoint, self)
			self.initialize("EXTERNAL", 
					self._extlistening_min_port, 
					self._extlistening_max_port, 
					self._extlistening_interface, 
					self._ext_endpoint, 
					self._external_listener_receiver)

		self._internal_listener_receiver = ListenerReceiver(self._int_endpoint, self)
		self.initialize("INTERNAL", 
				self._intlistening_port, 
				self._intlistening_port, 
				self._intlistening_interface, 
				self._int_endpoint, 
				self._internal_listener_receiver)

	def isExternal(self):
		return self._extlistening_min_port >= 0

	def closeSocket(self):
		if self._ext_endpoint and self._ext_endpoint.good():
			self._dispatcher.deregisterReadFileDescriptor(self._ext_endpoint)
			self._ext_endpoint.close()
		if self._int_endpoint and self._int_endpoint.good():
			self._dispatcher.deregisterReadFileDescriptor(self._int_endpoint)
			self._int_endpoint.close()

	def destroy(self):
		for addr, channel in self._channel_map.iteritems():
			channel and channel.destroy()
		self._channel_map.clear()
		self._ext_channel_num = 0

		self.closeSocket()
		self._ext_endpoint = None
		self._int_endpoint = None

		if self._dispatcher:
			self._dispatcher.destroy()
		self._dispatcher = None

		if self._external_listener_receiver:
			self._external_listener_receiver.destroy()
		self._external_listener_receiver = None

		if self._internal_listener_receiver:
			self._internal_listener_receiver.destroy()
		self._internal_listener_receiver = None

	def initialize(self, endpoint_name, min_port, max_port, listening_interface, endpoint, receiver):
		if endpoint.good():
			self._dispatcher.deregisterReadFileDescriptor(endpoint)
			endpoint.close()

		endpoint.create_socket()
		if not endpoint.good():
			print "NetworkInterface::initialize(): couldn't create a socket %s " % endpoint_name
			return False

		if min_port > 0 and min_port == max_port:
			endpoint.setreuseaddr()

		self._dispatcher.registerReadFileDescriptor(endpoint, receiver)

		bind_addr = '0.0.0.0'

		found_port = False
		listening_port = min_port
		if min_port != max_port:
			for port in xrange(min_port, max_port):
				listening_port = port
				if endpoint.bind(listening_port, bind_addr) != 0:
					continue
				else:
					found_port = True
					break
		else:
			endpoint.bind(bind_addr, listening_port)
			found_port = True

		if not found_port:
			print "NetworkInterface::initialize(): Couldn't bind the socket to %s:%s " % (bind_addr, str(listening_port))
			endpoint.close()
			return False

		endpoint.setnonblocking()
		endpoint.setnodelay()

		if endpoint.listen(5) == -1:
			print "NetworkInterface::initialize(): listen to %s (%s)" % (endpoint_name, bind_addr)
			endpoint.close()
			return

		print "NetworkInterface::initialize(): success"

		return True

	def get_dispatcher(self):
		return self._dispatcher

	def findChannelByAddr(self, addr):
		return self._channel_map.get(addr, None)

	def findChannelByFD(self, fd):
		for addr, channel in self._channel_map.iteritems():
			if channel and channel.get_endpoint():
				if channel.get_endpoint().get_fd() == fd:
					return channel
		return None

	def registerChannel(self, channel):
		assert channel
		assert channel.get_endpoint()

		addr = channel.get_endpoint().get_addr()
		if not addr or addr in self._channel_map.keys():
			return False

		self._channel_map[addr] = channel

		if channel.isExternal():
			self._ext_channel_num += 1

		return True

	def deregisterAllChannels(self):
		self._channel_map = {}
		self._ext_channel_num = 0
		return True

	def deregisterChannel(self, channel):
		assert channel
		assert channel.get_endpoint()

		addr = channel.get_endpoint().get_addr()
		if addr in self._channel_map.keys():
			del self._channel_map[addr]
			self._ext_channel_num -= 1

		return True

	def processChannels(self, msg_handlers):
		for addr, channel in self._channel_map.iteritems():
			if channel.isDestroyed():
				continue
			if channel.isCondemn():
				self.deregisterChannel(channel)
				channel.destroy()
				continue
			channel.processPackets(msg_handlers)

