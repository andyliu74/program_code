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

		self.ext_endpoint = EndPoint()
		self.int_endpoint = EndPoint()

		self.external_listener_receiver = None
		self.internal_listener_receiver = None

		if self.is_external():
			self.external_listener_receiver = ListenerReceiver(self.ext_endpoint, self)
			self.initialize("EXTERNAL", 
					self._extlistening_min_port, 
					self._extlistening_max_port, 
					self._extlistening_interface, 
					self.ext_endpoint, 
					self.external_listener_receiver)

		self.internal_listener_receiver = ListenerReceiver(self.int_endpoint, self)
		self.initialize("INTERNAL", 
					self._intlistening_port, 
					self._intlistening_port, 
					self._intlistening_interface, 
					self.int_endpoint, 
					self.internal_listener_receiver)

	def initialize(self, endpoint_name, min_port, max_port, listening_interface, endpoint, receiver):
		if endpoint.good():
			self._dispatcher.deregisterReadFileDescriptor(endpoint)
			endpoint.close()

		endpoint.create_socket()
		if not endpoint.good():
			print "NetworkInterface::initialize(): couldn't create a socket %s " % endpoint_name
			return False

		if min_port > 0 and min_port == max_port:
			endpoint.setreuseaddr(True)

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
			if endpoint.bind(listening_port, bind_addr) == 0:
				found_port = True

		if not found_port:
			print "NetworkInterface::initialize(): Couldn't bind the socket to %s:%s " % (bind_addr, str(listening_port))
			endpoint.close()
			return False

		endpoint.setnonblocking()
		endpoint.setnodelay(True)

		if endpoint.listen(5) == -1:
			print "NetworkInterface::initialize(): listen to %s (%s)" % (endpoint_name, bind_addr)
			endpoint.close()
			return

		print "NetworkInterface::initialize(): success"

		return True
