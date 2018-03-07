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


class EndPoint(object):

	def __init__(self, sock=None, addr=None):
		self._socket = sock
		self._address = addr

	@property
	def socket(self):
		return self._socket

	@property
	def fd(self):
		return self._socket.fileno() if self._socket else 0

	def good(self):
		return True if self._socket else False

	def create_socket(self, family=None, type=None):
		self.socket_family = family if family is not None else socket.AF_INET
		self.socket_type = type if type is not None else socket.SOCK_STREAM
		self._socket = socket.socket(self.socket_family, self.socket_type)

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

	def bind(self, port, addr):
		return self._socket.bind((addr, port))

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
			conn, addr = self.socket.accept()
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
			result = self.socket.send(data)
			return result
		except socket.error, why:
			if why.args[0] == EWOULDBLOCK:
				return 0
			elif why.args[0] in _DISCONNECTED:
				self.handle_close()
				return 0
			else:
				raise

	def recv(self, buffer_size):
		try:
			data = self.socket.recv(buffer_size)
			if not data:
				# a closed connection is indicated by signaling
				# a read condition, and having recv() return 0.
				self.handle_close()
				return ''
			else:
				return data
		except socket.error, why:
			# winsock sometimes raises ENOTCONN
			if why.args[0] in _DISCONNECTED:
				self.handle_close()
				return ''
			else:
				raise
