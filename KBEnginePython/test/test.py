#-- coding: utf-8 -*-

import sys
sys.path.append('../')

from endpoint import EndPoint
from event_dispatcher import EventDispatcher
from listener_receiver import ListenerReceiver


def main():
	end_point = EndPoint()
	end_point.create_socket()
	end_point.bind(8888, '0.0.0.0')
	end_point.listen()

	dispatcher = EventDispatcher()
	receiver = ListenerReceiver(end_point, None)
	dispatcher.registerReadFileDescriptor(end_point.fd, receiver)
	dispatcher.processUtilBreak()


if __name__ == "__main__":
	try:
		main()
	except:
		import traceback
		print traceback.format_exc()