#-- coding: utf-8 -*-

import os
import socket

from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, ECONNRESET, EINVAL, EAGAIN, \
					ENOTCONN, ESHUTDOWN, EISCONN, EBADF, ECONNABORTED, EPIPE, errorcode

if os.name == 'nt':
	from errno import WSAEWOULDBLOCK
else:
	WSAEWOULDBLOCK = 10035

_DISCONNECTED = frozenset((ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED, EPIPE, EBADF))


class EndPointClosedException(Exception):
	pass


class Address(object):

	def __init__(self, ip, port):
		self._ip = ip
		self._port = port

	@property
	def ip(self):
		return self._ip

	@property
	def port(self):
		return self._port

	@ip.setter
	def ip(self, ip):
		self._ip = ip

	@port.setter
	def port(self, port):
		self._port = port

	def __str__(self):
		return (self._ip, self._port)

	def __repr__(self):
		return (self._ip, self._port)


class EndPoint(object):

	def __init__(self, sock=None, addr=None):
		self._socket = sock
		self._address = addr
		self._socket_family = None
		self._socket_type = None

	def get_socket(self):
		return self._socket

	def get_fd(self):
		return self._socket.fileno() if self._socket else 0

	def get_addr(self):
		return self._address

	def good(self):
		return True if self._socket else False

	def create_socket(self, family=None, type=None):
		self._socket_family = family if family is not None else socket.AF_INET
		self._socket_type = type if type is not None else socket.SOCK_STREAM
		self._socket = socket.socket(self._socket_family, self._socket_type)

	def setnonblocking(self):
		self._socket.setblocking(0)

	def setbroadcast(self, broadcast):
		pass

	def setreuseaddr(self):
		try:
			self._socket.setsockopt(
				socket.SOL_SOCKET, socket.SO_REUSEADDR,
				self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1)
		except socket.error:
			pass

	def setkeepalive(self, keepalive):
		pass

	def setnodelay(self):
		if self._socket is not None \
				and self._socket.family in (socket.AF_INET, socket.AF_INET6):
			try:
				self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
			except socket.error as e:
				if e.errno != EINVAL:
					raise

	def bind(self, ip, port):
		self._address = Address(ip, port)
		self._socket.bind((ip, port))

	def listen(self, backlog = 5):
		self.accepting = True
		if os.name == 'nt' and backlog > 5:
			backlog = 5
		return self._socket.listen(backlog)

	def connect(self, port = None, addr = None, autosetflags = True):
		self.connected = False
		self.connecting = True
		err = self._socket.connect_ex((addr, port))
		if err in (EINPROGRESS, EALREADY, EWOULDBLOCK, WSAEWOULDBLOCK) \
				or err == EINVAL and os.name in ('nt', 'ce'):
			self._address = (addr, port)
			return
		if err in (0, EISCONN):
			self._address = (addr, port)
		else:
			raise socket.error(err, errorcode[err])

	def accept(self):
		try:
			conn, addr = self._socket.accept()
		except TypeError:
			return None
		except socket.error as why:
			if why.args[0] in (EWOULDBLOCK, ECONNABORTED, EAGAIN):
				return None
			else:
				raise
		else:
			return EndPoint(conn, addr)

	def send(self, data):
		try:
			result = self._socket.send(data)
			return result
		except socket.error, why:
			if why.args[0] == EWOULDBLOCK:
				return 0
			elif why.args[0] in _DISCONNECTED:
				raise EndPointClosedException
			else:
				raise

	def recv(self, buffer_size):
		try:
			data = self._socket.recv(buffer_size)
			if not data:
				# a closed connection is indicated by signaling
				# a read condition, and having recv() return 0.
				raise EndPointClosedException
			else:
				return data
		except socket.error, why:
			# winsock sometimes raises ENOTCONN
			if why.args[0] in _DISCONNECTED:
				raise EndPointClosedException
			else:
				raise

	def close(self):
		try:
			self._socket and self._socket.close()
		except:
			pass
