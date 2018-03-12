#-- coding: utf-8 -*-

from endpoint import EndPoint
from event_poller import EventPoller


class EventDispatcher(object):

	EVENT_DISPATCHER_STATUS_RUNNING = 0
	EVENT_DISPATCHER_STATUS_WAITING_BREAK_PROCESSING = 1
	EVENT_DISPATCHER_STATUS_BREAK_PROCESSING = 2

	def __init__(self):
		self._break_processing = 0
		self._maxwait = 0
		self._num_timer_calls = 0

		self._poller = EventPoller.create()

	def processOnce(self, should_idle=False):
		if self._break_processing != EventDispatcher.EVENT_DISPATCHER_STATUS_BREAK_PROCESSING:
			self._break_processing = EventDispatcher.EVENT_DISPATCHER_STATUS_RUNNING;

		self.processTasks()

		if self._break_processing != EventDispatcher.EVENT_DISPATCHER_STATUS_BREAK_PROCESSING:
			self.processTimers()

		self.processStats()

		if self._break_processing != EventDispatcher.EVENT_DISPATCHER_STATUS_BREAK_PROCESSING:
			return self.processNetwork(should_idle)

		return 0

	def processUtilBreak(self):
		if self._break_processing != EventDispatcher.EVENT_DISPATCHER_STATUS_BREAK_PROCESSING:
			self._break_processing = EventDispatcher.EVENT_DISPATCHER_STATUS_RUNNING;

		while self._break_processing != EventDispatcher.EVENT_DISPATCHER_STATUS_BREAK_PROCESSING:
			self.processOnce(True)

	def breakProcessing(self, break_state=True):
		if break_state:
			self._break_processing = EventDispatcher.EVENT_DISPATCHER_STATUS_BREAK_PROCESSING
		else:
			self._break_processing = EventDispatcher.EVENT_DISPATCHER_STATUS_RUNNING

	def setWaitBreakProcessing(self):
		self._break_processing = EventDispatcher.EVENT_DISPATCHER_STATUS_WAITING_BREAK_PROCESSING

	def registerReadFileDescriptor(self, fd, handler):
		assert isinstance(fd, EndPoint)

		return self._poller.registerForRead(fd.get_fd(), handler)

	def deregisterReadFileDescriptor(self, fd):
		assert isinstance(fd, EndPoint)

		self._poller.deregisterForRead(fd.get_fd())

	def registerWriteFileDescriptor(self, fd, handler):
		assert isinstance(fd, EndPoint)

		return self._poller.registerForWrite(fd.get_fd(), handler)

	def deregisterWriteFileDescriptor(self, fd):
		assert isinstance(fd, EndPoint)

		self._poller.deregisterForWrite(fd.get_fd())

	def processNetwork(self, should_idle):
		max_wait = self.calculateWait() if should_idle else 0.0
		return self._poller.processPendingEvents(max_wait)

	def processTasks(self):
		pass

	def processTimers(self):
		pass

	def processStats(self):
		pass

	def calculateWait(self):
		return self._maxwait

	def destroy(self):
		if self._poller:
			self._poller.destroy()
		self._poller = None