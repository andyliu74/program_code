#-- coding: utf-8 -*-

class EventDispatcher(object):

	EVENT_DISPATCHER_STATUS_RUNNING = 0
	EVENT_DISPATCHER_STATUS_WAITING_BREAK_PROCESSING = 1
	EVENT_DISPATCHER_STATUS_BREAK_PROCESSING = 2

	def __init__(self):
		self._break_processing = 0
		self._maxwait = 0
		self._num_timer_calls = 0

		self._poller = EventPoller()
