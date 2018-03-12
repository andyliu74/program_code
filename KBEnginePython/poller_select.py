# -*- coding: utf-8 -*-

import select
from event_poller import EventPoller


class SelectPoller(EventPoller):

	def __init__(self):
		super(SelectPoller, self).__init__()
		self.read_fds = set()
		self.write_fds = set()
		self.error_fds = set()
		self.fd_sets = (self.read_fds, self.write_fds, self.error_fds)

	def doRegisterForRead(self, fd):
		if fd in self.read_fds:
			return False
		self.read_fds.add(fd)
		return True

	def doRegisterForWrite(self, fd):
		if fd in self.write_fds:
			return False
		self.write_fds.add(fd)
		return True

	def doDeregisterForRead(self, fd):
		self.read_fds.discard(fd)

	def doDeregisterForWrite(self, fd):
		self.write_fds.discard(fd)

	def handleNotifications(self, events):
		for fd, event in events.iteritems():
			if event & EventPoller.READ:
				self.triggerRead(fd)
			if event & EventPoller.WRITE:
				self.triggerWrite(fd)

	def processPendingEvents(self, max_wait):
		assert self.read_fds or self.write_fds or self.error_fds
		# print 'processPendingEvents:', self.read_fds, self.write_fds, self.error_fds
		readable, writeable, errors = select.select(
			self.read_fds, self.write_fds, self.error_fds, max_wait)
		events = {}
		for fd in readable:
			events[fd] = events.get(fd, 0) | EventPoller.READ
		for fd in writeable:
			events[fd] = events.get(fd, 0) | EventPoller.WRITE
		for fd in errors:
			events[fd] = events.get(fd, 0) | EventPoller.ERROR

		if events:
			self.handleNotifications(events)