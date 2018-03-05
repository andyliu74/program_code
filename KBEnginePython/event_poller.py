# -*- coding: utf-8 -*-


class EventPoller(object):

	# Constants from the epoll module
	_EPOLLIN = 0x001
	_EPOLLPRI = 0x002
	_EPOLLOUT = 0x004
	_EPOLLERR = 0x008
	_EPOLLHUP = 0x010
	_EPOLLRDHUP = 0x2000
	_EPOLLONESHOT = (1 << 30)
	_EPOLLET = (1 << 31)

	# Our events map exactly to the epoll events
	NONE = 0
	READ = _EPOLLIN
	WRITE = _EPOLLOUT
	ERROR = _EPOLLERR | _EPOLLHUP

	def __init__(self):
		self._fd_read_handlers = {}
		self._fd_write_handlers = {}

	@staticmethod
	def create():
		from poller_select import SelectPoller
		return SelectPoller()

	def processPendingEvents(self, max_wait):
		raise NotImplementedError()

	def registerForRead(self, fd, handler):
		if not self.doRegisterForRead(fd):
			return False
		self._fd_read_handlers[fd] = handler
		return True

	def registerForWrite(self, fd, handler):
		if not self.doRegisterForWrite(fd):
			return False
		self._fd_write_handlers[fd] = handler
		return True

	def deregisterForRead(self, fd):
		try:
			del self._fd_read_handlers[fd]
		except:
			pass

	def deregisterForWrite(self, fd):
		try:
			del self._fd_write_handlers[fd]
		except:
			pass

	def doRegisterForRead(self, fd):
		raise NotImplementedError()

	def doRegisterForWrite(self, fd):
		raise NotImplementedError()

	def doDeregisterForRead(self, fd):
		raise NotImplementedError()

	def doDeregisterForWrite(self, fd):
		raise NotImplementedError()

	def triggerRead(self, fd):
		handler = self._fd_read_handlers.get(fd, None)
		if not handler:
			return False
		handler.handleInputNotification(fd)
		return True

	def triggerWrite(self, fd):
		handler = self._fd_write_handlers.get(fd, None)
		if not handler:
			return False
		handler.handleOutputNotification(fd)
		return True